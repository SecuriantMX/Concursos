"""
Pruebas del modelo, del armado de boletos y de la auditoria.
Uso: python3 pruebas.py

Cada bloque cubre un defecto que ya aparecio una vez (revisiones del 16-nov-2026)
o una propiedad que el resto del codigo da por hecha. Las afirmaciones llevan
valores concretos a proposito: una prueba que solo mira que "corra" no detecta
que el calculo cambio.
"""
import contextlib
import io
import itertools
import json
import os
import shutil
import subprocess
import sys
import tempfile
import warnings

import auditoria as A
import boletos as B
import modelo as M

AQUI = os.path.dirname(os.path.abspath(__file__))
L, E, V = (0,), (1,), (2,)


def cerca(a, b, tol=1e-9):
    return abs(a - b) <= tol


def callado(f, *args):
    with contextlib.redirect_stdout(io.StringIO()) as buf:
        r = f(*args)
    return r, buf.getvalue()


def prueba_shin():
    for momios in ([1.16, 6.60, 13.00], [2.30, 3.22, 3.08], [1.02, 21.0, 67.0], [1.90, 1.90]):
        p, z = M.shin(momios)
        assert cerca(sum(p), 1.0, 1e-9) and 0 <= z < 0.2, momios
        assert p.index(max(p)) == momios.index(min(momios))
    # valor conocido (ecuacion de Shin resuelta aparte). La normalizacion proporcional
    # daria 0.7905 / 0.1389 / 0.0705 con estos momios: Shin le quita menos al favorito
    p, z = M.shin([1.16, 6.60, 13.00])
    assert all(cerca(a, b, 1e-8) for a, b in zip(p, [0.8211015946, 0.1250313407, 0.0538670646]))
    assert cerca(z, 0.0495316677, 1e-8)
    assert p[0] > M.proporcional([1.16, 6.60, 13.00])[0]
    # sin margen no hay nada que quitar
    p, z = M.shin([2.0, 4.0, 4.0])
    assert all(cerca(a, b, 1e-6) for a, b in zip(p, [0.5, 0.25, 0.25])) and z < 1e-6


def prueba_elo():
    # dentro del rango alcanzable (603 puntos con 2.81 goles), el 1X2 reproduce el We de Elo sin avisar
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        for dr in range(-600, 601, 25):
            p, we = M.elo_1x2(1500 + dr, 1500, 0, 2.81, -0.10)
            assert cerca(sum(p), 1.0, 1e-9)
            assert cerca(p[0] + 0.5 * p[1], M.elo_esperado(1500 + dr, 1500, 0), 1e-7), dr
            assert cerca(we, p[0] + 0.5 * p[1], 1e-12)
    # simetria: cambiar de lado invierte L y V
    a, _ = M.elo_1x2(1700, 1500, 0, 2.81, 0.0)
    b, _ = M.elo_1x2(1500, 1700, 0, 2.81, 0.0)
    assert cerca(a[0], b[2], 1e-7) and cerca(a[1], b[1], 1e-7)
    # fuera del rango: avisa y devuelve el We que de verdad reproduce, no el pedido
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        p, we = M.elo_1x2(2290, 1352, 100, 2.81, -0.10)
    assert len(w) == 1 and cerca(we, p[0] + 0.5 * p[1], 1e-12)
    assert we < M.elo_esperado(2290, 1352, 100)


def mejor_bruto(P, juego, tope):
    """Mejor probabilidad de acertar todo, probando todas las formas de sencillo, doble y triple."""
    mejor = -1.0
    for forma in itertools.product((1, 2, 3), repeat=len(P)):
        t, d = forma.count(3), forma.count(2)
        if t not in juego["max_dobles"] or d > juego["max_dobles"][t]:
            continue
        if juego["precio"] * 3 ** t * 2 ** d > tope:
            continue
        pr = 1.0
        for p, k in zip(P, forma):
            pr *= sum(sorted(p, reverse=True)[:k])
        mejor = max(mejor, pr)
    return mejor


def prueba_boleto_optimo():
    sal = json.load(open(os.path.join(AQUI, "salida_ms822.json")))
    P = [f["p"] for f in sal["partidos"]]
    juego = {"precio": 15, "max_dobles": {0: 3, 1: 3, 2: 3}}
    for tope in (15, 135, 540, 1000, 1100):
        b = B.mejor_por_probabilidad(P, juego, tope)
        assert B.valido(b, juego, tope)
        assert cerca(B.prod(B.cobertura(b, P)), mejor_bruto(P, juego, tope), 1e-12), tope
    assert cerca(sum(B.dist_aciertos(B.cobertura(b, P))), 1.0, 1e-12)
    # el boleto guardado es el que sale de las probabilidades guardadas
    r = B.resumen(B.mejor_por_probabilidad(P, juego, 1100), P, juego)
    assert r["picks"] == sal["progol"]["recomendado"]["picks"] and r["costo"] <= 1100


def prueba_complemento():
    P = [[0.5, 0.3, 0.2]] * 7
    juego = B.REVANCHA
    # los previos cubren L y E en todo y V en los ultimos 6: solo queda libre el partido 1
    previos = [[L] * 7, [E] * 7, [L] + [V] * 6]
    assert B.mejor_complemento(P, juego, 5, previos, min_distintos=2) is None
    b = B.mejor_complemento(P, juego, 5, previos, min_distintos=1)
    assert b is not None and b[0] == V
    # con espacio de sobra, lo que devuelve si cumple la exigencia
    previos = [[L] * 7]
    b = B.mejor_complemento(P, juego, 20, previos, min_distintos=2)
    distintos = sum(set(b[i]).isdisjoint(previos[0][i]) for i in range(7))
    assert B.valido(b, juego, 20) and distintos >= 2


def prueba_triples_fijos():
    """Los triples obligados van donde se piden, aunque no sea donde mas conviene por probabilidad."""
    P = [[0.60, 0.25, 0.15]] * 2 + [[0.40, 0.30, 0.30]] * 5
    Q = [[0.5, 0.3, 0.2]] * 7
    fijos = (0, 1)
    b = B.mejor_complemento(P, B.REVANCHA, 45, [], triples_fijos=fijos, min_distintos=0)
    assert b is not None and all(len(b[i]) == 3 for i in fijos) and B.valido(b, B.REVANCHA, 45)
    b = B.mejor_complemento(P, B.REVANCHA, 45, [[L] * 7], triples_fijos=fijos, min_distintos=2)
    assert b is not None and all(len(b[i]) == 3 for i in fijos)
    assert sum(set(b[i]).isdisjoint(L) for i in range(7)) >= 2
    b = B.mejor_por_valor(P, Q, 1000, B.REVANCHA, 45, 0.0, fijos)
    assert b is not None and all(len(b[i]) == 3 for i in fijos) and B.valido(b, B.REVANCHA, 45)


def salida_de_prueba():
    filas = [dict(id=f"M{i}", local=f"L{i}", visita=f"V{i}", p=[0.5, 0.3, 0.2], conf="alta",
                  comp=dict(mercado=[0.5, 0.3, 0.2], elo=None, poisson=None),
                  publico=[100 / 3] * 3, publico_real=False) for i in range(1, 7)]
    filas[0]["comp"]["mercado"] = [0.6, 0.3, 0.1]                      # mercado distinto del final en M1
    filas[3].update(p=[1 / 3] * 3, conf="nula", comp=dict(mercado=None, elo=None, poisson=None))
    filas[5].update(p=[0.4, 0.2, 0.4], conf="media")                   # con estimacion, pero empatado arriba
    sal = dict(progol=dict(unico=dict(picks=["L", "EV", "LEV", "L", "L", "L"])), revancha={},
               partidos=filas, partidos_rev=[])
    res = dict(corte="prueba", partidos={
        "M1": dict(marcador="1-1", res="E"),      # el favorito (L) falla
        "M2": dict(marcador="2-0", res="L"),
        "M3": dict(marcador="", res=""),          # pendiente: no cuenta y no avisa
        "M4": dict(marcador="1-0", res="L"),      # gana el local donde no hay favorito
        "M5": dict(marcador="?", res="LE"),       # mal capturado: no cuenta y avisa
        "M6": dict(marcador="0-2", res="V"),
        "M9": dict(marcador="1-0", res="L"),      # clave que no es partido de la salida: avisa
    })
    return sal, res


def prueba_auditoria():
    sal, res = salida_de_prueba()
    tmp = tempfile.mkdtemp()
    antes = os.getcwd()
    try:
        os.chdir(tmp)
        json.dump(sal, open("salida_x.json", "w"))
        json.dump(res, open("resultados_x.json", "w"))
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            _, _, f = A.cargar("x")
        avisos = [str(x.message) for x in w if issubclass(x.category, UserWarning)]
        assert len(avisos) == 2 and "M9" in avisos[0] and "M5" in avisos[1] and "'LE'" in avisos[1]
        assert [x["id"] for x in f] == ["M1", "M2", "M4", "M6"]
        assert all(x["publico"] is None for x in f)          # el relleno de 1/3 no es dato del publico
        t, _ = callado(A.tabla_estimadores, f, "prueba")
        assert "publico" not in t and t["final"]["n"] == 4 and t["final*"]["n"] == 3
        # favorito: M1 falla, M2 acierta, M4 y M6 no tienen favorito aunque en M4 gano el local
        assert t["final"]["con_favorito"] == 2 and t["final"]["favorito"] == 1
        assert t["final*"]["con_favorito"] == 2 and t["final*"]["favorito"] == 1
        # el mercado de M6 si tiene favorito (L con 50%) y falla: 3 con favorito, 1 acierto
        assert t["mercado"]["con_favorito"] == 3 and t["mercado"]["favorito"] == 1
        # Brier a mano: M1 final 0.78 y mercado 0.86; M2 0.38; M6 final 0.56 y mercado 0.98
        assert cerca(t["final*"]["brier"], (0.78 + 0.38 + 0.56) / 3, 1e-12)
        assert cerca(t["mercado"]["brier"], (0.86 + 0.38 + 0.98) / 3, 1e-12)
        assert cerca(t["final"]["brier"], (0.78 + 0.38 + 2 / 3 + 0.56) / 4, 1e-12)
        assert A.favorito([1 / 3] * 3) is None and A.favorito([0.2, 0.5, 0.3]) == 1
        for malo in (None, {}, {"res": None}, {"res": ""}, {"res": "LE"}, {"res": "LEV"}, {"res": "v"}, {"res": "L "}):
            assert A.resultado(malo) is None, malo
        assert [A.resultado({"res": x}) for x in "LEV"] == [0, 1, 2]

        # el bloque principal dice por que un partido no trae favorito
        r = subprocess.run([sys.executable, "-B", "-W", "ignore", os.path.join(AQUI, "auditoria.py"), "x"],
                           capture_output=True, text=True)
        assert r.returncode == 0, r.stderr
        lin = {i: next(x for x in r.stdout.splitlines() if x.startswith(f"  {i} ")) for i in ("M1", "M4", "M6")}
        assert "favorito mio L (50%)" in lin["M1"]
        assert "sin favorito (sin estimacion)" in lin["M4"] and "sin favorito (empate en el maximo)" in lin["M6"]
        assert "unico          1 de 4 jugados; faltan 2." in r.stdout     # solo M4 cae dentro del boleto

        # una salida sin la clave publico_real (como la del 2359) trae el porcentaje oficial: se califica
        del sal["partidos"][0]["publico_real"]
        sal["partidos"][0]["publico"] = [45, 30, 15]
        sal["partidos"][1].update(publico=[0, 0, 0], publico_real=True)   # en ceros no es dato
        json.dump(sal, open("salida_x.json", "w"))
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            _, _, f = A.cargar("x")
        assert all(cerca(a, b) for a, b in zip(f[0]["publico"], [0.5, 1 / 3, 1 / 6]))
        assert f[1]["publico"] is None
    finally:
        os.chdir(antes)
        shutil.rmtree(tmp)


def prueba_auditoria_boletos():
    """Los aciertos se cuentan con los ids de la salida: M en Media Semana, P y R en Progol."""
    sal = dict(progol=dict(unico=dict(picks=["L", "EV", "LEV"])), revancha={},
               partidos=[dict(id=f"M{i}") for i in range(1, 4)], partidos_rev=[])
    res = dict(partidos={"M1": dict(res="L"), "M2": dict(res="L")})
    _, txt = callado(A.aciertos_boletos, sal, res)
    assert "1 de 2 jugados; faltan 1." in txt and "M2 (puse EV, salio L)" in txt

    # la revancha se cuenta contra partidos_rev, en su orden
    sal = dict(progol=dict(unico=dict(picks=["L", "E", "V"])), revancha=dict(unico=dict(picks=["V", "L"])),
               partidos=[dict(id=f"P{i}") for i in (1, 2, 3)], partidos_rev=[dict(id="R1"), dict(id="R2")])
    res = dict(partidos={"P1": dict(res="L"), "R1": dict(res="L"), "R2": dict(res="L")})
    _, txt = callado(A.aciertos_boletos, sal, res)
    assert "1 de 1 jugados; faltan 2." in txt and "1 de 2 jugados; faltan 0." in txt
    assert "Fallos: R1 (puse V, salio L)" in txt

    # un boleto con otro numero de picks que partidos es un error, no un conteo corrido
    for picks in (["V"], ["V", "L", "E"]):
        sal["revancha"]["unico"]["picks"] = picks
        try:
            callado(A.aciertos_boletos, sal, res)
        except ValueError:
            pass
        else:
            raise AssertionError(f"falto el ValueError con {len(picks)} picks para 2 partidos")


def prueba_auditoria_2359():
    """La auditoria final del 2359 (21 partidos, concurso cerrado) da las cifras anotadas en la bitacora."""
    tmp = tempfile.mkdtemp()
    antes = os.getcwd()
    try:
        for nombre in ("salida_2359.json", "resultados_2359.json"):
            shutil.copy(os.path.join(AQUI, nombre), tmp)
        os.chdir(tmp)
        sal, res, f = A.cargar("2359")
        assert len(f) == 21
        # las letras guardadas son las de la combinacion oficial de Loteria Nacional
        ofi = res["oficial"]["combinacion_progol"].split() + res["oficial"]["combinacion_revancha"].split()
        assert ["LEV"[x["res"]] for x in f] == ofi
        t, _ = callado(A.tabla_estimadores, f, "2359")
        assert (t["final"]["n"], t["final*"]["n"], t["mercado"]["n"], t["publico"]["n"]) == (21, 19, 19, 21)
        assert (t["final"]["favorito"], t["final"]["con_favorito"]) == (12, 20)
        assert (t["final*"]["favorito"], t["mercado"]["favorito"], t["publico"]["favorito"]) == (11, 12, 12)
        assert cerca(t["final*"]["logloss"], 0.9825, 1e-4) and cerca(t["mercado"]["logloss"], 0.9727, 1e-4)
        assert cerca(t["publico"]["logloss"], 0.9428, 1e-4) and cerca(t["final"]["brier"], 0.5637, 1e-4)
        _, txt = callado(A.aciertos_boletos, sal, res)
        assert "conservador    9 de 14 jugados; faltan 0." in txt and "conservador    6 de 7 jugados; faltan 0." in txt
        assert "agresivo       7 de 14 jugados; faltan 0." in txt
    finally:
        os.chdir(antes)
        shutil.rmtree(tmp)


if __name__ == "__main__":
    for nombre, f in sorted(globals().items()):
        if nombre.startswith("prueba_"):
            f()
            print("ok ", nombre)
