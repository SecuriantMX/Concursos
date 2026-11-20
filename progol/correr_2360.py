"""
Boleto del Progol 2360, version ligera: solo mercado (Shin sobre el promedio del comparador).
Uso: python3 correr_2360.py
"""
import json

import modelo as M
import boletos as B
import concurso_2360 as C

if __name__ == "__main__":
    filas = []
    for p in C.PARTIDOS:
        prob, z = M.shin(p["momios"])
        conf, ic = ("media", 0.05) if p["casas"] >= 3 else ("baja", 0.08)
        filas.append(dict(id=p["id"], local=p["local"], visita=p["visita"], p=prob, ic=ic, conf=conf,
                          comp=dict(mercado=prob, elo=None, poisson=None), pesos=dict(mercado=1.0),
                          det=dict(casas=p["casas"], margen=sum(1 / m for m in p["momios"]) - 1),
                          publico=[100 / 3] * 3, publico_real=False, entropia=M.entropia(prob)))
        print(f"{p['id']:4}{(p['local'] + ' - ' + p['visita'])[:28]:29}{p['casas']:3}  "
              + " ".join(f"{x*100:5.1f}" for x in prob) + f"  {conf}")
    P = [f["p"] for f in filas]
    b = B.mejor_por_probabilidad(P, B.PROGOL, C.TOPE)
    assert B.valido(b, B.PROGOL, C.TOPE)
    r = B.resumen(b, P, B.PROGOL)
    d = B.dist_aciertos(B.cobertura(b, P))
    r["p_10_o_mas"] = sum(d[10:])
    print(f"\nBoleto: {r['dobles']} dobles, {r['triples']} triples, {r['combinaciones']} combinaciones, ${r['costo']}")
    print("   " + "  ".join(f"{i+1}:{x}" for i, x in enumerate(r["picks"])))
    print(f"   P(14)={d[14]*100:.3f}%  P(13)={d[13]*100:.2f}%  P(12)={d[12]*100:.2f}%  P(10 o mas)={r['p_10_o_mas']*100:.1f}%"
          f"  aciertos esperados {sum(B.cobertura(b, P)):.1f}")
    json.dump({"progol": {"recomendado": r}, "revancha": {}, "partidos": filas, "partidos_rev": []},
              open("salida_2360.json", "w"), indent=1, ensure_ascii=False)
