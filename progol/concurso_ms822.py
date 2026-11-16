"""
Progol Media Semana, concurso 822. Entradas del modelo.

Boleta oficial (loterianacional.gob.mx/ProgolMediaSemana/Quiniela, leida el
16-nov-2026 a las 12:55 CDMX): 9 partidos, quiniela sencilla $15, venta hasta el
martes 17-nov a las 13:00. Cuenta el marcador del tiempo reglamentario.
Multiples: hasta 3 dobles y 2 triples (72 combinaciones, $1,080).

Momios: una fila por casa. Por partido se usa la lectura mas reciente que tenga al
menos 8 casas y no se mezclan lecturas de horas distintas.
  M1  lunes 16-nov 12:55-13:10 CDMX. betexplorer (ficha mexico-jamaica), oddsrun,
      sportytrader, ESPN (DraftKings).
  M2  lunes 16-nov 16:05-16:20. oddsmath (BetInAsia, 1xBet, Marathonbet, FEZbet,
      Bettogoal, con hora de ultimo cambio entre 15:37 y 15:55) y betexplorer
      (bet365.us, BetMGM.us, Stake.com, con hora por momio; promedio releido a las
      16:15: 3.23/3.82/1.90). La linea se movio hacia Lyonnes en tres tramos desde el
      15-nov (apertura de 1xBet 2.44/3.95/2.34) y ninguna casa regreso. Pinnacle
      3.18/3.53/2.11 queda fuera: su ultima hora verificable es anterior al ultimo tramo.
  M3-M5  lunes 16-nov 16:02-16:10. PinnRadar y SteamWatch (Pinnacle), betexplorer
      (bet365, BetMGM, Stake), Oddsbunch y OddStorm (resto). Ya incluye las
      conferencias de prensa de la tarde.
  M6, M8  lunes 16-nov 16:13-16:22. betexplorer, tabla por casa con hora de ultimo cambio.
  M7  lunes 16-nov ~13:00-13:20. mercadodecuotas.com, flashscore, betexplorer, ESPN.
  M9  lunes 16-nov ~13:05. betexplorer, statsniper, rg.org, ESPN (DraftKings).

Limpieza de filas:
  - fuera los promedios de comparador y los "mejor momio" (no son una casa);
  - fuera los mercados de intercambio (Betfair Exchange, Kalshi): se usan solo de
    contraste. A las 16:02 Kalshi daba 42/24/35 en M3, 42/26/33 en M4 y 46/30/25 en M5;
  - fuera las filas cuyo 1/L + 1/E + 1/V no cae entre 1.00 y 1.15;
  - filas con los tres momios identicos cuentan una vez (casas con el mismo proveedor);
  - una misma casa no entra dos veces: si hay dos lecturas, vale la que trae hora.

Elo: eloratings.net/World.tsv, leido el 16-nov-2026 a las 14:00 CDMX.
xG: se guarda con el numero de partidos de la muestra (xg_n). El Poisson solo entra
cuando cada equipo tiene al menos MIN_XG partidos en su corte de casa o de visita.
  M6-M8  footystats.org, Serie A 2026, columnas At Home / At Away, 17 partidos por lado
         (leido y vuelto a comprobar en vivo el 16-nov). statz.ai da otros valores
         (M6: 1.66/0.89 y 1.17/1.15; M7: 1.29/0.87 y 1.04/1.68); con ellos el boleto no cambia.
  M9     American Soccer Analysis, temporada regular de la MLS 2026, 17 partidos por lado.
         El partido es de playoffs: misma liga, otra fase.

Porcentajes de venta del publico del 822: NO ENCONTRADOS (la pagina oficial seguia
con la imagen del 821 a las 15:56 CDMX del 16-nov). Bolsa del 822: NO ENCONTRADA.
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
    dict(id="M2", local="Arsenal F", visita="Lyonnes F", tipo="club", neutral=False,
         xg=(2.89, 0.54, 3.035, 0.335), xg_n=(2, 2),
         momios=[
             [3.44, 3.75, 2.00, "BetInAsia"],
             [3.25, 3.64, 1.91, "1xBet"],
             [3.18, 3.64, 1.89, "Marathonbet"],
             [3.40, 3.40, 1.95, "FEZbet"],
             [3.25, 3.33, 1.92, "Bettogoal"],
             [3.40, 4.20, 1.85, "bet365.us"],
             [3.00, 3.50, 1.98, "BetMGM.us"],
             [3.30, 3.75, 1.89, "Stake.com"],
         ]),
    dict(id="M3", local="Dinamarca", visita="Noruega", tipo="seleccion", neutral=False, elo=(1920, 1909),
         momios=[
             [2.33, 4.04, 2.83, "Pinnacle"],
             [2.25, 4.00, 2.75, "bet365"],
             [2.25, 3.80, 2.80, "BetMGM"],
             [2.24, 3.75, 2.70, "Stake"],
             [2.35, 3.95, 2.83, "1xBet"],
             [2.35, 3.80, 2.77, "Betano"],
             [2.30, 3.70, 2.62, "William Hill"],
             [2.20, 3.70, 2.70, "BetVictor"],
             [2.41, 3.80, 2.75, "Dafabet"],
         ]),
    dict(id="M4", local="Polonia", visita="Suecia", tipo="seleccion", neutral=False, elo=(1663, 1784),
         momios=[
             [2.33, 3.73, 2.95, "Pinnacle"],
             [2.30, 3.60, 2.80, "bet365"],
             [2.25, 3.60, 2.90, "BetMGM"],
             [2.24, 3.50, 2.80, "Stake"],
             [2.28, 3.69, 3.12, "1xBet"],
             [2.25, 3.65, 3.08, "Marathonbet"],
             [2.25, 3.60, 3.05, "Betano"],
             [2.20, 3.30, 2.90, "William Hill"],
             [2.20, 3.50, 2.80, "BetVictor"],
             [2.25, 3.70, 3.10, "Dafabet"],
         ]),
    dict(id="M5", local="Rep. Irlanda", visita="Kosovo", tipo="seleccion", neutral=False, elo=(1703, 1700),
         momios=[
             [2.15, 3.21, 3.85, "Pinnacle"],
             [2.10, 3.10, 3.70, "bet365"],
             [2.20, 3.10, 3.50, "BetMGM"],
             [2.09, 3.05, 3.55, "Stake"],
             [2.18, 3.24, 3.80, "1xBet"],
             [2.15, 3.20, 3.76, "Marathonbet"],
             [2.15, 3.25, 3.90, "Betano"],
             [2.10, 3.00, 3.60, "William Hill"],
             [2.05, 3.10, 3.50, "BetVictor"],
             [2.20, 3.15, 3.70, "Dafabet"],
         ]),
    dict(id="M6", local="Cruzeiro", visita="Palmeiras", tipo="club", neutral=False,
         xg=(1.77, 1.15, 1.49, 1.66), xg_n=(17, 17),
         momios=[
             [2.79, 3.55, 2.56, "BetInAsia"],
             [2.81, 3.47, 2.52, "1xBet"],
             [2.70, 3.50, 2.45, "bet365"],
             [2.75, 3.40, 2.40, "Betfair"],
             [2.80, 3.50, 2.40, "bwin"],
             [2.78, 3.42, 2.50, "Megapari"],
             [2.70, 3.35, 2.50, "Cloudbet"],
             [2.72, 3.30, 2.45, "Betsson"],
             [2.70, 3.29, 2.46, "Bets.io"],
             [2.63, 3.30, 2.50, "Betway"],
             [2.63, 3.25, 2.45, "888sport"],
             [2.62, 3.25, 2.45, "William Hill"],
             [2.70, 3.40, 2.39, "Stake.com"],
             [2.80, 3.50, 2.32, "Unibet"],
             [2.70, 3.35, 2.55, "Duelbits"],
             [2.72, 3.45, 2.42, "Rainbet"],
             [2.70, 3.45, 2.42, "Roobet"],
         ]),
    dict(id="M7", local="Corinthians", visita="Botafogo", tipo="club", neutral=False,
         xg=(1.66, 1.0, 1.38, 1.71), xg_n=(17, 17),
         momios=[
             [1.81, 3.81, 4.26, "Pinnacle"],
             [1.86, 3.75, 4.22, "1xBet"],
             [1.90, 3.60, 4.10, "Betano"],
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
         xg=(1.66, 1.17, 1.4, 1.66), xg_n=(17, 17),
         momios=[
             [2.43, 3.30, 3.08, "BetInAsia"],
             [2.34, 3.28, 3.23, "1xBet"],
             [2.32, 3.20, 3.10, "bet365"],
             [2.30, 3.20, 3.00, "Betfair"],
             [2.30, 3.25, 3.10, "bwin"],
             [2.38, 3.20, 2.95, "Unibet"],
             [2.38, 3.25, 2.90, "Betway"],
             [2.35, 3.16, 2.97, "Bets.io"],
             [2.42, 3.15, 3.00, "Duelbits"],
             [2.36, 3.20, 3.00, "Rainbet"],
             [2.34, 3.20, 3.00, "Roobet"],
             [2.28, 3.20, 3.05, "Stake.com"],
             [2.35, 3.20, 3.00, "Cloudbet"],
             [2.32, 3.24, 3.19, "Megapari"],
             [2.35, 3.15, 2.95, "Betsson"],
             [2.30, 3.00, 3.00, "888sport"],
         ]),
    dict(id="M9", local="Orlando", visita="Cincinnati", tipo="club", neutral=False,
         xg=(1.86, 1.87, 1.6, 1.95), xg_n=(17, 17),
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
