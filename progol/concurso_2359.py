"""
Entradas del Progol 2359 (juegos del 14 al 16 de noviembre de 2026).
Todo fue consultado el 13-nov-2026. None = NO ENCONTRADO.

Fuentes:
  boleta, precios y porcentajes de venta: loterianacional.gob.mx (Progol/Quiniela, Progol/Momios)
  momios, en este orden por partido: betexplorer.com (promedio de las casas listadas),
          oddschecker.com (mejor precio), Caliente via ESPN (solo P1), Playdoit (P1, R1, R3, R4)
  Elo de selecciones: eloratings.net (World.tsv, sin fecha de corte)
  goles ultimos 10: Wikipedia / Flashscore / ESPN (selecciones), footystats (xG de clubes)
"""

# momios: lista de [L, E, V] decimales
# gol: (gf_local, gc_local, n_local, gf_visita, gc_visita, n_visita) en los ultimos partidos
# xg:  (xg_local_en_casa, xga_local_en_casa, xg_visita_fuera, xga_visita_fuera) por partido
# publico: porcentaje de venta oficial [L, E, V]
PARTIDOS = [
    dict(id="P1", local="Queretaro", visita="Monterrey", tipo="club", neutral=False,
         momios=[[3.36, 3.61, 1.96], [3.60, 3.80, 2.00], [3.50, 3.70, 1.97], [3.50, 3.80, 2.00]],
         publico=[17.55, 16.17, 66.28]),
    dict(id="P2", local="NY Red Bulls", visita="America", tipo="club", neutral=False,
         momios=[], publico=[32.33, 22.79, 44.88]),
    dict(id="P3", local="Japon", visita="Brasil", tipo="seleccion", neutral=True,
         momios=[[3.76, 3.73, 1.81], [3.90, 3.90, 1.87]], elo=(1897, 2001), publico=[20.23, 19.96, 59.81]),
    dict(id="P4", local="Panama", visita="Curazao", tipo="seleccion", neutral=False,
         momios=[[1.64, 3.42, 5.15]], elo=(1650, 1495), publico=[71.51, 15.03, 13.46]),
    dict(id="P5", local="Irlanda del Norte", visita="Ucrania", tipo="seleccion", neutral=False,
         momios=[[2.51, 2.98, 3.05], [2.62, 3.10, 3.10]],
         elo=(1672, 1724), gol=(8, 7, 10, 9, 14, 10), publico=[57.24, 18.13, 24.63]),
    dict(id="P6", local="Chipre", visita="Montenegro", tipo="seleccion", neutral=False,
         momios=[[3.06, 3.21, 2.31], [3.10, 3.35, 2.35]],
         elo=(1352, 1494), gol=(14, 12, 10, 18, 13, 10), publico=[22.36, 27.24, 50.40]),
    dict(id="P7", local="Belgica", visita="Italia", tipo="seleccion", neutral=False,
         momios=[[2.09, 3.64, 3.16], [2.15, 3.90, 3.35]],
         elo=(1971, 1948), gol=(19, 11, 10, 16, 10, 9), publico=[41.78, 26.71, 31.51]),
    dict(id="P8", local="Espana", visita="Inglaterra", tipo="seleccion", neutral=False,
         momios=[[1.69, 4.02, 4.30], [1.75, 4.33, 4.50]],
         elo=(2290, 2150), gol=(23, 6, 10, 27, 10, 10), publico=[61.73, 21.91, 16.36]),
    dict(id="P9", local="Islas Feroe", visita="Moldavia", tipo="seleccion", neutral=False,
         momios=[], elo=(1397, 1308), gol=(10, 10, 9, 11, 21, 10), publico=[37.76, 34.73, 27.51]),
    dict(id="P10", local="Alemania", visita="Paises Bajos", tipo="seleccion", neutral=False,
         momios=[[1.81, 3.98, 3.66]],
         elo=(1895, 1974), gol=(22, 8, 10, 26, 11, 10), publico=[57.17, 22.00, 20.83]),
    dict(id="P11", local="Mirassol", visita="Atletico Mineiro", tipo="club", neutral=False,
         momios=[[1.98, 3.50, 3.60], [2.05, 3.50, 3.70]], publico=[34.74, 19.06, 46.20]),
    dict(id="P12", local="Criciuma", visita="Novorizontino", tipo="club", neutral=False,
         momios=[[2.73, 3.04, 2.57], [2.76, 3.20, 2.65]],
         xg=(1.81, 1.09, 1.45, 1.38), publico=[36.26, 29.32, 34.42]),
    dict(id="P13", local="Sport", visita="Goias", tipo="club", neutral=False,
         momios=[[3.47, 3.68, 1.92], [3.60, 3.80, 1.95]], publico=[37.50, 24.74, 37.76]),
    dict(id="P14", local="Cerezo Osaka", visita="Urawa", tipo="club", neutral=False,
         momios=[[2.87, 3.45, 2.18], [3.00, 3.90, 2.30]], xg=(1.51, 1.26, 2.14, 1.62), publico=[51.17, 26.03, 22.80]),
]

REVANCHA = [
    dict(id="R1", local="Jamaica", visita="Mexico", tipo="seleccion", neutral=False,
         momios=[[5.86, 3.83, 1.50], [5.75, 3.80, 1.53]], elo=(1543, 1868), publico=[15.38, 23.65, 60.97]),
    dict(id="R2", local="Georgia", visita="Hungria", tipo="seleccion", neutral=False,
         momios=[[3.03, 3.08, 2.45], [3.10, 3.10, 2.45]],
         elo=(1628, 1725), gol=(8, 11, 10, 12, 7, 10), publico=[26.30, 25.86, 47.84]),
    dict(id="R3", local="Noruega", visita="Gales", tipo="seleccion", neutral=False,
         momios=[[1.22, 6.46, 10.71], [1.24, 7.00, 12.00], [1.25, 6.33, 11.00]],
         elo=(1901, 1681), gol=(19, 19, 10, 14, 11, 10), publico=[70.03, 16.76, 13.21]),
    dict(id="R4", local="Suecia", visita="Bosnia y Herzegovina", tipo="seleccion", neutral=False,
         momios=[[1.51, 4.31, 5.87], [1.55, 4.50, 6.50], [1.56, 4.00, 6.33]],
         elo=(1774, 1672), gol=(17, 18, 10, 12, 12, 10), publico=[66.08, 20.97, 12.95]),
    dict(id="R5", local="Letonia", visita="Armenia", tipo="seleccion", neutral=False,
         momios=[[2.94, 3.32, 2.26], [3.10, 3.40, 2.30]],
         elo=(1241, 1348), gol=(6, 15, 10, 9, 20, 10), publico=[29.48, 31.63, 38.89]),
    dict(id="R6", local="Croacia", visita="Chequia", tipo="seleccion", neutral=False,
         momios=[[1.49, 4.32, 6.02], [1.53, 4.50, 6.50]],
         elo=(1852, 1653), gol=(13, 24, 10, 9, 20, 10), publico=[69.13, 18.04, 12.83]),
    dict(id="R7", local="Kashima", visita="Yokohama Marinos", tipo="club", neutral=False,
         momios=[[1.64, 3.88, 4.30], [1.67, 4.20, 4.60]], xg=(1.64, 1.25, 1.32, 1.68), publico=[40.08, 30.19, 29.73]),
]

# Pesos de la mezcla. El mercado pesa mas porque resume informacion de bajas,
# rotaciones y motivacion que el modelo propio no ve.
# En selecciones el Poisson con goles crudos de los ultimos 10 NO entra a la mezcla:
# no esta ajustado por rival (ejemplo: da 48% a Noruega contra 79% del mercado) y
# no se encontro xG. Se muestra solo como referencia. El Elo si ajusta por rival.
PESOS = {"mercado": 0.75, "elo": 0.25, "poisson": 0.0}
PESOS_CLUB = {"mercado": 0.80, "poisson": 0.20}

# Premios del concurso 2358 (reporteindigo.com, 9-nov-2026) para estimar cuantas
# combinaciones juega el publico: ganadores con 10, 11, 12 y 13 aciertos.
GANADORES_2358 = {10: 6223, 11: 1085, 12: 137, 13: 10}

BOLSA = 9_000_000   # primer lugar, captura de la app MiLoteria, 13-nov-2026
TOPE = 1100         # presupuesto para Progol + Revancha

# Momios de Playdoit leidos el 13-nov-2026 ~15:50 CDMX (formato americano convertido a decimal).
# Solo estos cuatro partidos se pudieron leer; doble oportunidad, ambos anotan y handicap: no leidos.
PLAYDOIT = {
    "P1": {"1x2": [3.50, 3.80, 2.00], "over25": 1.57, "under25": 2.30},
    "R1": {"1x2": [5.75, 3.80, 1.53], "over25": 1.94, "under25": 1.75},
    "R3": {"1x2": [1.25, 6.33, 11.00]},
    "R4": {"1x2": [1.56, 4.00, 6.33], "over25": 1.63, "under25": 2.30},
}
