"""
Progol 2360. Entradas del modelo, version ligera (tope de consumo fijado por el usuario).

Lista de partidos: boleta de la app oficial que mando el usuario el 20-nov-2026 a las 13:54
(bolsa $5,000,000), igual a la boleta oficial leida el 16-nov. Venta hasta el viernes 20-nov
a las 21:00. Quiniela sencilla $15.

Momios: promedio 1X2 de betexplorer por partido, paginas /fixtures/ de cada competencia,
leidas el 20-nov-2026 a las 13:55 CDMX. El cuarto numero es cuantas casas promedia.
Es UNA lectura por partido, sin fila por casa y sin segunda comprobacion. Sin Elo (son
clubes) y sin xG (no se busco). El partido 14 trae una sola casa.
Porcentajes de venta del publico: NO BUSCADOS.
"""

PARTIDOS = [
    dict(id="P1", local="Juarez", visita="Atlas", momios=[3.67, 3.55, 1.89], casas=15),
    dict(id="P2", local="Pachuca", visita="Toluca", momios=[2.63, 3.84, 2.22], casas=15),
    dict(id="P3", local="Santos Laguna", visita="Leon", momios=[2.31, 3.59, 2.64], casas=15),
    dict(id="P4", local="Pumas", visita="Monterrey", momios=[2.50, 3.46, 2.50], casas=15),
    dict(id="P5", local="Tigres", visita="America", momios=[3.29, 3.51, 2.00], casas=15),
    dict(id="P6", local="Guadalajara", visita="Cruz Azul", momios=[2.18, 3.84, 2.70], casas=15),
    dict(id="P7", local="Sevilla", visita="Betis", momios=[3.03, 3.38, 2.33], casas=4),
    dict(id="P8", local="Coventry", visita="Crystal Palace", momios=[2.44, 3.46, 2.73], casas=4),
    dict(id="P9", local="Elversberg", visita="Friburgo", momios=[3.45, 3.75, 1.97], casas=4),
    dict(id="P10", local="Estrasburgo", visita="Brest", momios=[2.19, 3.65, 3.03], casas=4),
    dict(id="P11", local="Lille", visita="Lyon", momios=[2.20, 3.28, 3.28], casas=4),
    dict(id="P12", local="Lorient", visita="Rennes", momios=[2.83, 3.46, 2.38], casas=4),
    dict(id="P13", local="Palmeiras", visita="Flamengo", momios=[4.24, 3.77, 1.77], casas=3),
    dict(id="P14", local="At. Mineiro", visita="Boca Jrs", momios=[3.40, 3.00, 2.28], casas=1),
]
TOPE = 1100
