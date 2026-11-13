"""Corre el modelo y arma los boletos del Progol 2359. Uso: python3 correr_2359.py"""
import json
from math import comb, log, sqrt

import modelo as M
import boletos as B
import concurso_2359 as C

RHO = -0.10  # supuesto del modelo (Dixon-Coles reportan dependencia negativa en marcadores bajos)


def total_goles_muestra():
    """Goles por partido en la muestra de ultimos 10 de las selecciones."""
    g = n = 0
    for p in C.PARTIDOS + C.REVANCHA:
        if "gol" in p:
            a, b, na, c, d, nb = p["gol"]
            g += a + b + c + d
            n += na + nb
    return g / n


TOTAL = total_goles_muestra()


def ventaja_local():
    """Factor de local equivalente a los 100 puntos Elo de eloratings.net."""
    lo, hi = 0.5, 0.9
    we = M.elo_esperado(0, 0, 100)
    for _ in range(60):
        f = (lo + hi) / 2
        p = M.p1x2(TOTAL * f, TOTAL * (1 - f), RHO)
        if p[0] + 0.5 * p[1] < we:
            lo = f
        else:
            hi = f
    return sqrt(f / (1 - f))


VENTAJA = ventaja_local()


def estimar(p):
    comp, det = {"mercado": None, "elo": None, "poisson": None}, {}
    if p["momios"]:
        comp["mercado"], det["margen"], det["casas"] = M.mercado(p["momios"])
    if "elo" in p:
        bono = 0 if p["neutral"] else 100
        comp["elo"], det["we"] = M.elo_1x2(p["elo"][0], p["elo"][1], bono, TOTAL, RHO)
    if "gol" in p:
        a, b, na, c, d, nb = p["gol"]
        media = (a + b + c + d) / (na + nb) / 2
        v = 1.0 if p["neutral"] else VENTAJA
        lh, la = M.lambdas(a / na, b / na, c / nb, d / nb, media, v, na, nb)
        comp["poisson"], det["lambdas"] = M.p1x2(lh, la, RHO), (lh, la)
    elif "xg" in p:
        xl, xal, xv, xav = p["xg"]  # los cortes casa/fuera ya traen la localia
        lh, la = (xl + xav) / 2, (xv + xal) / 2
        comp["poisson"], det["lambdas"] = M.p1x2(lh, la, RHO), (lh, la)
    if all(v is None for v in comp.values()):
        return dict(p=[1 / 3] * 3, comp=comp, det=det, pesos={}, sin_estimacion=True)
    pesos = C.PESOS if p["tipo"] == "seleccion" else {**C.PESOS_CLUB, "elo": 0}
    activos = {k: v for k, v in comp.items() if v is not None and pesos.get(k, 0) > 0}
    if not activos:
        return dict(p=[1 / 3] * 3, comp=comp, det=det, pesos={}, sin_estimacion=True)
    prob, usados = M.mezclar(activos, pesos)
    return dict(p=prob, comp=comp, det=det, pesos=usados, sin_estimacion=False)


def intervalo(e):
    """Medio ancho del intervalo: dispersion entre estimadores, con piso segun calidad."""
    vals = [e["comp"][k] for k in e["pesos"]]
    if e["sin_estimacion"]:
        return 0.20, "nula"
    disp = max(max(v[i] for v in vals) - min(v[i] for v in vals) for i in range(3)) if len(vals) > 1 else 0
    casas = e["det"].get("casas", 0)
    if casas >= 2 and len(vals) >= 2:
        conf, piso = "alta", 0.03
    elif casas >= 1:
        conf, piso = "media", 0.05
    else:
        conf, piso = "baja", 0.08
    return max(piso, disp / 2), conf


def estimar_N():
    """
    Combinaciones jugadas por el publico, a partir de los ganadores del 2358.
    Si cada combinacion acierta un partido con probabilidad q, el cociente entre
    ganadores de k y k+1 aciertos da q, y el conteo de un nivel da N.
    """
    g = C.GANADORES_2358
    qs = []
    for k in (10, 11, 12):
        x = g[k] / g[k + 1] * (14 - k) / (k + 1)  # (1-q)/q
        qs.append(1 / (1 + x))
    q = sum(qs) / len(qs)
    ns = [g[k] / (comb(14, k) * q ** k * (1 - q) ** (14 - k)) for k in (10, 11, 12)]
    return q, sum(ns) / len(ns), ns


def tabla(partidos, titulo):
    print(f"\n{titulo}")
    print(f"{'':4}{'partido':34}{'mercado':>17}{'elo':>17}{'poisson':>17}{'FINAL L/E/V':>19}  ±   conf  entropia  justo L/E/V")
    filas = []
    for p in partidos:
        e = estimar(p)
        ic, conf = intervalo(e)
        f = lambda v: "      -          " if v is None else f"{v[0]*100:5.1f}{v[1]*100:5.1f}{v[2]*100:5.1f}  "
        pr = e["p"]
        just = " ".join(f"{1/x:5.2f}" for x in pr)
        print(f"{p['id']:4}{(p['local']+' - '+p['visita'])[:33]:34}{f(e['comp']['mercado'])}{f(e['comp']['elo'])}"
              f"{f(e['comp']['poisson'])}  {pr[0]*100:5.1f}{pr[1]*100:5.1f}{pr[2]*100:5.1f} {ic*100:4.0f}  {conf:5} {M.entropia(pr):6.2f}   {just}")
        filas.append(dict(id=p["id"], local=p["local"], visita=p["visita"], p=pr, ic=ic, conf=conf,
                          comp=e["comp"], pesos=e["pesos"], det=e["det"], publico=p["publico"],
                          entropia=M.entropia(pr)))
    return filas


def mostrar(nombre, b, P, juego, Q, N, ids):
    r = B.resumen(b, P, juego, Q, N)
    print(f"\n  {nombre}: {r['dobles']} dobles, {r['triples']} triples, {r['combinaciones']} combinaciones, ${r['costo']}")
    print("   " + "  ".join(f"{i}:{x}" for i, x in zip(ids, r["picks"])))
    n = len(P)
    print(f"   P({n})={r['p_todos']*100:.4f}%  P({n-1})={r['p_n_menos_1']*100:.3f}%  P({n-2})={r['p_n_menos_2']*100:.2f}%"
          f"  fraccion esperada de bolsa={r['valor_bolsa']:.3e}")
    return r


if __name__ == "__main__":
    print(f"goles por partido en la muestra: {TOTAL:.2f}   factor de local: {VENTAJA:.3f}   rho: {RHO}")
    fp = tabla(C.PARTIDOS, "PROGOL 2359")
    fr = tabla(C.REVANCHA, "REVANCHA 2359")

    q, N, ns = estimar_N()
    print(f"\nPublico 2358: acierto medio por partido q={q:.3f}; combinaciones jugadas N≈{N/1e6:.2f} M "
          f"(por nivel: {', '.join(f'{x/1e6:.2f}' for x in ns)})")

    P = [f["p"] for f in fp]
    Q = [[x / 100 for x in f["publico"]] for f in fp]
    ids = [f["id"][1:] for f in fp]
    print("\nValor contra el publico (probabilidad / porcentaje de venta), mayor que 1 = poco jugado:")
    for f in fp + fr:
        r = [f["p"][i] / (f["publico"][i] / 100) for i in range(3)]
        print(f"  {f['id']:4}{f['local'][:16]:17} L {r[0]:4.2f}  E {r[1]:4.2f}  V {r[2]:4.2f}")

    salida = {"progol": {}, "revancha": {}, "N": N}
    # Revancha: se reserva su costo dentro del tope
    PR = [f["p"] for f in fr]
    QR = [[x / 100 for x in f["publico"]] for f in fr]
    idr = [f["id"][1:] for f in fr]
    NR = N  # no hay dato de venta de Revancha; se usa el mismo orden de magnitud

    SIN_EST = [i for i, p in enumerate(C.PARTIDOS) if estimar(p)["sin_estimacion"]]
    print("\nBOLETOS PROGOL (tope Progol+Revancha $%d)" % C.TOPE)
    for nombre, tope_p, tope_r, piso in (("conservador", 960, 120, None), ("balanceado", 960, 120, 0.6),
                                         ("agresivo", 960, 120, 0.4)):
        base = B.mejor_por_probabilidad(P, B.PROGOL, tope_p)
        pmax = B.prod(B.cobertura(base, P))
        b = base if piso is None else B.mejor_por_valor(P, Q, N, B.PROGOL, tope_p, piso * pmax, SIN_EST)
        salida["progol"][nombre] = mostrar(nombre, b, P, B.PROGOL, Q, N, ids)
        for esc in (N / 2, N * 2):
            print(f"      con N={esc/1e6:.1f} M: fraccion esperada {B.valor_esperado(b, P, Q, esc):.3e}"
                  f" -> premio esperado de 1er lugar ${B.valor_esperado(b, P, Q, esc)*C.BOLSA:,.0f}")
        print(f"      premio esperado de 1er lugar (N estimado): ${salida['progol'][nombre]['valor_bolsa']*C.BOLSA:,.0f}")
        baser = B.mejor_por_probabilidad(PR, B.REVANCHA, tope_r)
        pmaxr = B.prod(B.cobertura(baser, PR))
        br = baser if piso is None else B.mejor_por_valor(PR, QR, NR, B.REVANCHA, tope_r, piso * pmaxr)
        salida["revancha"][nombre] = mostrar("revancha " + nombre, br, PR, B.REVANCHA, QR, NR, idr)

    alt = B.mejor_por_probabilidad(P, B.PROGOL, 1080)
    salida["progol"]["alterno_1080"] = mostrar("alterno max probabilidad con $1,080", alt, P, B.PROGOL, Q, N, ids)
    altr = B.mejor_por_probabilidad(PR, B.REVANCHA, 20)
    salida["revancha"]["alterno_20"] = mostrar("revancha con $20", altr, PR, B.REVANCHA, QR, NR, idr)

    print("\nPLAYDOIT: valor esperado = probabilidad propia x momio - 1; Kelly 1/4")
    por_id = {f["id"]: f for f in fp + fr}
    salida["playdoit"] = []
    for pid, m in C.PLAYDOIT.items():
        f = por_id[pid]
        for i, et in enumerate(("L", "E", "V")):
            o, p = m["1x2"][i], f["p"][i]
            ev = p * o - 1
            p_min = p - f["ic"]            # probabilidad en el borde bajo del intervalo
            ev_min = p_min * o - 1
            kelly = max(0.0, (p * o - 1) / (o - 1)) / 4
            marca = "APOSTABLE" if ev_min > 0 else ("ev+ pero dentro del error" if ev > 0 else "")
            print(f"  {pid:3} {f['local'][:10]:10}-{f['visita'][:10]:10} {et} momio {o:5.2f} p={p*100:5.1f}% "
                  f"EV={ev*100:+6.1f}%  EV(p-ic)={ev_min*100:+6.1f}%  kelly/4={kelly*100:4.1f}%  {marca}")
            salida["playdoit"].append(dict(id=pid, pick=et, momio=o, p=p, ev=ev, ev_min=ev_min, kelly4=kelly))

    salida["partidos"] = fp
    salida["partidos_rev"] = fr
    json.dump(salida, open("salida_2359.json", "w"), indent=1, ensure_ascii=False)
