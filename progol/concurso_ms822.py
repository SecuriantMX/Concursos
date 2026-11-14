"""
Progol Media Semana 822 (juegos del 17 al 19 de noviembre de 2026).
Boleta oficial: loterianacional.gob.mx/ProgolMediaSemana/Quiniela, venta hasta el martes 17 a las 13:00.
Reglas de multiples (ProgolMediaSemana/Coperacha): sencilla $15, hasta 3 dobles y 2 triples.

PRELIMINAR del 14-nov-2026 11:50 CDMX. None o lista vacia = NO ENCONTRADO todavia.
Momios: betexplorer.com (promedio de las casas listadas). Elo: eloratings.net World.tsv.
"""
PARTIDOS = [
    dict(id="M1", local="Mexico", visita="Jamaica", tipo="seleccion", neutral=False, momios=[], elo=(1868, 1543)),
    dict(id="M2", local="Arsenal F", visita="Lyon F", tipo="club", neutral=False, momios=[]),
    dict(id="M3", local="Dinamarca", visita="Noruega", tipo="seleccion", neutral=False, momios=[], elo=(1861, 1901)),
    dict(id="M4", local="Polonia", visita="Suecia", tipo="seleccion", neutral=False, momios=[[2.30, 3.40, 2.90]], elo=(1685, 1774)),
    # Elo de Kosovo tomado del codigo "KO" del archivo; falta verificar que ese codigo sea Kosovo
    dict(id="M5", local="Rep. Irlanda", visita="Kosovo", tipo="seleccion", neutral=False, momios=[[1.95, 3.28, 4.10]], elo=(1711, 1700)),
    dict(id="M6", local="Cruzeiro", visita="Palmeiras", tipo="club", neutral=False, momios=[]),
    dict(id="M7", local="Corinthians", visita="Botafogo", tipo="club", neutral=False, momios=[]),
    dict(id="M8", local="Sao Paulo", visita="Fluminense", tipo="club", neutral=False, momios=[]),
    dict(id="M9", local="Orlando", visita="Cincinnati", tipo="club", neutral=False, momios=[[2.41, 3.98, 2.46]]),
]
MEDIA_SEMANA = {"precio": 15, "max_dobles": {0: 3, 1: 3, 2: 3}}
PESOS = {"mercado": 0.75, "elo": 0.25}
