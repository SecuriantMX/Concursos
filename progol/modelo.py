"""
Modelo de probabilidades 1X2 para quinielas.

Tres estimadores por partido:
  1. Mercado: momios de varias casas sin margen (metodo de Shin).
  2. Poisson con correccion Dixon-Coles a partir de goles esperados por equipo.
  3. Elo: diferencia de rating -> marcador esperado -> 1X2 via Poisson.

Referencias:
  Shin (1993), "Measuring the incidence of insider trading in a market for
    state-contingent claims", Economic Journal 103.
  Strumbelj (2014), "On determining probability forecasts from betting odds",
    Int. J. Forecasting 30 (Shin supera a la normalizacion simple).
  Dixon & Coles (1997), "Modelling association football scores and
    inefficiencies in the football betting market", Applied Statistics 46.
  Elo para selecciones: formula publicada en eloratings.net (+100 de local).
"""
import warnings
from math import exp, factorial, log, sqrt

MAXG = 10  # goles maximos por equipo en la rejilla de marcadores


# ---------------------------------------------------------------- mercado
def shin(momios):
    """Probabilidades sin margen por el metodo de Shin. momios: decimales [L, E, V]."""
    q = [1.0 / o for o in momios]
    suma = sum(q)
    if suma <= 1.0:  # sin margen (o arbitraje): solo normalizar
        return [x / suma for x in q], 0.0

    def probs(z):
        return [(sqrt(z * z + 4 * (1 - z) * x * x / suma) - z) / (2 * (1 - z)) for x in q]

    lo, hi = 0.0, 0.4
    for _ in range(200):  # biseccion sobre z para que las probabilidades sumen 1
        mid = (lo + hi) / 2
        if sum(probs(mid)) > 1:
            lo = mid
        else:
            hi = mid
    z = (lo + hi) / 2
    p = probs(z)
    s = sum(p)
    return [x / s for x in p], z


def proporcional(momios):
    q = [1.0 / o for o in momios]
    s = sum(q)
    return [x / s for x in q]


def mercado(lista_momios):
    """Promedia las probabilidades de Shin de cada casa. Regresa (p, margen medio, n casas)."""
    ps, margenes = [], []
    for m in lista_momios:
        p, _ = shin(m)
        ps.append(p)
        margenes.append(sum(1.0 / o for o in m) - 1.0)
    n = len(ps)
    p = [sum(x[i] for x in ps) / n for i in range(3)]
    return p, sum(margenes) / n, n


# ---------------------------------------------------------------- poisson
def pois(k, lam):
    return exp(-lam) * lam ** k / factorial(k)


def tau(x, y, lh, la, rho):
    """Correccion de Dixon-Coles para marcadores bajos."""
    if x == 0 and y == 0:
        return 1 - lh * la * rho
    if x == 0 and y == 1:
        return 1 + lh * rho
    if x == 1 and y == 0:
        return 1 + la * rho
    if x == 1 and y == 1:
        return 1 - rho
    return 1.0


def rejilla(lh, la, rho=-0.10):
    g = [[pois(x, lh) * pois(y, la) * tau(x, y, lh, la, rho) for y in range(MAXG + 1)]
         for x in range(MAXG + 1)]
    s = sum(map(sum, g))
    return [[v / s for v in fila] for fila in g]


def p1x2(lh, la, rho=-0.10):
    g = rejilla(lh, la, rho)
    L = sum(g[x][y] for x in range(MAXG + 1) for y in range(MAXG + 1) if x > y)
    E = sum(g[x][x] for x in range(MAXG + 1))
    return [L, E, 1 - L - E]


def mercados_goles(lh, la, rho=-0.10):
    """Mercados alternos a partir de la misma rejilla."""
    g = rejilla(lh, la, rho)
    R = range(MAXG + 1)
    over25 = sum(g[x][y] for x in R for y in R if x + y >= 3)
    btts = sum(g[x][y] for x in R for y in R if x >= 1 and y >= 1)
    return {"over25": over25, "under25": 1 - over25, "btts_si": btts, "btts_no": 1 - btts}


def lambdas(gf_l, gc_l, gf_v, gc_v, media, ventaja_local, n_l, n_v, k=6.0):
    """
    Goles esperados de cada equipo.
    gf/gc: promedio de goles (o xG) a favor y en contra por partido en la muestra.
    media: goles por equipo por partido de referencia en la competencia.
    Cada tasa se encoge hacia la media con peso k (partidos ficticios) porque
    diez partidos son poca muestra. ventaja_local multiplica al local y divide
    al visitante (1.0 en sede neutral).
    """
    def enc(x, n):
        return (x * n + media * k) / (n + k)

    atq_l, def_l = enc(gf_l, n_l) / media, enc(gc_l, n_l) / media
    atq_v, def_v = enc(gf_v, n_v) / media, enc(gc_v, n_v) / media
    lh = media * atq_l * def_v * ventaja_local
    la = media * atq_v * def_l / ventaja_local
    return lh, la


# ---------------------------------------------------------------- elo
def elo_esperado(elo_l, elo_v, bono_local=100.0):
    return 1.0 / (1.0 + 10 ** (-(elo_l + bono_local - elo_v) / 400.0))


def elo_1x2(elo_l, elo_v, bono_local=100.0, goles_totales=2.6, rho=-0.10):
    """
    Elo da el marcador esperado We = P(gana) + 0.5 P(empata), no el empate.
    Se busca el reparto de goles (total fijo) cuyo Poisson reproduce ese We.

    Devuelve (probabilidades, We que esas probabilidades reproducen). Con el
    total de goles fijo el empate nunca baja de P(0-0), asi que We no pasa de
    1 - 0.5*exp(-total): unos 600 puntos de diferencia con 2.81 goles. Mas
    alla de eso no hay solucion; se devuelve la del borde con su We real y se
    avisa, para que el dato no pase como si fuera el de Elo.
    """
    we = elo_esperado(elo_l, elo_v, bono_local)
    lo, hi = 1e-9, 1 - 1e-9  # fraccion de los goles que anota el local
    for _ in range(80):
        mid = (lo + hi) / 2
        p = p1x2(goles_totales * mid, goles_totales * (1 - mid), rho)
        if p[0] + 0.5 * p[1] < we:
            lo = mid
        else:
            hi = mid
    f = (lo + hi) / 2
    p = p1x2(goles_totales * f, goles_totales * (1 - f), rho)
    logrado = p[0] + 0.5 * p[1]
    if abs(logrado - we) > 1e-6:
        warnings.warn(f"Elo pide We={we:.4f} y con {goles_totales} goles solo se alcanza {logrado:.4f}; "
                      "la diferencia de rating es demasiado grande para este total de goles")
    return p, logrado


# ---------------------------------------------------------------- mezcla
def mezclar(componentes, pesos):
    """Mezcla lineal. componentes: dict nombre -> [L,E,V] o None. Reparte el peso de los ausentes."""
    activos = {k: v for k, v in componentes.items() if v is not None}
    total = sum(pesos[k] for k in activos)
    p = [sum(pesos[k] / total * activos[k][i] for k in activos) for i in range(3)]
    return p, {k: pesos[k] / total for k in activos}


def ajustar(p, deltas):
    """Suma ajustes en puntos de probabilidad [dL, dE, dV] y renormaliza."""
    q = [max(1e-4, a + b) for a, b in zip(p, deltas)]
    s = sum(q)
    return [x / s for x in q]


def entropia(p):
    return -sum(x * log(x) for x in p if x > 0) / log(3)  # normalizada 0..1
