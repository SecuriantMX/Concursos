"""
Pruebas del modelo, del armado de boletos y de la auditoria.
Uso: python3 pruebas.py

Cada bloque cubre un defecto que ya aparecio una vez (revision del 16-nov-2026)
o una propiedad que el resto del codigo da por hecha.
"""
import contextlib
import io
import itertools
import json
import os
import shutil
import tempfile
import warnings

import auditoria as A
import boletos as B
import modelo as M

AQUI = os.path.dirname(os.path.abspath(__file__))


def cerca(a, b, tol=1e-9):
    return abs(a - b) <= tol


def prueba_shin():
    for momios in ([1.16, 6.60, 13.00], [2.30, 3.22, 3.08], [1.02, 21.0, 67.0], [1.90, 1.90]):
        p, z = M.shin(momios)
        assert cerca(sum(p), 1.0, 1e-9) and 0 <= z < 0.2, momios
        # el favorito de los momios sigue siendo el favorito sin margen
        assert p.index(max(p)) == momios.index(min(momios))
    # sin margen no hay nada que quitar
    p, z = M.shin([2.0, 4.0, 4.0])
    assert all(cerca(a, b, 1e-6) for a, b in zip(p, [0.5, 0.25, 0.25])) and z < 1e-6


def prueba_elo():
    # dentro del rango alcanzable, el 1X2 reproduce el We de Elo
    for dr in range(-550, 551, 25):
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
    # la distribucion de aciertos suma 1
    assert cerca(sum(B.dist_aciertos(B.cobertura(b, P))), 1.0, 1e-12)


def prueba_complemento():
    P = [[0.5, 0.3, 0.2]] * 7
    juego = B.REVANCHA
    L, E, V = (0,), (1,), (2,)
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


def prueba_auditoria():
    filas = [dict(id=f"M{i}", local=f"L{i}", visita=f"V{i}", p=[0.5, 0.3, 0.2], conf="alta",
                  comp=dict(mercado=[0.5, 0.3, 0.2], elo=None, poisson=None),
                  publico=[100 / 3] * 3, publico_real=False) for i in range(1, 5)]
    filas[3].update(p=[1 / 3] * 3, conf="nula", comp=dict(mercado=None, elo=None, poisson=None))
    sal = dict(progol=dict(unico=dict(picks=["L", "EV", "LEV", "L"])), revancha={}, partidos=filas, partidos_rev=[])
    res = dict(corte="prueba", partidos={
        "M1": dict(marcador="1-0", res="L"),
        "M2": dict(marcador="2-0", res="L"),      # fuera del doble EV
        "M3": dict(marcador="", res=""),          # sin resultado: no debe contar
        "M4": dict(marcador="0-0", res="E"),
        "M9": dict(marcador="?", res="LE"),       # basura: no debe contar
    })
    tmp = tempfile.mkdtemp()
    antes = os.getcwd()
    try:
        os.chdir(tmp)
        json.dump(sal, open("salida_x.json", "w"))
        json.dump(res, open("resultados_x.json", "w"))
        _, _, f = A.cargar("x")
        assert [x["id"] for x in f] == ["M1", "M2", "M4"]
        assert all(x["publico"] is None for x in f)          # el relleno de 1/3 no es dato del publico
        with contextlib.redirect_stdout(io.StringIO()):
            t = A.tabla_estimadores(f, "prueba")
        assert "publico" not in t and t["final"]["n"] == 3 and t["final*"]["n"] == 2
        assert t["final"]["con_favorito"] == 2                # M4 no tiene favorito
        assert A.favorito([1 / 3] * 3) is None and A.favorito([0.2, 0.5, 0.3]) == 1
        assert A.resultado(None) is None and A.resultado({"res": None}) is None and A.resultado({"res": "V"}) == 2
    finally:
        os.chdir(antes)
        shutil.rmtree(tmp)


def prueba_auditoria_boletos():
    """Los aciertos del boleto se cuentan con los ids de la salida (M1.. en Media Semana)."""
    filas = [dict(id=f"M{i}") for i in range(1, 4)]
    sal = dict(progol=dict(unico=dict(picks=["L", "EV", "LEV"])), revancha={}, partidos=filas, partidos_rev=[])
    res = dict(partidos={"M1": dict(res="L"), "M2": dict(res="L")})
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        A.aciertos_boletos(sal, res)
    assert "1 de 2 jugados; faltan 1." in buf.getvalue() and "M2 (puse EV, salio L)" in buf.getvalue()


if __name__ == "__main__":
    for nombre, f in sorted(globals().items()):
        if nombre.startswith("prueba_"):
            f()
            print("ok ", nombre)
