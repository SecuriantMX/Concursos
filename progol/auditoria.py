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
from math import log, sqrt

LETRAS = "LEV"
MIN_PARTIDOS = 60       # partidos con mercado y Elo antes de tocar pesos
EPS = 1e-6


def brier(p, r):
    return sum((p[i] - (1.0 if i == r else 0.0)) ** 2 for i in range(3))


def logloss(p, r):
    return -log(max(p[r], EPS))


def cargar(n):
    sal = json.load(open(f"salida_{n}.json"))
    res = json.load(open(f"resultados_{n}.json"))
    filas = []
    for f in sal["partidos"] + sal["partidos_rev"]:
        r = res["partidos"].get(f["id"])
        if not r or r.get("res") not in LETRAS:
            continue
        pub = [x / 100 for x in f["publico"]]
        s = sum(pub)
        filas.append(dict(concurso=n, id=f["id"], local=f["local"], visita=f["visita"],
                          res=LETRAS.index(r["res"]), marcador=r["marcador"], conf=f["conf"],
                          final=f["p"], mercado=f["comp"].get("mercado"), elo=f["comp"].get("elo"),
                          poisson=f["comp"].get("poisson"), publico=[x / s for x in pub]))
    return sal, res, filas


def tabla_estimadores(filas, titulo):
    print(f"\n{titulo}")
    print(f"  {'estimador':10}{'n':>4}{'Brier':>9}{'log-loss':>10}{'acierto del favorito':>23}")
    out = {}
    for est in ("final", "mercado", "elo", "poisson", "publico"):
        fs = [f for f in filas if f[est] is not None]
        if not fs:
            continue
        b = sum(brier(f[est], f["res"]) for f in fs) / len(fs)
        ll = sum(logloss(f[est], f["res"]) for f in fs) / len(fs)
        fav = sum(max(range(3), key=lambda i: f[est][i]) == f["res"] for f in fs)
        print(f"  {est:10}{len(fs):4}{b:9.3f}{ll:10.3f}{fav:>14} de {len(fs)}")
        out[est] = dict(n=len(fs), brier=b, logloss=ll, favorito=fav)
    print(f"  {'al azar':10}{'':4}{2/3:9.3f}{log(3):10.3f}")
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
    for juego, pref in (("progol", "P"), ("revancha", "R")):
        for nombre, b in sal[juego].items():
            ok = jug = 0
            fallos = []
            for i, pick in enumerate(b["picks"], 1):
                r = res["partidos"].get(f"{pref}{i}")
                if not r or r.get("res") not in LETRAS:
                    continue
                jug += 1
                if r["res"] in pick:
                    ok += 1
                else:
                    fallos.append(f"{pref}{i} (puse {pick}, salio {r['res']})")
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
        fav = max(range(3), key=lambda i: f["final"][i])
        print(f"  {f['id']:4}{(f['local'] + ' - ' + f['visita'])[:34]:35}{f['marcador']:>5}  salio {LETRAS[f['res']]}"
              f"  le daba {f['final'][f['res']] * 100:4.1f}%  favorito mio {LETRAS[fav]} ({f['final'][fav] * 100:.0f}%)")
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
