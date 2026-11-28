"""
Corre el modelo y arma el boleto del Progol 2361 (modo completo).
Uso: python3 correr_2361.py

Lee concurso_2361.py (entradas con fuente) y escribe salida_2361.json.
Mismo esquema que correr_ms822.py:
  mercado  momios de cada casa sin margen (Shin), promediados
  elo      solo selecciones varoniles con rating en eloratings.net
  poisson  solo clubes con xG de casa y de visita de la misma competencia
           y muestra de al menos MIN_XG partidos por lado
"""
import json

import modelo as M
import boletos as B
import concurso_2361 as C

RHO = -0.10


def estimar(p):
    comp = {"mercado": None, "elo": None, "poisson": None}
    det = {}
    if p.get("momios"):
        comp["mercado"], det["margen"], det["casas"] = M.mercado([m[:3] for m in p["momios"]])
    if p.get("elo"):
        bono = 0 if p.get("neutral") else 100
        comp["elo"], det["we"] = M.elo_1x2(p["elo"][0], p["elo"][1], bono, C.GOLES_ELO, RHO)
    if p.get("xg"):
        if min(p.get("xg_n", (0, 0))) >= C.MIN_XG:
            xl, xal, xv, xav = p["xg"]  # local en casa a favor / en contra, visita fuera a favor / en contra
            lh, la = (xl + xav) / 2, (xv + xal) / 2
            comp["poisson"], det["lambdas"] = M.p1x2(lh, la, RHO), [lh, la]
        else:
            det["xg_fuera"] = f"muestra de {min(p.get('xg_n', (0, 0)))} partidos, minimo {C.MIN_XG}"
    pesos = C.PESOS_SELECCION if p["tipo"] == "seleccion" else C.PESOS_CLUB
    activos = {k: v for k, v in comp.items() if v is not None and pesos.get(k, 0) > 0}
    if not activos:
        return dict(p=[1 / 3] * 3, comp=comp, det=det, pesos={}, ic=0.20, conf="nula")
    prob, usados = M.mezclar(activos, pesos)
    vals = list(activos.values())
    disp = max(max(v[i] for v in vals) - min(v[i] for v in vals) for i in range(3)) / 2 if len(vals) > 1 else 0.0
    casas = det.get("casas", 0)
    if casas >= 3:
        conf, piso = "alta", 0.03
    elif casas >= 1:
        conf, piso = "media", 0.05
    else:
        conf, piso = "baja", 0.08
    return dict(p=prob, comp=comp, det=det, pesos=usados, ic=max(piso, disp), conf=conf)


def pct(v):
    return "       -        " if v is None else f"{v[0]*100:5.1f}{v[1]*100:5.1f}{v[2]*100:5.1f} "


def describir(b, P, ids, nombre):
    r = B.resumen(b, P, B.PROGOL)
    c = B.cobertura(b, P)
    d = B.dist_aciertos(c)
    r["p_10_o_mas"] = sum(d[10:])
    r["esperados"] = sum(c)
    print(f"\n{nombre} (tope ${C.TOPE}): {r['dobles']} dobles, {r['triples']} triples, {r['combinaciones']} combinaciones, ${r['costo']}")
    print("   " + "  ".join(f"{i}:{x}" for i, x in zip(ids, r["picks"])))
    print(f"   P(14)={d[14]*100:.3f}%  P(13)={d[13]*100:.2f}%  P(12)={d[12]*100:.2f}%  P(10 o mas)={r['p_10_o_mas']*100:.1f}%"
          f"  aciertos esperados {r['esperados']:.2f}")
    print("   cobertura por partido: " + "  ".join(f"{i}:{x*100:.0f}%" for i, x in zip(ids, c)))
    return r


if __name__ == "__main__":
    filas = []
    print(f"{'':4}{'partido':27}{'casas':>5} {'mercado':>15}{'elo':>16}{'poisson':>16}{'FINAL L/E/V':>17}   ±  conf")
    for p in C.PARTIDOS:
        e = estimar(p)
        f = e["p"]
        print(f"{p['id']:4}{(p['local'] + ' - ' + p['visita'])[:26]:27}{e['det'].get('casas', 0):5} "
              f"{pct(e['comp']['mercado'])}{pct(e['comp']['elo'])}{pct(e['comp']['poisson'])}"
              f"{f[0]*100:5.1f}{f[1]*100:5.1f}{f[2]*100:5.1f}  {e['ic']*100:3.0f}  {e['conf']}")
        pub = p.get("publico")
        hay_pub = bool(pub) and sum(pub) > 0  # porcentajes oficiales de venta; en ceros o ausentes no son dato
        filas.append(dict(id=p["id"], local=p["local"], visita=p["visita"], p=f, ic=e["ic"], conf=e["conf"],
                          comp=e["comp"], pesos=e["pesos"], det=e["det"],
                          publico=pub if hay_pub else [100 / 3] * 3, publico_real=hay_pub,
                          entropia=M.entropia(f)))

    P = [f["p"] for f in filas]
    ids = [f["id"][1:] for f in filas]

    if all(f["publico_real"] for f in filas):
        print("\nProbabilidad propia entre porcentaje de venta (mayor que 1 = poco jugado por el publico):")
        for f in filas:
            r = [f["p"][i] / max(f["publico"][i] / 100, 1e-9) for i in range(3)]
            print(f"  {f['id']:4}{f['local'][:14]:15} L {r[0]:4.2f}  E {r[1]:4.2f}  V {r[2]:4.2f}"
                  f"   publico {f['publico'][0]:.0f}/{f['publico'][1]:.0f}/{f['publico'][2]:.0f}")

    # boleto: el de mayor probabilidad de 14 aciertos que cabe en el tope. Se comprobo el 22-nov
    # que es el mismo que maximiza llegar a 10, 11 o 12.
    b = B.mejor_por_probabilidad(P, B.PROGOL, C.TOPE)
    assert B.valido(b, B.PROGOL, C.TOPE)
    assert all(len(b[i]) == 3 for i, f in enumerate(filas) if f["conf"] == "nula"), "partido sin estimacion sin triple"
    r = describir(b, P, ids, "Boleto")

    # el mismo armado usando solo el mercado, para ver cuanto mueve el Poisson
    Pm = [f["comp"]["mercado"] or f["p"] for f in filas]
    bm = B.mejor_por_probabilidad(Pm, B.PROGOL, C.TOPE)
    rm = describir(bm, Pm, ids, "Boleto solo mercado")
    print("   evaluado con las probabilidades finales: "
          f"P(14)={B.prod(B.cobertura(bm, P))*100:.3f}%  (el boleto final da {B.prod(B.cobertura(b, P))*100:.3f}%)")

    # cuanto cambia P(14) si cada partido cae en el borde malo o bueno de su intervalo
    lo = hi = 1.0
    for i, f in enumerate(filas):
        if len(b[i]) == 3:
            continue
        c = sum(f["p"][o] for o in b[i])
        lo *= max(0.01, c - f["ic"])
        hi *= min(0.99, c + f["ic"])
    print(f"   P(14) con todos los partidos en el borde de su intervalo: {lo*100:.3f}% a {hi*100:.3f}%")

    salida = {"progol": {"recomendado": r}, "revancha": {}, "partidos": filas, "partidos_rev": [],
              "solo_mercado": rm, "sensibilidad_p14": [lo, hi]}
    json.dump(salida, open("salida_2361.json", "w"), indent=1, ensure_ascii=False)
