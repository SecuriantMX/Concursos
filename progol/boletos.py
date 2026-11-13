"""
Armado de boletos para Progol y Revancha.

Reglas de multiples tomadas de la tabla oficial de Loteria Nacional
(loterianacional.gob.mx/Progol/Coperacha, consultada el 13-nov-2026):
  Progol: sencilla $15; hasta 8 dobles, hasta 5 triples y las combinaciones
          que aparecen en la tabla (por triples: 0->8 dobles, 1->6, 2->5, 3->3, 4->2, 5->0).
  Revancha: sencilla $5; hasta 3 dobles y 2 triples.
"""
from itertools import combinations, product
from math import exp
import random

PROGOL = {"precio": 15, "max_dobles": {0: 8, 1: 6, 2: 5, 3: 3, 4: 2, 5: 0}}
REVANCHA = {"precio": 5, "max_dobles": {0: 3, 1: 3, 2: 3}}

OPC = [(0,), (1,), (2,), (0, 1), (0, 2), (1, 2), (0, 1, 2)]  # indices L=0, E=1, V=2
LETRA = "LEV"


def costo(boleto, juego):
    return juego["precio"] * prod(len(s) for s in boleto)


def prod(xs):
    r = 1
    for x in xs:
        r *= x
    return r


def valido(boleto, juego, presupuesto):
    t = sum(len(s) == 3 for s in boleto)
    d = sum(len(s) == 2 for s in boleto)
    if t not in juego["max_dobles"] or d > juego["max_dobles"][t]:
        return False
    return costo(boleto, juego) <= presupuesto


def cobertura(boleto, P):
    return [sum(P[i][o] for o in s) for i, s in enumerate(boleto)]


def dist_aciertos(c):
    """Distribucion del numero de partidos cubiertos (Poisson-binomial)."""
    d = [1.0]
    for p in c:
        n = [0.0] * (len(d) + 1)
        for k, v in enumerate(d):
            n[k] += v * (1 - p)
            n[k + 1] += v * p
        d = n
    return d


def mejor_por_probabilidad(P, juego, presupuesto):
    """Boleto que maximiza la probabilidad de acertar todo. Busqueda exhaustiva."""
    n = len(P)
    orden = [sorted(range(3), key=lambda o: -P[i][o]) for i in range(n)]
    mejor, mejor_p = None, -1
    for t, dmax in juego["max_dobles"].items():
        for d in range(dmax + 1):
            if juego["precio"] * 3 ** t * 2 ** d > presupuesto or t + d > n:
                continue
            for trip in combinations(range(n), t):
                resto = [i for i in range(n) if i not in trip]
                # con los triples fijos, los dobles van donde mas sube la cobertura
                gan = sorted(resto, key=lambda i: -(P[i][orden[i][0]] + P[i][orden[i][1]]) / P[i][orden[i][0]])
                dob = set(gan[:d])
                b = []
                for i in range(n):
                    if i in trip:
                        b.append((0, 1, 2))
                    elif i in dob:
                        b.append(tuple(sorted(orden[i][:2])))
                    else:
                        b.append((orden[i][0],))
                p = prod(cobertura(b, P))
                if p > mejor_p:
                    mejor, mejor_p = b, p
    return mejor


def valor_esperado(boleto, P, Q, N):
    """
    Fraccion esperada de la bolsa de primer lugar que cobra el boleto.
    Cada combinacion c gana con prob P(c); la bolsa se reparte entre 1 + K
    ganadores, K ~ Poisson(N*Q(c)), Q(c) = fraccion del publico con esa
    combinacion. E[1/(1+K)] = (1 - e^-m)/m con m = N*Q(c).
    """
    total = 0.0
    for c in product(*boleto):
        p = prod(P[i][o] for i, o in enumerate(c))
        m = N * prod(Q[i][o] for i, o in enumerate(c))
        total += p * ((1 - exp(-m)) / m if m > 1e-9 else 1.0)
    return total


def mejor_por_valor(P, Q, N, juego, presupuesto, piso_prob=0.0, semilla=7, reinicios=30):
    """
    Busqueda local: maximiza el valor esperado de la bolsa de primer lugar
    sujeto a que la probabilidad de acertar todo no baje de piso_prob.
    """
    rng = random.Random(semilla)
    base = mejor_por_probabilidad(P, juego, presupuesto)
    n = len(P)

    def puntaje(b):
        if prod(cobertura(b, P)) < piso_prob:
            return -1.0
        return valor_esperado(b, P, Q, N)

    mejor, mejor_v = base, puntaje(base)
    for r in range(reinicios):
        b = list(base)
        if r:  # perturbar el punto de partida
            for i in rng.sample(range(n), 3):
                cand = [o for o in OPC if len(o) == len(b[i])]
                b[i] = rng.choice(cand)
            if not valido(b, juego, presupuesto):
                b = list(base)
        v = puntaje(b)
        mejora = True
        while mejora:
            mejora = False
            idx = list(range(n))
            rng.shuffle(idx)
            for i in idx:  # cambiar un partido
                for o in OPC:
                    if o == b[i]:
                        continue
                    nb = b[:i] + [o] + b[i + 1:]
                    if valido(nb, juego, presupuesto):
                        nv = puntaje(nb)
                        if nv > v + 1e-15:
                            b, v, mejora = nb, nv, True
            for i, j in combinations(range(n), 2):  # mover un doble/triple de partido
                if len(b[i]) == len(b[j]):
                    continue
                for oi in (o for o in OPC if len(o) == len(b[j])):
                    for oj in (o for o in OPC if len(o) == len(b[i])):
                        nb = list(b)
                        nb[i], nb[j] = oi, oj
                        nv = puntaje(nb)
                        if nv > v + 1e-15:
                            b, v, mejora = nb, nv, True
        if v > mejor_v:
            mejor, mejor_v = b, v
    return mejor


def texto(boleto):
    return ["".join(LETRA[o] for o in s) for s in boleto]


def resumen(boleto, P, juego, Q=None, N=None):
    c = cobertura(boleto, P)
    d = dist_aciertos(c)
    n = len(P)
    r = {
        "picks": texto(boleto),
        "dobles": sum(len(s) == 2 for s in boleto),
        "triples": sum(len(s) == 3 for s in boleto),
        "combinaciones": prod(len(s) for s in boleto),
        "costo": costo(boleto, juego),
        "p_todos": d[n],
        "p_n_menos_1": d[n - 1],
        "p_n_menos_2": d[n - 2],
    }
    if Q is not None and N is not None:
        r["valor_bolsa"] = valor_esperado(boleto, P, Q, N)
    return r
