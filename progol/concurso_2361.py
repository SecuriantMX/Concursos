"""
Progol 2361. Entradas del modelo, modo completo (el usuario activo los flujos de agentes el 27-nov).

Concurso, lista y cierre: mascarilla oficial de Loteria Nacional del 22-nov-2026 ("Proximo concurso
No. 2361, a la venta del lunes 23 al viernes 27 de noviembre de 2026 hasta las 21:00 horas; juegos
del sabado 28 al domingo 29"), confirmada por la cuenta oficial de Facebook el 25-nov. La lista
coincide con la captura de la app que mando el usuario el 27-nov a las 19:03: mismos 14 partidos,
mismo orden y mismo local. Quiniela sencilla $15. Bolsa anunciada: 8.9 millones.

Momios: una fila por casa, mercado 1X2 a 90 minutos, leidos el 27-nov-2026 entre las 19:10 y las
19:16 CDMX por un agente por cada par de partidos (steamwatch, oddsrun, oddsforge, oddsmath,
betexplorer). Un segundo agente releyo filas, local y horario de cada lectura; su veredicto y su
precio de referencia van en el comentario de cada partido. Se descartan promedios de comparador,
intercambios, margenes fuera de 1% a 15%, casas repetidas y ternas identicas a la de otra casa.

xG: footystats.org, columnas At Home / At Away de la competencia en curso, con el numero de
partidos de la muestra (xg_n). El Poisson solo entra cuando cada lado tiene al menos MIN_XG
partidos; en las ligas europeas van 5 a 7 jornadas por lado y no alcanza.

Porcentajes de venta del publico: NO LEIDOS. Loteria Nacional los publica como imagen
(loterianacional.gob.mx/Progol/Momios) y no se pudo abrir en esta sesion.

Particularidades de la jornada (segun las fuentes de calendario de cada lectura):
  P1 y P2 son la vuelta de cuartos de Liga MX (idas: Monterrey 0-0 America, Toluca 2-0 Atlas).
  P3 es la vuelta de la final de la Liga de Expansion (ida: Morelia 4-1 La Paz).
  P4 es cuartos de final del Campeonato Concacaf W, partido unico en sede neutral (Mansfield, Texas).
  P14 es el juego 2 de una serie al mejor de tres de los playoffs de MLS.
En todos cuenta solo el marcador a 90 minutos.
"""

PARTIDOS = [
    # P1: Liga MX Apertura 2026 / Cuartos de final, vuelta. 2026-11-28 21:10. Estadio Banorte, Ciudad de Mexico (asi lo nombran tvazteca y excelsior; titan007 lo llama 'Mexico City Stadium' y footballnation 'Estadio Azteca'). Lectura: 2026-11-27 19:16
    #   promedio del comparador (no entra al calculo): 2.11/3.12/3.47 con 16 casas
    #   fila descartada: FanDuel: terna identica a otra casa
    #   fila descartada: BetMGM: terna identica a otra casa
    #   fila descartada: Betway: terna identica a otra casa
    #   fuente: https://1x2d.titan007.com/3116378.js
    dict(id='P1', local='America', visita='Monterrey', tipo='club', neutral=False,
         xg=(2.1, 1.39, 1.39, 1.41), xg_n=(8, 9),  # https://footystats.org/clubs/cf-monterrey-1430 ; https://footystats.org/clubs/club-america-1420
         momios=[
             [2.16, 3.08, 3.84, 'Pinnacle'],
             [2.15, 3.25, 3.6, 'bet365'],
             [2.12, 3.05, 3.57, '1xBet'],
             [2.1, 3.05, 3.54, 'Marathonbet'],
             [2.1, 3.1, 3.8, 'Betfair Sportsbook'],
             [2, 3.25, 3.1, 'William Hill'],
             [2.23, 3, 3.25, 'Unibet'],
             [2.2, 3.3, 3.2, 'bwin'],
             [2.15, 3.1, 3.6, 'DraftKings'],
             [2.15, 3.05, 3.25, 'Codere'],
             [2.05, 3.5, 3.25, 'Betano'],
         ]),
    # P2: Liga MX Apertura 2026 / Cuartos de final, vuelta. 2026-11-28 19:00. Estadio Jalisco, Guadalajara. Lectura: 2026-11-27 19:16
    #   promedio del comparador (no entra al calculo): 2.91/3.63/2.15 con 16 casas
    #   fila descartada: BetMGM: terna identica a otra casa
    #   fuente: https://1x2d.titan007.com/3116377.js
    #   fuente: https://www.betexplorer.com/football/mexico/liga-mx/atlas-toluca/rP4cBDo4/1x2/
    dict(id='P2', local='Atlas', visita='Toluca', tipo='club', neutral=False,
         xg=(1.46, 1.5, 1.53, 1.75), xg_n=(9, 9),  # https://footystats.org/clubs/csyd-atlas-de-guadalajara-1421 ; https://footystats.org/mexico/csyd-atlas-de-guadalajara-vs-deportivo-toluca
         momios=[
             [3.08, 3.86, 2.21, 'Pinnacle'],
             [3.1, 3.8, 2.15, 'bet365'],
             [2.87, 3.58, 2.21, '1xBet'],
             [2.85, 3.58, 2.19, 'Marathonbet'],
             [2.9, 3.75, 2.2, 'Betfair Sportsbook'],
             [2.8, 3.4, 2.1, 'William Hill'],
             [3, 3.55, 2.1, 'Unibet'],
             [2.87, 3.75, 2.15, 'bwin'],
             [2.95, 3.8, 2.15, 'DraftKings'],
             [2.95, 3.7, 2.2, 'FanDuel'],
             [2.85, 3.6, 2.1, 'Codere'],
             [2.9, 3.8, 2.15, 'Betway'],
             [2.92, 3.7, 2.22, 'Betano'],
         ]),
    # P3: Liga de Expansion MX, Apertura 2026 / Final, partido de vuelta (ida: Atl. Morelia 4-1 Atletico La Paz, segun betexplorer). 2026-11-28 21:00 (sabado). Estadio Guaycura, La Paz, Baja California Sur. Lectura: 2026-11-27 19:11
    #   promedio del comparador (no entra al calculo): 1.93/3.37/3.52 con 14 casas
    #   fila descartada: SBOBET: margen 17.0% fuera de 1% a 15%
    #   fila descartada: Bettogoal: terna identica a otra casa
    #   fuente: https://www.oddsmath.com/api/v1/live-odds.json/?event_id=5154097&cat_id=0&include_exchanges=1&language=en&country_code=MX
    dict(id='P3', local='La Paz', visita='Morelia', tipo='club', neutral=False,
         momios=[
             [1.95, 3.48, 3.58, '1xBet'],
             [1.93, 3.48, 3.56, 'Marathonbet'],
             [1.95, 3.5, 3.6, 'Betway'],
             [1.88, 3.25, 3.45, 'Suprabets'],
             [1.9, 3.25, 3.5, 'FEZbet'],
         ]),
    # P4: Campeonato Concacaf W 2026 (CONCACAF W Championship), selecciones mayores femeniles; otorga boleto al Mundial Femenil Brasil 2027 / Cuartos de final, partido unico a eliminacion directa. 2026-11-28 15:30 (sabado). Texas Health Mansfield Stadium, Mansfield, Texas, Estados Unidos. Lectura: 2026-11-27 19:12
    #   promedio del comparador (no entra al calculo): 1.16/5.86/12.1 con 5 casas
    #   fila descartada: Marathonbet: terna identica a otra casa
    #   fila descartada: Bettogoal: terna identica a otra casa
    #   fuente: https://www.oddsmath.com/api/v1/live-odds.json/?event_id=5161278&cat_id=0&include_exchanges=1&language=en&country_code=MX
    dict(id='P4', local='Mexico Femenil', visita='Haiti Femenil', tipo='seleccion', neutral=True,
         momios=[
             [1.122, 6.4, 13.5, '1xBet'],
             [1.19, 5.4, 11, 'Suprabets'],
             [1.17, 5.66, 12, 'FEZbet'],
         ]),
    # P5: LaLiga 2026-27 / Jornada 14 (fase regular). 2026-11-29 11:30 (domingo; 17:30 UTC / 18:30 CET). Abanca-Balaidos (Estadio Municipal de Balaidos), Vigo. Lectura: 2026-11-27 19:10-19:15
    #   promedio del comparador (no entra al calculo): 2.72/3.49/2.48 con 10 casas
    #   referencia del segundo lector: 2.78/3.59/2.56 (Pinnacle (fila de referencia) en comparador justgobet, mercado 'Winner)
    #   fila descartada: Coral: terna identica a otra casa
    #   fila descartada: Paddy Power: terna identica a otra casa
    #   fila descartada: Betfred: terna identica a otra casa
    #   fuente: https://oddsforge.co.uk/football/la-liga/celta-vigo-vs-villarreal-2026-11-29
    #   fuente: https://oddsrun.com/match/football/es/38223/13428688/spain-la-liga/celta-vigo-vs-villarreal/
    #   fuente: https://www.steamwatch.io/match/20c78c2ef75c4a6d7f4af81dd32e97cd
    dict(id='P5', local='Celta', visita='Villarreal', tipo='club', neutral=False,
         xg=(1.39, 1.45, 1.66, 1.52), xg_n=(7, 7),  # https://footystats.org/clubs/real-club-celta-de-vigo-281 ; https://footystats.org/clubs/villarreal-cf-76
         momios=[
             [2.78, 3.59, 2.56, 'Pinnacle'],
             [2.8, 3.4, 2.5, 'bet365'],
             [2.83, 3.63, 2.59, '1xBet'],
             [2.75, 3.54, 2.52, 'Marathonbet'],
             [2.75, 3.5, 2.5, 'Betfair Sportsbook'],
             [2.7, 3.3, 2.45, 'William Hill'],
             [2.75, 3.5, 2.45, 'bwin'],
             [2.75, 3.55, 2.5, 'DraftKings'],
             [2.7, 3.5, 2.45, 'Ladbrokes'],
             [2.7, 3.4, 2.45, 'Sky Bet'],
             [2.62, 3.5, 2.4, 'Betway'],
         ]),
    # P6: Premier League 2026-27 / Jornada 12 (fase regular). 2026-11-29 08:05. Craven Cottage, Londres (dato de fragmentos de buscador: https://matchesnow.co.uk/leagues/premier-league/2026/fulham-bournemouth y https://soccernet.ng/2026/11/fulham-vs-bournemouth-preview-team-news-h2h.html). Lectura: 2026-11-27 19:16
    #   promedio del comparador (no entra al calculo): 2.83/3.41/2.43 con 4 casas
    #   fila descartada: Coral: terna identica a otra casa
    #   fuente: https://www.oddschecker.com/football/english/premier-league/fulham-v-bournemouth/winner
    #   fuente: https://www.sportytrader.com/en/odds/fulham-bournemouth-8558927/
    #   fuente: https://www.steamwatch.io/match/56ea91809ff11d3a67557a21b3371cb9
    #   fuente: https://www.tempoodds.com/games/bournemouth-at-fulham-2026-11-29
    dict(id='P6', local='Fulham', visita='Bournemouth', tipo='club', neutral=False,
         xg=(1.67, 1.532, 1.556, 1.316), xg_n=(5, 5),  # https://www.statmuse.com/fc/ask/bournemouth-total-expected-goals-away-in-the-premier-league-this-season ; https://www.statmuse.com/fc
         momios=[
             [2.91, 3.53, 2.48, 'Pinnacle'],
             [2.8, 3.3, 2.5, 'bet365'],
             [2.88, 3.72, 2.51, '1xBet'],
             [2.875, 3.4, 2.45, 'Betfair Sportsbook'],
             [2.7, 3.5, 2.4, 'William Hill'],
             [2.8, 3.4, 2.5, 'Unibet (UK)'],
             [2.8, 3.5, 2.5, 'DraftKings'],
             [2.9, 3.4, 2.45, 'FanDuel'],
             [2.7, 3.5, 2.5, 'BetMGM (EE.UU.)'],
             [2.7, 3.4, 2.5, 'Ladbrokes'],
             [2.75, 3.4, 2.5, 'Betfred'],
             [2.75, 3.4, 2.4, 'Betway'],
             [2.75, 3.5, 2.4, 'BoyleSports'],
         ]),
    # P7: Premier League 2026-27 / Jornada 12 (fase regular). 2026-11-29 10:30. Emirates Stadium, Londres. Lectura: 2026-11-27 19:16
    #   promedio del comparador (no entra al calculo): 1.96/3.65/3.66 con 4 casas
    #   fila descartada: Betway: terna identica a otra casa
    #   fuente: https://www.oddschecker.com/football/english/premier-league/arsenal-v-man-city/winner
    #   fuente: https://www.sportytrader.com/en/odds/arsenal-manchester-city-8558923/
    #   fuente: https://www.steamwatch.io/match/d20ede55e54ed7b55fdc36ca373727c0
    #   fuente: https://www.tempoodds.com/games/manchester-city-at-arsenal-2026-11-29
    dict(id='P7', local='Arsenal', visita='Man. City', tipo='club', neutral=False,
         xg=(1.916, 0.464, 1.502, 0.826), xg_n=(5, 5),  # https://www.statmuse.com/fc/ask/arsenal-total-expected-goals-at-home-in-the-premier-league-this-season ; https://www.statmuse.com/fc
         momios=[
             [2.01, 3.73, 3.76, 'Pinnacle'],
             [1.95, 3.6, 3.8, 'bet365'],
             [2.06, 3.87, 3.7, '1xBet'],
             [2, 3.6, 3.75, 'Betfair Sportsbook'],
             [1.95, 3.6, 3.5, 'William Hill'],
             [2, 3.6, 3.6, 'Unibet (UK)'],
             [2, 3.7, 3.6, 'DraftKings'],
             [2, 3.6, 3.7, 'FanDuel'],
             [1.98, 3.75, 3.5, 'BetMGM (EE.UU.)'],
             [1.95, 3.6, 3.6, 'Paddy Power'],
             [2, 3.5, 3.6, 'Sky Bet'],
             [1.95, 3.7, 3.5, 'Ladbrokes'],
             [2, 3.75, 3.5, 'Coral'],
         ]),
    # P8: Serie A 2026-27 / Jornada 13 (fase regular). 2026-11-29 13:45 (domingo; 19:45 UTC / 20:45 CET). Stadio Giuseppe Sinigaglia, Como. Lectura: 2026-11-27 19:10-19:15
    #   promedio del comparador (no entra al calculo): 1.96/3.54/3.73 con 16 casas
    #   referencia del segundo lector: 2.04/3.53/3.89 (Pinnacle (fila de referencia) en comparador justgobet, mercado 'Winner)
    #   fila descartada: Ladbrokes: terna identica a otra casa
    #   fila descartada: Coral: terna identica a otra casa
    #   fuente: https://oddsforge.co.uk/football/serie-a/como-vs-juventus-2026-11-29
    #   fuente: https://oddsrun.com/match/football/it/199/11997927/italy-serie-a/como-vs-juventus/
    #   fuente: https://www.steamwatch.io/match/3876ad367184af2f8fc04a544fc894aa
    dict(id='P8', local='Como', visita='Juventus', tipo='club', neutral=False,
         xg=(2.04, 0.87, 2.01, 1.32), xg_n=(5, 6),  # https://footystats.org/clubs/calcio-como-518 ; https://footystats.org/clubs/juventus-fc-90
         momios=[
             [2.04, 3.53, 3.89, 'Pinnacle'],
             [1.91, 3.6, 4, 'bet365'],
             [1.95, 3.74, 3.76, 'Marathonbet'],
             [2, 3.5, 3.9, 'Betfair Sportsbook'],
             [1.95, 3.4, 3.5, 'William Hill'],
             [1.98, 3.5, 3.75, 'Unibet'],
             [1.95, 3.6, 3.7, 'bwin'],
             [1.95, 3.45, 3.65, 'DraftKings'],
             [1.95, 3.5, 3.8, 'Paddy Power'],
             [1.95, 3.4, 3.75, 'Sky Bet'],
             [1.95, 3.4, 3.6, 'Betway'],
             [1.95, 3.6, 3.75, 'Betfred'],
         ]),
    # P9: Bundesliga 2026-27 / Jornada 11 (fase regular). 2026-11-29 08:30 (domingo; 14:30 UTC / 15:30 CET). Europa-Park Stadion, Freiburg im Breisgau, Alemania. Lectura: 2026-11-27 19:13 (lecturas entre 19:10 y 19:14)
    #   promedio del comparador (no entra al calculo): 2.7/3.83/2.35 con 10 casas
    #   fila descartada: Ladbrokes: terna identica a otra casa
    #   fila descartada: Coral: terna identica a otra casa
    #   fuente: https://oddsrun.com/match/football/de/123/12153818/germany-bundesliga-i/sc-freiburg-vs-rb-leipzig/
    #   fuente: https://singlebet.net/odds/freiburg-vs-rb-leipzig-2026-11-29-3886766
    #   fuente: https://www.steamwatch.io/match/2aa9aa95157eb36fed45135c995cdd80
    dict(id='P9', local='Friburgo', visita='Leipzig', tipo='club', neutral=False,
         xg=(1.77, 0.87, 2.738, 1.646), xg_n=(5, 5),  # https://www.statmuse.com/fc/ask/freiburg-total-expected-goals-at-home-in-the-bundesliga-this-season ; https://www.statmuse.com/fc/ask/
         momios=[
             [2.81, 3.98, 2.36, 'Pinnacle'],
             [2.7, 3.75, 2.38, 'bet365'],
             [2.83, 3.92, 2.46, '1xBet'],
             [2.75, 3.82, 2.39, 'Marathonbet'],
             [2.7, 4, 2.3, "Betfair Sportsbook (la fuente la rotula solo 'Betfair')"],
             [2.6, 3.9, 2.37, 'bwin'],
             [2.65, 3.7, 2.3, 'DraftKings'],
             [2.72, 3.8, 2.37, 'Betano'],
             [2.73, 3.78, 2.37, 'Melbet'],
             [2.75, 3.9, 2.35, 'Fonbet'],
             [2.7, 3.9, 2.37, 'Dafabet'],
             [2.71, 3.8, 2.28, 'Vbet'],
         ]),
    # P10: Ligue 1 2026-27 / Jornada 12. 2026-11-29 10:15. Stadium de Toulouse. Lectura: 2026-11-27 19:14
    #   promedio del comparador (no entra al calculo): 2.42/3.59/2.73 con 16 casas
    #   fuente: https://www.steamwatch.io/match/71c08940a73e9f42d503449f052a1bdf
    #   fuente: https://www.wincomparator.com/predictions/toulouse-rennes-8532504/
    dict(id='P10', local='Toulouse', visita='Rennes', tipo='club', neutral=False,
         xg=(1.858, 1.286, 1.866, 2.616), xg_n=(5, 5),  # https://statz.ai/team/rennes ; https://statz.ai/team/toulouse
         momios=[
             [2.44, 3.72, 2.84, 'Pinnacle'],
             [2.45, 3.6, 2.7, 'bet365'],
             [2.56, 3.74, 2.8, '1xBet'],
             [2.38, 3.5, 2.62, 'William Hill'],
             [2.48, 3.55, 2.6, 'Unibet'],
             [2.4, 3.6, 2.75, 'bwin'],
             [2.3, 3.6, 2.75, 'Betway'],
             [2.42, 3.55, 2.75, 'Betsson'],
             [2.28, 3.6, 2.75, 'Stake'],
             [2.47, 3.6, 2.7, '22bet'],
             [2.55, 3.7, 2.56, 'Melbet'],
             [2.38, 3.4, 2.6, 'Betfred'],
             [2.41, 3.55, 2.75, 'Tonybet'],
             [2.42, 3.55, 2.72, 'BC Game'],
         ]),
    # P11: Ligue 1 2026-27 / Jornada 12. 2026-11-29 13:45. Groupama Stadium (wincomparator lo nombra Parc Olympique Lyonnais), Lyon. Lectura: 2026-11-27 19:14
    #   promedio del comparador (no entra al calculo): 2.35/3.35/2.99 con 16 casas
    #   fila descartada: Melbet: terna identica a otra casa
    #   fuente: https://www.steamwatch.io/match/ca8aa566e27e1d05b47e8151b2066f9a
    #   fuente: https://www.wincomparator.com/predictions/lyon-monaco-8532501/
    dict(id='P11', local='Lyon', visita='Monaco', tipo='club', neutral=False,
         xg=(2.284, 0.878, 1.07, 1.598), xg_n=(5, 6),  # https://statz.ai/team/monaco ; https://statz.ai/team/olympique-lyonnais
         momios=[
             [2.44, 3.34, 3.11, 'Pinnacle'],
             [2.3, 3.4, 3, 'bet365'],
             [2.41, 3.59, 3.1, '1xBet'],
             [2.3, 3.3, 2.9, 'William Hill'],
             [2.23, 3.4, 3, 'Unibet'],
             [2.35, 3.4, 2.95, 'bwin'],
             [2.38, 3.25, 2.9, 'Betway'],
             [2.38, 3.25, 3, 'Betsson'],
             [2.24, 3.35, 3, 'Stake'],
             [2.33, 3.46, 2.99, '22bet'],
             [2.3, 3.2, 2.88, 'Betfred'],
             [2.37, 3.35, 2.95, 'Tonybet'],
             [2.36, 3.3, 2.98, 'BC Game'],
         ]),
    # P12: Eredivisie 2026-27 / Jornada 14 (fase regular). 2026-11-29 07:30 (domingo; 13:30 UTC / 14:30 CET). De Kuip (Stadion Feijenoord), Rotterdam, Paises Bajos. Lectura: 2026-11-27 19:13 (lecturas entre 19:10 y 19:13)
    #   promedio del comparador (no entra al calculo): 2.21/3.88/2.8 con 10 casas
    #   fila descartada: Coral: terna identica a otra casa
    #   fuente: https://oddsrun.com/match/football/nl/66/12026853/netherlands-eredivisie/feyenoord-vs-ajax/
    #   fuente: https://www.singlebet.net/odds/feyenoord-vs-ajax-2026-11-29-3861791/
    dict(id='P12', local='Feyenoord', visita='Ajax', tipo='club', neutral=False,
         xg=(2.277, 1.058, 2.222, 1.42), xg_n=(6, 6),  # https://statz.ai/team/ajax ; https://statz.ai/team/feyenoord
         momios=[
             [2.23, 3.99, 2.87, 'Pinnacle'],
             [2.2, 4, 2.8, 'bet365'],
             [2.26, 3.96, 2.88, '1xBet'],
             [2.19, 3.84, 2.79, 'Marathonbet'],
             [2.15, 4, 2.88, "Betfair Sportsbook (la fuente la rotula solo 'Betfair')"],
             [2.2, 4, 2.87, 'bwin'],
             [2.2, 3.95, 2.8, 'DraftKings'],
             [2.15, 3.9, 2.87, 'Ladbrokes'],
             [2.22, 4, 2.85, 'Betano'],
             [2.23, 3.92, 2.85, 'Melbet'],
             [2.18, 3.95, 2.8, 'Fonbet'],
             [2.15, 4, 3, 'Dafabet'],
             [2.19, 3.89, 2.81, 'Vbet'],
         ]),
    # P13: Campeonato Brasileiro Serie A 2026 / Rodada 37 de 38 (fase unica, liga). 2026-11-29 15:30. Estadio Jose Maria de Campos Maia (Maiao), Mirassol (SP), Brasil. Lectura: 2026-11-27 19:12
    #   promedio del comparador (no entra al calculo): 2.03/3.48/3.52 con 3 casas
    #   referencia del segundo lector: 2.05/3.71/3.5 (tipy1x2.com, bloque de cabecera del partido (Mirassol local, Regular S)
    #   fila descartada: Bettogoal: invalida segun el segundo lector: Probable clon de Suprabets, no una linea independiente: precios identicos (1.96 / 3.51 / 3.50), todo el historial identi
    #   fuente: https://www.betexplorer.com/match-odds-old/8b9sgtZa/1/1x2/1/en/
    #   fuente: https://www.oddsmath.com/api/v1/live-odds.json/?event_id=5154704&cat_id=0&include_exchanges=1&language=en&country_code=MX
    dict(id='P13', local='Mirassol', visita='Paranaense', tipo='club', neutral=False,
         momios=[
             [2, 3.4, 3.75, 'bet365 (bet365.us)'],
             [2.1, 3.6, 3.3, 'BetMGM (BetMGM.us)'],
             [1.98, 3.45, 3.5, 'Stake.com'],
             [2.052, 3.71, 3.505, '1xBet'],
             [1.99, 3.6, 3.4, 'Marathonbet'],
             [2.14, 3.62, 3.665, 'BetInAsia'],
             [2, 3.6, 3.4, 'Betway'],
             [2.05, 3.5, 3.6, 'FEZbet'],
             [1.96, 3.51, 3.5, 'Suprabets'],
         ]),
    # P14: MLS 2026 - Audi MLS Cup Playoffs / Round One (Conferencia Este), serie al mejor de 3, Juego 2. NO es eliminacion directa a partido unico: Charlotte lidera la serie 1-0. 2026-11-28 11:30. Bank of America Stadium, Charlotte, North Carolina, EE.UU.. Lectura: 2026-11-27 19:12
    #   promedio del comparador (no entra al calculo): 2.63/3.74/2.36 con 10 casas
    #   referencia del segundo lector: 2.74/3.84/2.34 (Melbet, tabla 'Best Betting Odds' de sportytrader: https://www.sportyt)
    #   fila descartada: Bettogoal: invalida segun el segundo lector: Probable clon de Suprabets, no una linea independiente: precios identicos (2.60 / 3.64 / 2.37), historial identico y mis
    #   fuente: https://www.betexplorer.com/match-odds-old/CvDzX0Ok/1/1x2/1/en/
    #   fuente: https://www.oddsmath.com/api/v1/live-odds.json/?event_id=5156416&cat_id=0&include_exchanges=1&language=en&country_code=MX
    dict(id='P14', local='Charlotte', visita='Chicago', tipo='club', neutral=False,
         momios=[
             [2.63, 3.9, 2.4, 'bet365 (bet365.us)'],
             [2.55, 3.9, 2.35, 'BetMGM (BetMGM.us)'],
             [2.6, 3.8, 2.4, 'FanDuel'],
             [2.6, 3.75, 2.31, 'Stake.com'],
             [2.796, 3.92, 2.39, '1xBet'],
             [2.68, 3.76, 2.29, 'Marathonbet'],
             [2.682, 3.854, 2.45, 'BetInAsia'],
             [2.625, 3.75, 2.4, 'Betway'],
             [2.6, 3.8, 2.36, 'FEZbet'],
             [2.6, 3.64, 2.37, 'Suprabets'],
         ]),
]

PESOS_SELECCION = {"mercado": 0.75, "elo": 0.25}
PESOS_CLUB = {"mercado": 0.80, "poisson": 0.20}
GOLES_ELO = 2.81   # no se usa en este concurso: no hay selecciones con rating Elo
MIN_XG = 8         # partidos minimos por lado para que el xG entre al Poisson
TOPE = 1100        # pesos, fijado por el usuario
