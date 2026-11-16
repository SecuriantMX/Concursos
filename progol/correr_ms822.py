"""Corre el modelo y arma el boleto de Media Semana 822. Uso: python3 correr_ms822.py"""
import json
import modelo as M
import boletos as B
import concurso_ms822 as C

TOTAL = 2.81  # goles por partido de la muestra de selecciones usada en el 2359

filas = []
print(f"{'':4}{'partido':26}{'mercado':>16}{'elo':>16}{'FINAL L/E/V':>18}   ±  conf   justo L/E/V")
for p in C.PARTIDOS:
    m = M.mercado(p["momios"])[0] if p["momios"] else None
    e = M.elo_1x2(p["elo"][0], p["elo"][1], 100, TOTAL)[0] if "elo" in p else None
    comp = {k: v for k, v in (("mercado", m), ("elo", e)) if v is not None}
    if comp:
        f, w = M.mezclar(comp, C.PESOS)
        disp = max(abs(m[i] - e[i]) for i in range(3)) / 2 if m and e else 0
        ic, conf = (max(0.05, disp), "media") if m else (0.08, "baja")
    else:
        f, w, ic, conf = [1 / 3] * 3, {}, 0.20, "nula"
    fmt = lambda v: "       -        " if v is None else f"{v[0]*100:5.1f}{v[1]*100:5.1f}{v[2]*100:5.1f} "
    print(f"{p['id']:4}{(p['local'] + ' - ' + p['visita'])[:25]:26}{fmt(m)}{fmt(e)} {f[0]*100:5.1f}{f[1]*100:5.1f}{f[2]*100:5.1f}"
          f"  {ic*100:3.0f}  {conf:5}  " + " ".join(f"{1/x:5.2f}" for x in f))
    filas.append(dict(id=p["id"], local=p["local"], visita=p["visita"], p=f, ic=ic, conf=conf,
                      comp={"mercado": m, "elo": e, "poisson": None}, pesos=w, det={},
                      publico=[100 / 3] * 3, entropia=M.entropia(f)))

P = [f["p"] for f in filas]
ids = [f["id"][1:] for f in filas]
salida = {"progol": {}, "revancha": {}, "partidos": filas, "partidos_rev": [], "N": None}
for nombre, tope in (("recomendado_tope_1000", C.TOPE), ("maximo_1080", 1080)):
    b = B.mejor_por_probabilidad(P, C.MEDIA_SEMANA, tope)
    r = B.resumen(b, P, C.MEDIA_SEMANA)
    salida["progol"][nombre] = r
    print(f"\n{nombre}: {r['dobles']} dobles, {r['triples']} triples, {r['combinaciones']} combinaciones, ${r['costo']}")
    print("   " + "  ".join(f"{i}:{x}" for i, x in zip(ids, r["picks"])))
    print(f"   P(9)={r['p_todos']*100:.2f}%  P(8)={r['p_n_menos_1']*100:.2f}%  P(7)={r['p_n_menos_2']*100:.2f}%")
json.dump(salida, open("salida_ms822.json", "w"), indent=1, ensure_ascii=False)
