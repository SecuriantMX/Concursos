"""
Progol Media Semana, concurso 822. Entradas del modelo.

Boleta oficial (loterianacional.gob.mx/ProgolMediaSemana/Quiniela, leida el
16-nov-2026 a las 12:55 CDMX): 9 partidos, quiniela sencilla $15, venta hasta el
martes 17-nov a las 13:00. Cuenta el marcador del tiempo reglamentario.
Multiples: hasta 3 dobles y 2 triples (72 combinaciones, $1,080).

Momios: lectura del lunes 16-nov-2026 entre 12:55 y 13:30 CDMX, una fila por casa.
Fuentes por partido:
  M1  betexplorer (ficha mexico-jamaica), oddsrun, sportytrader, ESPN (DraftKings)
  M2  betexplorer (ficha arsenal-ol-lyonnes), con hora por momio
  M3-M5  betexplorer (fichas de la Nations League), dailysports.net, ESPN (DraftKings)
  M6-M8  mercadodecuotas.com, betexplorer, flashscore, ESPN (DraftKings)
  M9  betexplorer (ficha orlando-city-fc-cincinnati), statsniper, rg.org, ESPN (DraftKings)

Limpieza de filas:
  - fuera los promedios de comparador y los "mejor momio" (no son una casa);
  - fuera las filas cuyo 1/L + 1/E + 1/V no cae entre 1.00 y 1.15;
  - filas con los tres momios identicos cuentan una vez (casas con el mismo proveedor);
  - M2: la linea se movio fuerte el 16-nov (bet365.us paso de 2.70/4.00/2.20 a
    3.40/4.20/1.85 a las 09:53 CDMX) y dos comparadores sin hora por momio seguian
    mostrando precios viejos; solo entran las tres casas con hora verificable.
    Relectura del promedio de betexplorer a las 13:58 CDMX: 3.23/3.82/1.91, sin cambio.

Elo: eloratings.net/World.tsv, leido el 16-nov-2026 a las 14:00 CDMX.
xG: se guarda con el numero de partidos de la muestra (xg_n). El Poisson solo entra
cuando cada equipo tiene al menos MIN_XG partidos en su corte de casa o de visita.

Porcentajes de venta del publico del 822: NO ENCONTRADOS (la pagina oficial seguia
con la imagen del 821 a las 13:04 CDMX). Bolsa del 822: NO ENCONTRADA.
Referencia: en el 821 hubo 17 ganadores de 9 aciertos, $181,406.91 cada uno.
"""

PARTIDOS = [
    dict(id="M1", local="Mexico", visita="Jamaica", tipo="seleccion", neutral=False, elo=(1837, 1574),
         momios=[
             [1.14, 6.50, 15.00, "bet365"],
             [1.17, 6.50, 10.50, "BetMGM.us"],
             [1.16, 6.40, 13.00, "Stake.com"],
             [1.15, 6.50, 12.00, "DraftKings"],
             [1.15, 6.94, 11.90, "Pinnacle"],
             [1.15, 7.50, 14.00, "Betfair"],
             [1.17, 6.50, 10.00, "Ladbrokes"],
             [1.16, 6.85, 13.25, "Marathonbet"],
             [1.18, 7.40, 15.00, "Dafabet"],
             [1.14, 6.25, 11.00, "Everygame"],
             [1.15, 6.30, 11.00, "Mansion"],
             [1.09, 7.10, 15.00, "Macauslot"],
             [1.14, 6.50, 11.00, "Spreadex"],
             [1.15, 5.90, 12.00, "Duelbits"],
             [1.18, 6.70, 14.00, "Fonbet"],
             [1.16, 6.70, 13.00, "Ysb88"],
             [1.17, 6.85, 13.10, "1xBet"],
             [1.18, 6.60, 12.00, "Roobet"],
             [1.17, 7.50, 12.00, "Betway"],
             [1.16, 6.60, 13.50, "Betsson"],
             [1.20, 6.70, 15.00, "Shangrila"],
         ]),
    # xG de la fase de liga de la UWCL (footystats): solo 2 partidos por lado, no alcanza la muestra minima
    dict(id="M2", local="Arsenal F", visita="Lyonnes F", tipo="club", neutral=False,
         xg=(2.89, 0.54, 3.035, 0.335), xg_n=(2, 2),
         momios=[
             [3.40, 4.20, 1.85, "bet365.us"],
             [3.00, 3.50, 1.98, "BetMGM.us"],
             [3.30, 3.75, 1.89, "Stake.com"],
         ]),
    dict(id="M3", local="Dinamarca", visita="Noruega", tipo="seleccion", neutral=False, elo=(1920, 1909),
         momios=[
             [2.38, 3.80, 2.70, "bet365.us"],
             [2.30, 3.75, 2.70, "BetMGM.us"],
             [2.30, 3.70, 2.70, "Stake.com"],
             [2.35, 3.70, 2.60, "DraftKings"],
             [2.36, 3.76, 2.74, "Melbet"],
             [2.41, 3.85, 2.80, "1xBet"],
             [2.30, 3.70, 2.62, "BC.Game"],
             [2.41, 3.98, 2.77, "Betwinner"],
             [2.26, 3.79, 2.60, "Mostbet"],
         ]),
    dict(id="M4", local="Polonia", visita="Suecia", tipo="seleccion", neutral=False, elo=(1663, 1784),
         momios=[
             [2.20, 3.60, 3.00, "bet365.us"],
             [2.25, 3.60, 2.90, "BetMGM.us"],
             [2.22, 3.45, 2.75, "Stake.com"],
             [2.25, 3.55, 2.85, "DraftKings"],
             [2.23, 3.60, 3.05, "Melbet"],
             [2.28, 3.69, 3.12, "1xBet"],
             [2.20, 3.30, 2.90, "BC.Game"],
             [2.30, 3.76, 3.06, "Betwinner"],
             [2.20, 3.60, 2.75, "BetWay"],
             [2.25, 3.47, 2.80, "Mostbet"],
         ]),
    dict(id="M5", local="Rep. Irlanda", visita="Kosovo", tipo="seleccion", neutral=False, elo=(1703, 1700),
         momios=[
             [2.10, 3.10, 3.70, "bet365.us"],
             [2.20, 3.10, 3.50, "BetMGM.us"],
             [2.08, 3.00, 3.50, "Stake.com"],
             [2.10, 3.10, 3.60, "DraftKings"],
             [2.13, 3.17, 3.72, "Melbet"],
             [2.18, 3.24, 3.81, "1xBet"],
             [2.10, 3.00, 3.60, "BC.Game"],
             [2.16, 3.26, 3.88, "Betwinner"],
             [2.10, 3.25, 3.60, "BetWay"],
         ]),
    dict(id="M6", local="Cruzeiro", visita="Palmeiras", tipo="club", neutral=False,
         momios=[
             [2.78, 3.41, 2.55, "Pinnacle"],
             [2.81, 3.46, 2.52, "1xBet"],
             [2.75, 3.50, 2.50, "Bet365"],
             [2.85, 3.50, 2.42, "Betano"],
             [2.70, 3.50, 2.40, "BetVictor"],
             [2.75, 3.40, 2.40, "Betfair"],
             [2.72, 3.36, 2.44, "Marathonbet"],
             [2.62, 3.25, 2.45, "William Hill"],
             [2.70, 3.50, 2.45, "bet365.us"],
             [2.80, 3.50, 2.40, "BetMGM.us"],
             [2.80, 3.40, 2.33, "Stake.com"],
             [2.75, 3.35, 2.45, "DraftKings"],
             [2.78, 3.42, 2.49, "Melbet"],
         ]),
    dict(id="M7", local="Corinthians", visita="Botafogo", tipo="club", neutral=False,
         momios=[
             [1.81, 3.81, 4.26, "Pinnacle"],
             [1.86, 3.75, 4.22, "1xBet"],
             [1.90, 3.60, 4.10, "Betano"],
             [1.83, 3.60, 4.33, "Bet365"],
             [1.83, 3.60, 4.20, "Betfair"],
             [1.80, 3.64, 4.10, "Marathonbet"],
             [1.80, 3.60, 4.10, "BetVictor"],
             [1.83, 3.50, 3.90, "William Hill"],
             [1.76, 3.60, 4.50, "bet365.us"],
             [1.82, 3.70, 4.20, "BetMGM.us"],
             [1.83, 3.60, 4.30, "Fanatics"],
             [1.80, 3.70, 4.20, "DraftKings"],
         ]),
    dict(id="M8", local="Sao Paulo", visita="Fluminense", tipo="club", neutral=False,
         momios=[
             [2.42, 3.27, 3.07, "Pinnacle"],
             [2.34, 3.28, 3.22, "1xBet"],
             [2.40, 3.25, 3.05, "Betano"],
             [2.38, 3.20, 3.10, "Bet365"],
             [2.27, 3.18, 3.12, "Marathonbet"],
             [2.30, 3.25, 3.00, "BetVictor"],
             [2.30, 3.20, 3.00, "Betfair"],
             [2.30, 3.00, 3.00, "William Hill"],
             [2.33, 3.20, 3.10, "bet365.us"],
             [2.30, 3.25, 3.10, "BetMGM.us"],
         ]),
    dict(id="M9", local="Orlando", visita="Cincinnati", tipo="club", neutral=False,
         momios=[
             [2.50, 3.90, 2.45, "bet365.us"],
             [2.37, 4.00, 2.45, "BetMGM.us"],
             [2.45, 4.00, 2.45, "FanDuel"],
             [2.33, 4.00, 2.49, "Stake.com"],
             [2.40, 3.80, 2.45, "DraftKings"],
             [2.49, 3.97, 2.54, "Pinnacle"],
             [2.36, 4.00, 2.51, "Caesars"],
             [2.23, 4.10, 2.65, "BetRivers"],
             [2.46, 3.90, 2.51, "Bovada"],
             [2.40, 4.00, 2.50, "ESPN BET"],
             [2.35, 3.80, 2.45, "Fanatics"],
             [2.25, 4.00, 2.65, "Hard Rock Bet"],
             [2.50, 4.13, 2.57, "1xBet"],
             [2.46, 4.04, 2.51, "22Bet"],
             [2.35, 3.95, 2.44, "Tonybet"],
             [2.40, 3.90, 2.45, "29Black"],
             [2.50, 3.90, 2.55, "LetsBetMD"],
         ]),
]

# tabla oficial de multiples de Media Semana: hasta 3 dobles con 0, 1 o 2 triples
MEDIA_SEMANA = {"precio": 15, "max_dobles": {0: 3, 1: 3, 2: 3}}

PESOS_SELECCION = {"mercado": 0.75, "elo": 0.25}
PESOS_CLUB = {"mercado": 0.80, "poisson": 0.20}
GOLES_ELO = 2.81   # goles por partido de la muestra de selecciones usada en el concurso 2359
MIN_XG = 8         # partidos minimos por lado para que el xG entre al Poisson
TOPE = 1100        # pesos, fijado por el usuario el 16-nov
