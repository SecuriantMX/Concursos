"""
Auditoria: lo que se propuso contra lo que resulto.

Uso:  python3 auditoria.py 2359

Lee salida_<n>.json (lo que el modelo dijo antes del cierre) y
resultados_<n>.json (marcadores con fuente). Calcula Brier y log-loss de cada
estimador, cuenta aciertos de cada boleto, y vuelve a escribir historial.csv,
que acumula un renglon por partido jugado de todos los concursos.

Los pesos de la mezcla NO se cambian con un solo concurso. La funcion
revisar_pesos() solo propone un cambio cuando el historial junta suficientes
partidos (MIN_PARTIDOS) y la mejora en log-loss es mayor que su error estandar.
"""
import csv
import glob
import json
import sys
import warnings
from math import log, sqrt

LETRAS = "LEV"
MIN_PARTIDOS = 60       # partidos con mercado y Elo antes de tocar pesos
EPS = 1e-6


def brier(p, r):
    return sum((p[i] - (1.0 if i == r else 0.0)) ** 2 for i in range(3))


def logloss(p, r):
    return -log(max(p[r], EPS))


def resultado(r):
    """Indice 0, 1 o 2 del resultado; None si el partido no trae exactamente L, E o V."""
    res = r.get("res") if isinstance(r, dict) else None
    return LETRAS.index(res) if res in ("L", "E", "V") else None


def leer(ruta):
    with open(ruta) as fh:
        return json.load(fh)


def cargar(n):
    sal = leer(f"salida_{n}.json")
    res = leer(f"resultados_{n}.json")
    filas = []
    ids = {f["id"] for f in sal["partidos"] + sal["partidos_rev"]}
    ajenas = [k for k in res["partidos"] if k not in ids]
    if ajenas:
        warnings.warn(f"resultados_{n}.json trae claves que no son partidos de salida_{n}.json y no se cuentan: "
                      + ", ".join(ajenas))
    for f in sal["partidos"] + sal["partidos_rev"]:
        r = res["partidos"].get(f["id"])
        k = resultado(r)
        if k is None:
            # sin resultado todavia es normal; un resultado escrito que no es L, E o V es un error de captura
            if isinstance(r, dict) and r.get("res") not in (None, ""):
                warnings.warn(f"resultados_{n}.json: {f['id']} trae res={r.get('res')!r}; debe ser L, E o V. No se cuenta.")
            continue
        # el publico solo cuenta si es el porcentaje oficial; el relleno de 1/3 no es un dato
        pub = None
        if f.get("publico_real", True) and sum(f["publico"]) > 0:
            s = sum(f["publico"])
            pub = [x / s for x in f["publico"]]
        filas.append(dict(concurso=n, id=f["id"], local=f["local"], visita=f["visita"],
                          res=k, marcador=r["marcador"], conf=f["conf"],
                          final=f["p"], mercado=f["comp"].get("mercado"), elo=f["comp"].get("elo"),
                          poisson=f["comp"].get("poisson"), publico=pub))
    return sal, res, filas


def favorito(p):
    """Indice del resultado mas probable, o None si hay empate en el maximo (no hay favorito)."""
    m = max(p)
    idx = [i for i in range(3) if m - p[i] < 1e-9]
    return idx[0] if len(idx) == 1 else None


def tabla_estimadores(filas, titulo):
    print(f"\n{titulo}")
    print(f"  {'estimador':10}{'n':>4}{'Brier':>9}{'log-loss':>10}{'acierto del favorito':>23}")
    out = {}
    con_mercado = [f for f in filas if f["mercado"] is not None]
    renglones = [("final", "final", filas)]
    if 0 < len(con_mercado) < len(filas):
        # mismo conjunto que el mercado: asi los dos renglones si se pueden restar
        renglones.append(("final*", "final", con_mercado))
    renglones += [(e, e, filas) for e in ("mercado", "elo", "poisson", "publico")]
    for nombre, est, base in renglones:
        fs = [f for f in base if f[est] is not None]
        if not fs:
            continue
        b = sum(brier(f[est], f["res"]) for f in fs) / len(fs)
        ll = sum(logloss(f[est], f["res"]) for f in fs) / len(fs)
        con_fav = [f for f in fs if favorito(f[est]) is not None]
        fav = sum(favorito(f[est]) == f["res"] for f in con_fav)
        print(f"  {nombre:10}{len(fs):4}{b:9.3f}{ll:10.3f}{fav:>14} de {len(con_fav)}")
        out[nombre] = dict(n=len(fs), brier=b, logloss=ll, favorito=fav, con_favorito=len(con_fav))
    print(f"  {'al azar':10}{'':4}{2/3:9.3f}{log(3):10.3f}")
    if 0 < len(con_mercado) < len(filas):
        print("  final* = modelo final solo en los partidos que tienen mercado. El favorito no cuenta"
              " donde el estimador empata en el maximo.")
    return out


def cara_a_cara(filas):
    """Modelo final contra mercado, solo en los partidos donde hay mercado."""
    fs = [f for f in filas if f["mercado"] is not None]
    if not fs:
        return None
    d = [logloss(f["mercado"], f["res"]) - logloss(f["final"], f["res"]) for f in fs]
    m = sum(d) / len(d)
    ee = sqrt(sum((x - m) ** 2 for x in d) / (len(d) - 1) / len(d)) if len(d) > 1 else float("nan")
    return dict(n=len(d), ventaja=m, error=ee)


def aciertos_boletos(sal, res):
    print("\nBoletos (aciertos sobre partidos ya jugados)")
    for juego, lista in (("progol", sal["partidos"]), ("revancha", sal["partidos_rev"])):
        ids = [f["id"] for f in lista]
        for nombre, b in sal[juego].items():
            if len(b["picks"]) != len(ids):
                raise ValueError(f"el boleto {juego}/{nombre} trae {len(b['picks'])} picks para {len(ids)} partidos")
            ok = jug = 0
            fallos = []
            for pid, pick in zip(ids, b["picks"]):
                k = resultado(res["partidos"].get(pid))
                if k is None:
                    continue
                jug += 1
                if LETRAS[k] in pick:
                    ok += 1
                else:
                    fallos.append(f"{pid} (puse {pick}, salio {LETRAS[k]})")
            print(f"  {juego:9}{nombre:14} {ok} de {jug} jugados; faltan {len(b['picks']) - jug}."
                  + (f"  Fallos: {', '.join(fallos)}" if fallos else ""))


def escribir_historial():
    """Reconstruye historial.csv desde todos los concursos con resultados."""
    todas = []
    for ruta in sorted(glob.glob("resultados_*.json")):
        n = ruta.split("_")[1].split(".")[0]
        try:
            todas += cargar(n)[2]
        except FileNotFoundError:
            pass
    with open("historial.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["concurso", "id", "local", "visita", "marcador", "resultado", "confianza"]
                   + [f"{e}_{x}" for e in ("final", "mercado", "elo", "poisson", "publico") for x in LETRAS])
        for f in todas:
            fila = [f["concurso"], f["id"], f["local"], f["visita"], f["marcador"], LETRAS[f["res"]], f["conf"]]
            for e in ("final", "mercado", "elo", "poisson", "publico"):
                fila += [""] * 3 if f[e] is None else [f"{x:.4f}" for x in f[e]]
            w.writerow(fila)
    return todas


def revisar_pesos(todas):
    """Busca el peso del Elo que minimiza el log-loss del historial. Solo propone con muestra suficiente."""
    fs = [f for f in todas if f["mercado"] is not None and f["elo"] is not None]
    print(f"\nRevision de pesos mercado/Elo: {len(fs)} partidos en el historial (minimo {MIN_PARTIDOS}).")
    if len(fs) < MIN_PARTIDOS:
        print("  Muestra insuficiente: los pesos se quedan como estan.")
        return None

    def ll(w):
        return sum(logloss([(1 - w) * f["mercado"][i] + w * f["elo"][i] for i in range(3)], f["res"]) for f in fs) / len(fs)

    mejor = min((w / 20 for w in range(0, 13)), key=ll)
    d = [logloss([0.75 * f["mercado"][i] + 0.25 * f["elo"][i] for i in range(3)], f["res"])
         - logloss([(1 - mejor) * f["mercado"][i] + mejor * f["elo"][i] for i in range(3)], f["res"]) for f in fs]
    m = sum(d) / len(d)
    ee = sqrt(sum((x - m) ** 2 for x in d) / (len(d) - 1) / len(d))
    print(f"  Peso de Elo con menor log-loss: {mejor:.2f} (actual 0.25). Mejora {m:.4f} ± {ee:.4f}.")
    if m > 2 * ee:
        print("  La mejora supera dos errores estandar: se justifica cambiar el peso.")
        return mejor
    print("  La mejora no se distingue del ruido: los pesos se quedan como estan.")
    return None


if __name__ == "__main__":
    n = sys.argv[1]
    sal, res, filas = cargar(n)
    total = len(sal["partidos"]) + len(sal["partidos_rev"])
    print(f"Concurso {n}: {len(filas)} de {total} partidos con resultado (corte: {res.get('corte', '?')})")
    for f in filas:
        fav = favorito(f["final"])
        motivo = "sin estimacion" if f["conf"] == "nula" else "empate en el maximo"
        mio = f"sin favorito ({motivo})" if fav is None else f"favorito mio {LETRAS[fav]} ({f['final'][fav] * 100:.0f}%)"
        print(f"  {f['id']:4}{(f['local'] + ' - ' + f['visita'])[:34]:35}{f['marcador']:>5}  salio {LETRAS[f['res']]}"
              f"  le daba {f['final'][f['res']] * 100:4.1f}%  {mio}")
    if filas:
        tabla_estimadores(filas, "Este concurso")
        c = cara_a_cara(filas)
        if c:
            print(f"\n  Modelo final contra mercado en {c['n']} partidos: ventaja de log-loss {c['ventaja']:+.4f} ± {c['error']:.4f}"
                  " (positivo = el modelo fue mejor)")
    aciertos_boletos(sal, res)
    todas = escribir_historial()
    if len({f["concurso"] for f in todas}) > 1:
        tabla_estimadores(todas, "Historial acumulado")
    revisar_pesos(todas)
