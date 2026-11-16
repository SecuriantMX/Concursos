"""
Progol Media Semana 822 (juegos del 17 al 19 de noviembre de 2026).
Boleta oficial: loterianacional.gob.mx/ProgolMediaSemana/Quiniela, venta hasta el martes 17 a las 13:00.
Reglas de multiples (ProgolMediaSemana/Coperacha): sencilla $15, hasta 3 dobles y 2 triples.

Datos del 15-nov-2026 ~20:15 CDMX. Lista vacia o None = NO ENCONTRADO.
Momios: betexplorer.com, promedio de las casas listadas (entre 2 y 4 por partido).
Elo: eloratings.net World.tsv leido el 15-nov; codigos verificados en en.teams.tsv (KO = Kosovo).
Porcentajes de venta del 822: NO ENCONTRADO (la imagen oficial seguia mostrando el concurso 821).
"""
PARTIDOS = [
    dict(id="M1", local="Mexico", visita="Jamaica", tipo="seleccion", neutral=False,
         momios=[[1.21, 5.55, 11.00]], elo=(1837, 1574)),
    dict(id="M2", local="Arsenal F", visita="Lyon F", tipo="club", neutral=False, momios=[]),
    dict(id="M3", local="Dinamarca", visita="Noruega", tipo="seleccion", neutral=False,
         momios=[[2.38, 3.67, 2.67]], elo=(1920, 1909)),
    dict(id="M4", local="Polonia", visita="Suecia", tipo="seleccion", neutral=False,
         momios=[[2.30, 3.40, 2.90]], elo=(1663, 1784)),   # momio leido el 14-nov, una sola casa
    dict(id="M5", local="Rep. Irlanda", visita="Kosovo", tipo="seleccion", neutral=False,
         momios=[[1.95, 3.28, 4.10]], elo=(1703, 1700)),   # momio leido el 14-nov, dos casas
    dict(id="M6", local="Cruzeiro", visita="Palmeiras", tipo="club", neutral=False, momios=[[2.86, 3.48, 2.32]]),
    dict(id="M7", local="Corinthians", visita="Botafogo", tipo="club", neutral=False, momios=[[1.80, 3.62, 4.21]]),
    dict(id="M8", local="Sao Paulo", visita="Fluminense", tipo="club", neutral=False, momios=[[2.30, 3.22, 3.08]]),
    dict(id="M9", local="Orlando", visita="Cincinnati", tipo="club", neutral=False, momios=[[2.41, 3.98, 2.46]]),
]
MEDIA_SEMANA = {"precio": 15, "max_dobles": {0: 3, 1: 3, 2: 3}}
PESOS = {"mercado": 0.75, "elo": 0.25}
TOPE = 1000
