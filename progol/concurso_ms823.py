"""
Progol Media Semana 823. Entradas, version ligera (tope de consumo fijado por el usuario).

Lista de partidos: boleta de la app oficial que mando el usuario el 22-nov-2026 a las 16:22.
Los partidos 1 a 4 venian como "EQ8 LIGA MX - EQ1 LIGA MX", etc. Los equipos salen de la
tabla final del Apertura 2026 segun El Financiero (22-nov 19:28), ESPN y Mediotiempo:
1 Guadalajara, 2 Cruz Azul, 3 America, 4 Atlas, 5 Toluca, 6 Monterrey, 7 Leon, 8 Pachuca.
Deducido de la tabla y despues confirmado por la app oficial (captura del usuario).

Numero de concurso (823) y fechas de los partidos 5 a 9: quinielaganadora.com, leida el
23-nov. No es fuente oficial. Hora de cierre de venta: NO VERIFICADA.

Momios: promedio 1X2 de betexplorer, paginas /fixtures/ de Liga MX (etapa Play Offs,
cuartos de ida) y de Champions League. Segunda lectura, 23-nov-2026 a las 22:08 CDMX:
es la que se usa en los nueve partidos (3 casas en Liga MX, 4 en Champions). Sin fila por casa.
El usuario mando a las 22:08 una segunda captura de la app con los equipos de los partidos
1 a 4 ya escritos: Pachuca-Guadalajara, Leon-C. Azul, Monterrey-Aguilas, Toluca-Atlas.
Coinciden con lo deducido de la tabla, mismo local y visitante.
El local de betexplorer coincide con el de la boleta en los nueve partidos.
Sin Elo ni xG. Porcentajes de venta del publico: NO BUSCADOS.
"""

PARTIDOS = [
    dict(id="M1", local="Pachuca", visita="Guadalajara", momios=[2.65, 3.52, 2.46], casas=3),
    dict(id="M2", local="Leon", visita="Cruz Azul", momios=[3.17, 3.55, 2.11], casas=3),
    dict(id="M3", local="Monterrey", visita="America", momios=[2.29, 3.47, 2.86], casas=3),
    dict(id="M4", local="Toluca", visita="Atlas", momios=[1.41, 4.85, 6.40], casas=3),
    dict(id="M5", local="Arsenal", visita="Dortmund", momios=[1.41, 4.83, 6.76], casas=4),
    dict(id="M6", local="Feyenoord", visita="Porto", momios=[2.98, 3.65, 2.20], casas=4),
    dict(id="M7", local="Slavia Praga", visita="Villarreal", momios=[3.06, 3.84, 2.09], casas=4),
    dict(id="M8", local="Brujas", visita="Liverpool", momios=[4.33, 4.61, 1.62], casas=4),
    dict(id="M9", local="Sp. Lisboa", visita="Man. United", momios=[2.40, 3.70, 2.66], casas=4),
]

# primera lectura (23-nov 12:05 CDMX, 4 casas en todos), solo como registro; no entra al calculo
LECTURA_1 = {"M1": [2.59, 3.45, 2.48], "M2": [3.10, 3.51, 2.11], "M3": [2.42, 3.61, 2.59], "M4": [1.36, 4.98, 7.06],
             "M5": [1.38, 4.90, 7.23], "M6": [2.85, 3.61, 2.28], "M7": [3.10, 3.78, 2.10], "M8": [4.31, 4.59, 1.61],
             "M9": [2.38, 3.68, 2.66]}

# tabla oficial de multiples de Media Semana: sencilla $15, hasta 3 dobles y 2 triples
MEDIA_SEMANA = {"precio": 15, "max_dobles": {0: 3, 1: 3, 2: 3}}
TOPE = 1100
