"""
Progol Media Semana, concurso 822. Entradas del modelo.

Boleta oficial (loterianacional.gob.mx/ProgolMediaSemana/Quiniela, leida el
16-nov-2026 a las 12:55 CDMX): 9 partidos, quiniela sencilla $15, venta hasta el
martes 17-nov a las 13:00. Cuenta el marcador del tiempo reglamentario.
Multiples: hasta 3 dobles y 2 triples (72 combinaciones, $1,080).

Momios: una fila por casa. Por partido se usa la lectura mas reciente que tenga al
menos 8 casas y no se mezclan lecturas de horas distintas. Lectura vigente: lunes
16-nov-2026 entre 20:02 y 20:36 CDMX; un segundo agente releyo cada fila en vivo entre
20:30 y 20:50 y las diferencias que hallo ya estan aplicadas.
  M1  oddsrun (Pinnacle y 15 casas), betexplorer (bet365, BetMGM, Stake, con hora),
      sportytrader, ESPN (DraftKings). Pinnacle 1.14/7.22/12.20.
  M2  oddsmath, API por casa con hora de ultimo cambio (BetInAsia, 1xBet, Marathonbet,
      FEZbet, Suprabets), y betexplorer (bet365.us, BetMGM.us, Stake.com). El ultimo
      cambio de todo el mercado visible fue a las 16:55 CDMX. Pinnacle: NO ENCONTRADO
      con hora posterior al 15-nov 21:29; BetInAsia (3.48/3.75/1.98) hace de casa afilada.
      Ojo: en la lectura de las 16:05 las filas de bet365.us y BetMGM.us venian de la
      lectura de las 13:22 y ya estaban viejas (eran 3.20/4.10/1.91 y 3.20/3.60/1.90).
  M3-M5  pinnradar y steamwatch (Pinnacle), betexplorer (3 casas), albion.rs (casas de
      Serbia, con bitacora de cambios) y legalsport.pl (casas de Polonia).
  M6-M8  Pinnacle directo (API publica de invitado), titan007 (tabla por casa con hora)
      y betexplorer (3 casas).
  M9  oddsbunch (Pinnacle y 7 casas), betexplorer, ESPN (DraftKings), Action Network.
Las horas data-created de betexplorer estan en CET (UTC+1), no en UTC.

Limpieza de filas:
  - fuera los promedios de comparador y los "mejor momio" (no son una casa);
  - fuera los mercados de intercambio (Betfair Exchange, Kalshi, Polymarket): se usan
    solo de contraste. Una fila "Betfair" entra solo si la fuente dice que es la casa;
  - fuera las filas cuyo 1/L + 1/E + 1/V no cae entre 1.01 y 1.15. Un margen menor a 1%
    no es un precio normal de casa (promocion o error de captura);
  - filas con los tres momios identicos cuentan una vez (casas con el mismo proveedor);
  - una misma casa no entra dos veces: si hay dos lecturas, vale la que trae hora.
Contraste con la casa mas afilada sola (Pinnacle; BetInAsia en M2): difiere del promedio
de todas las filas en 1 punto o menos en los nueve partidos.

Elo: eloratings.net/World.tsv, leido el 16-nov-2026 a las 14:00 CDMX.
xG: se guarda con el numero de partidos de la muestra (xg_n). El Poisson solo entra
cuando cada equipo tiene al menos MIN_XG partidos en su corte de casa o de visita.
  M6-M8  footystats.org, Serie A 2026, columnas At Home / At Away, 17 partidos por lado
         (leido y vuelto a comprobar en vivo el 16-nov). statz.ai da otros valores
         (M6: 1.66/0.89 y 1.17/1.15; M7: 1.29/0.87 y 1.04/1.68); con ellos el boleto no cambia.
  M9     American Soccer Analysis, temporada regular de la MLS 2026, 17 partidos por lado.
         El partido es de playoffs: misma liga, otra fase.

Porcentajes de venta del publico del 822: NO ENCONTRADOS (la pagina oficial seguia
con la imagen del 821 a las 20:07 CDMX del 16-nov). Bolsa del 822: NO ENCONTRADA.
Referencia: en el 821 hubo 17 ganadores de 9 aciertos, $181,406.91 cada uno.
"""

PARTIDOS = [
    dict(id="M1", local="Mexico", visita="Jamaica", tipo="seleccion", neutral=False, elo=(1837, 1574),
         momios=[
             [1.14, 7.22, 12.20, "Pinnacle"],
             [1.13, 7.00, 17.00, "bet365"],
             [1.15, 7.00, 12.00, "BetMGM"],
             [1.14, 6.60, 13.00, "Stake"],
             [1.14, 7.00, 12.00, "DraftKings"],
             [1.15, 7.00, 11.00, "Ladbrokes"],
             [1.15, 6.80, 14.50, "Betsson"],
             [1.14, 6.00, 9.80, "Sbobet"],
             [1.17, 7.60, 16.00, "Dafabet"],
             [1.14, 7.20, 14.00, "Marathonbet"],
             [1.12, 6.75, 11.00, "Everygame"],
             [1.14, 6.60, 11.00, "Mansion"],
             [1.08, 7.50, 16.00, "Macauslot"],
             [1.13, 7.00, 11.00, "Spreadex"],
             [1.14, 6.10, 12.75, "Duelbits"],
             [1.17, 7.00, 15.00, "Fonbet"],
             [1.13, 6.60, 13.00, "Ysb88"],
             [1.17, 8.00, 12.00, "Betway"],
             [1.16, 6.60, 14.00, "Roobet"],
             [1.18, 7.00, 16.00, "Shangrila"],
         ]),
    dict(id="M2", local="Arsenal F", visita="Lyonnes F", tipo="club", neutral=False,
         xg=(2.89, 0.54, 3.035, 0.335), xg_n=(2, 2),
         momios=[
             [3.48, 3.75, 1.98, "BetInAsia"],
             [3.32, 3.66, 1.88, "1xBet"],
             [3.25, 3.66, 1.86, "Marathonbet"],
             [3.33, 3.50, 1.94, "FEZbet"],
             [3.29, 3.33, 1.90, "Suprabets"],
             [3.20, 4.10, 1.91, "bet365.us"],
             [3.20, 3.60, 1.90, "BetMGM.us"],
             [3.30, 3.75, 1.89, "Stake.com"],
         ]),
    dict(id="M3", local="Dinamarca", visita="Noruega", tipo="seleccion", neutral=False, elo=(1920, 1909),
         momios=[
             [2.32, 4.10, 2.82, "Pinnacle"],
             [2.25, 4.00, 2.75, "bet365"],
             [2.25, 3.80, 2.80, "BetMGM"],
             [2.24, 3.75, 2.70, "Stake.com"],
             [2.32, 4.05, 2.83, "MerkurXtip (Serbia)"],
             [2.38, 3.90, 2.80, "Volcano Bet (Serbia)"],
             [2.35, 3.80, 2.80, "Superbet (Serbia)"],
             [2.27, 3.90, 2.83, "BetOle (Serbia)"],
             [2.25, 4.00, 2.81, "Admiral Bet (Serbia)"],
             [2.27, 3.95, 2.80, "Soccerbet (Serbia)"],
             [2.25, 4.00, 2.80, "MaxBet (Serbia)"],
             [2.25, 3.90, 2.85, "Brazilbet (Serbia)"],
             [2.30, 3.80, 2.75, "Mozzart (Serbia)"],
             [2.22, 3.85, 2.75, "Oktagonbet (Serbia)"],
             [2.30, 4.00, 2.80, "STS (Polonia)"],
             [2.33, 3.80, 2.77, "Fortuna (Polonia)"],
             [2.27, 3.78, 2.75, "Betclic (Polonia)"],
             [2.35, 3.75, 2.75, "Betfan (Polonia)"],
             [2.30, 3.95, 2.80, "LV BET (Polonia)"],
         ]),
    dict(id="M4", local="Polonia", visita="Suecia", tipo="seleccion", neutral=False, elo=(1663, 1784),
         momios=[
             [2.33, 3.71, 2.97, "Pinnacle"],
             [2.30, 3.60, 2.80, "bet365"],
             [2.25, 3.60, 2.90, "BetMGM"],
             [2.24, 3.50, 2.80, "Stake.com"],
             [2.35, 3.70, 2.95, "Volcano Bet (Serbia)"],
             [2.30, 3.65, 3.00, "MerkurXtip (Serbia)"],
             [2.32, 3.60, 2.95, "Superbet (Serbia)"],
             [2.25, 3.70, 3.00, "Brazilbet (Serbia)"],
             [2.26, 3.69, 2.95, "Admiral Bet (Serbia)"],
             [2.25, 3.70, 2.95, "BetOle (Serbia)"],
             [2.30, 3.60, 2.85, "Soccerbet (Serbia)"],
             [2.30, 3.70, 2.80, "Mozzart (Serbia)"],
             [2.25, 3.65, 2.90, "MaxBet (Serbia)"],
             [2.22, 3.65, 2.88, "Oktagonbet (Serbia)"],
             [2.30, 3.55, 2.95, "Superbet (Polonia)"],
             [2.30, 3.70, 2.95, "STS (Polonia)"],
             [2.33, 3.60, 2.88, "Fortuna (Polonia)"],
             [2.27, 3.58, 2.85, "Betclic (Polonia)"],
             [2.35, 3.60, 2.75, "Betfan (Polonia)"],
         ]),
    dict(id="M5", local="Rep. Irlanda", visita="Kosovo", tipo="seleccion", neutral=False, elo=(1703, 1700),
         momios=[
             [2.13, 3.22, 3.89, "Pinnacle"],
             [2.05, 3.20, 3.75, "bet365"],
             [2.10, 3.10, 3.70, "BetMGM"],
             [2.05, 3.05, 3.65, "Stake.com"],
             [2.18, 3.20, 3.80, "Volcano Bet (Serbia)"],
             [2.13, 3.20, 3.95, "MerkurXtip (Serbia)"],
             [2.20, 3.05, 3.80, "Brazilbet (Serbia)"],
             [2.20, 3.05, 3.75, "BetOle (Serbia)"],
             [2.17, 3.10, 3.72, "Admiral Bet (Serbia)"],
             [2.12, 3.15, 3.80, "Superbet (Serbia)"],
             [2.10, 3.15, 3.85, "Soccerbet (Serbia)"],
             [2.15, 3.25, 3.50, "Mozzart (Serbia)"],
             [2.12, 3.10, 3.60, "MaxBet (Serbia)"],
             [2.10, 3.10, 3.75, "Superbet (Polonia)"],
             [2.15, 3.20, 3.80, "STS (Polonia)"],
             [2.11, 3.10, 3.75, "Fortuna (Polonia)"],
             [2.12, 3.10, 3.63, "Betclic (Polonia)"],
             [2.10, 3.15, 3.80, "Betfan (Polonia)"],
             [2.15, 3.20, 3.85, "LV BET (Polonia)"],
         ]),
    dict(id="M6", local="Cruzeiro", visita="Palmeiras", tipo="club", neutral=False,
         xg=(1.77, 1.15, 1.49, 1.66), xg_n=(17, 17),
         momios=[
             [2.78, 3.41, 2.55, "Pinnacle"],
             [2.70, 3.50, 2.45, "bet365.us"],
             [2.80, 3.50, 2.40, "BetMGM.us"],
             [2.70, 3.40, 2.39, "Stake.com"],
             [2.81, 3.47, 2.52, "1xBet"],
             [2.77, 3.50, 2.42, "Betano"],
             [2.63, 3.25, 2.45, "William Hill"],
             [2.72, 3.36, 2.44, "Marathonbet"],
             [2.80, 3.50, 2.32, "Unibet"],
             [2.62, 3.30, 2.50, "Betway"],
             [2.62, 3.25, 2.45, "888sport"],
             [2.72, 3.30, 2.45, "Betsson"],
             [2.70, 3.50, 2.40, "BetVictor"],
             [2.70, 3.15, 2.42, "10bet"],
             [2.68, 3.35, 2.44, "12bet"],
             [2.62, 3.19, 2.34, "SBOBET"],
             [2.68, 3.55, 2.35, "Crown"],
             [2.80, 3.50, 2.50, "Dafabet"],
             [2.75, 3.40, 2.50, "Interwetten"],
             [2.75, 3.40, 2.40, "Betfair Sportsbook"],
             [2.75, 3.35, 2.45, "DraftKings"],
             [2.80, 3.40, 2.40, "FanDuel"],
             [2.70, 3.35, 2.30, "Codere"],
             [2.80, 3.33, 2.54, "Playdoit"],
             [2.95, 3.60, 2.25, "RushBet.MX"],
             [2.78, 3.40, 2.52, "BetOnline"],
             [2.78, 3.40, 2.55, "bet105"],
         ]),
    dict(id="M7", local="Corinthians", visita="Botafogo", tipo="club", neutral=False,
         xg=(1.66, 1.0, 1.38, 1.71), xg_n=(17, 17),
         momios=[
             [1.84, 3.76, 4.18, "Pinnacle"],
             [1.79, 3.60, 4.33, "bet365.us"],
             [1.82, 3.70, 4.20, "BetMGM.us"],
             [1.80, 3.55, 4.10, "Stake.com"],
             [1.86, 3.75, 4.23, "1xBet"],
             [1.83, 3.60, 4.25, "Betano"],
             [1.80, 3.50, 4.00, "William Hill"],
             [1.80, 3.64, 4.10, "Marathonbet"],
             [1.90, 3.50, 3.85, "Unibet"],
             [1.80, 3.45, 4.10, "Betsson"],
             [1.80, 3.60, 4.20, "BetVictor"],
             [1.83, 3.30, 4.00, "10bet"],
             [1.84, 3.55, 3.90, "12bet"],
             [1.82, 3.25, 3.79, "SBOBET"],
             [1.84, 3.65, 3.80, "Crown"],
             [1.87, 3.70, 4.20, "Dafabet"],
             [1.90, 3.55, 4.00, "Interwetten"],
             [1.83, 3.60, 4.20, "Betfair Sportsbook"],
             [1.83, 3.65, 4.00, "DraftKings"],
             [1.76, 3.60, 4.20, "FanDuel"],
             [1.82, 3.45, 3.90, "Codere"],
             [1.83, 3.75, 4.20, "Playdoit"],
             [1.90, 3.55, 3.90, "RushBet.MX"],
             [1.84, 3.73, 4.18, "BetOnline"],
             [1.84, 3.75, 4.17, "bet105"],
         ]),
    dict(id="M8", local="Sao Paulo", visita="Fluminense", tipo="club", neutral=False,
         xg=(1.66, 1.17, 1.4, 1.66), xg_n=(17, 17),
         momios=[
             [2.42, 3.27, 3.07, "Pinnacle"],
             [2.30, 3.20, 3.20, "bet365.us"],
             [2.30, 3.25, 3.10, "BetMGM.us"],
             [2.28, 3.20, 3.05, "Stake.com"],
             [2.34, 3.28, 3.23, "1xBet"],
             [2.37, 3.20, 3.05, "Betano"],
             [2.30, 3.00, 3.00, "William Hill"],
             [2.27, 3.18, 3.12, "Marathonbet"],
             [2.38, 3.20, 2.95, "Unibet"],
             [2.37, 3.25, 2.90, "Betway"],
             [2.30, 3.25, 3.00, "BetVictor"],
             [2.28, 2.95, 3.00, "10bet"],
             [2.32, 3.20, 2.97, "12bet"],
             [2.27, 3.04, 2.84, "SBOBET"],
             [2.28, 3.30, 2.95, "Crown"],
             [2.39, 3.30, 3.15, "Dafabet"],
             [2.40, 3.15, 3.05, "Interwetten"],
             [2.30, 3.20, 3.10, "Betfair Sportsbook"],
             [2.35, 3.25, 3.00, "DraftKings"],
             [2.35, 3.20, 3.10, "FanDuel"],
             [2.25, 3.15, 2.95, "Codere"],
             [2.37, 3.25, 3.10, "Playdoit"],
             [2.41, 3.25, 3.06, "BetOnline"],
         ]),
    dict(id="M9", local="Orlando", visita="Cincinnati", tipo="club", neutral=False,
         xg=(1.86, 1.87, 1.6, 1.95), xg_n=(17, 17),
         momios=[
             [2.49, 3.97, 2.54, "Pinnacle"],
             [2.50, 3.90, 2.45, "bet365"],
             [2.38, 3.75, 2.45, "William Hill"],
             [2.40, 3.96, 2.46, "Marathonbet"],
             [2.50, 3.95, 2.52, "Betano"],
             [2.38, 4.00, 2.38, "BetVictor"],
             [2.45, 4.20, 2.55, "Dafabet"],
             [2.40, 4.00, 2.45, "Betfair Sportsbook (etiqueta 'Betfair')"],
             [2.40, 3.85, 2.45, "DraftKings"],
             [2.45, 4.00, 2.45, "FanDuel"],
             [2.37, 4.00, 2.45, "BetMGM"],
             [2.25, 3.95, 2.65, "BetRivers"],
             [2.33, 4.00, 2.49, "Stake"],
         ]),
]

# tabla oficial de multiples de Media Semana: hasta 3 dobles con 0, 1 o 2 triples
MEDIA_SEMANA = {"precio": 15, "max_dobles": {0: 3, 1: 3, 2: 3}}

PESOS_SELECCION = {"mercado": 0.75, "elo": 0.25}
PESOS_CLUB = {"mercado": 0.80, "poisson": 0.20}
GOLES_ELO = 2.81   # goles por partido de la muestra de selecciones usada en el concurso 2359
MIN_XG = 8         # partidos minimos por lado para que el xG entre al Poisson
TOPE = 1100        # pesos, fijado por el usuario el 16-nov
