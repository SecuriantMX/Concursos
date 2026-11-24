# Base Progol

Bitácora de lo que el modelo propuso contra lo que pasó. Se actualiza con cada auditoría diaria.

## Límite de consumo

Fijado por el usuario el 2026-11-19: como máximo 5% de su cuota de uso por día. El medidor no se puede ver desde la sesión, así que se trabaja en modo ligero por omisión: sin flujos de agentes ni subagentes, pocas búsquedas web (seis en la auditoría diaria) y respuestas cortas. Un trabajo grande, como armar una quiniela con investigación completa, se avisa antes con su costo aproximado y se hace solo si el usuario lo pide.

## Cómo se audita

1. Buscar en la web los marcadores de los partidos ya jugados y guardarlos con fuente en `resultados_<concurso>.json`. Cuenta el marcador a 90 minutos más compensación.
2. Correr `python3 auditoria.py <concurso>`. Calcula Brier y log-loss del modelo final, del mercado, del Elo, del Poisson y del público, cuenta aciertos por boleto y reescribe `historial.csv`.
3. Anotar aquí lo observado.

Cómo leer la tabla de `auditoria.py`:
- `final` es el modelo en todos los partidos jugados; `final*` es el modelo solo en los partidos que tienen mercado. Para comparar contra el mercado se usa `final*` o la línea "Modelo final contra mercado", que es pareada.
- El "acierto del favorito" no cuenta los partidos donde el estimador empata en el máximo (por ejemplo, un partido sin estimación con 1/3 para cada resultado).
- El público solo se califica cuando el porcentaje es el oficial de Lotería Nacional. Si no se publicó, queda vacío en `historial.csv`.
- Los aciertos de cada boleto se cuentan con los ids de la salida, así que sirve igual para Progol (P, R) y para Media Semana (M).
- `python3 pruebas.py` corre las pruebas del modelo, del armado y de la auditoría. Deben pasar antes de cada commit que toque código.

Notas prácticas:
- Una tarea programada puede llegar con horas o días de retraso si la sesión está caída. Pasó el 17-nov: la revisión de las 11:15 llegó el 19, dos días después del cierre. El boleto que vale es el último entregado con margen; una revisión de último minuto es un extra, no una garantía. Al despertar, lo primero es ver si se pasó algún cierre y decirlo.
- Los porcentajes de venta de Media Semana 822 se publicaron el martes a las 12:23, 37 minutos antes del cierre. No se puede contar con ellos para armar el boleto con tiempo. Para leerlos: captura de la página oficial, ampliar los renglones y comprobar que cada uno suma 100.
- Las páginas de resultados de temporada completa de betexplorer son enormes. Para marcadores conviene la nota de resumen de la jornada (UEFA, medios) o una búsqueda por partido.

## Cuándo se cambia un valor del modelo

- Los pesos de la mezcla (hoy 75% mercado y 25% Elo en selecciones; 80% mercado y 20% Poisson en clubes con xG) solo se mueven cuando el historial tiene al menos 60 partidos con ambos estimadores y la mejora en log-loss supera dos errores estándar. `auditoria.py` hace esa prueba sola.
- Una regla nueva entra a "Reglas vigentes" solo si el mismo patrón aparece en al menos tres concursos distintos. Antes de eso vive en "Observaciones".
- Un solo resultado no cambia nada.

## Reglas vigentes

Ninguna estadística todavía.

Decisión de diseño del 2026-11-16: el xG solo entra al Poisson de clubes cuando cada equipo tiene al menos 8 partidos en su corte (casa para el local, visita para el visitante) de la misma liga. Con menos, el partido se queda con el mercado. No sale de resultados; es para no meter al modelo muestras de 2 partidos.

Decisión de diseño aprobada por el usuario el 2026-11-15, a partir de Media Semana 822: si se juegan varios boletos en un concurso, deben diferir en los sencillos más inciertos. Se arma con `boletos.mejor_complemento`, que busca combinaciones que los boletos anteriores no cubren y exige al menos 2 partidos con picks sin traslape. No es una regla sobre probabilidades; es sobre cómo repartir el riesgo entre boletos.

## Observaciones (candidatas, sin confirmar)

| Fecha | Concurso | Observación | Veces vista |
|---|---|---|---|
| 2026-11-14 | 2359 | Amistoso de selecciones en sede neutral (Japón 3-2 Brasil): cayó el favorito del mercado, del Elo y del público. Brasil llegó sin jugadores de Flamengo ni Palmeiras y con cinco debutantes. Pregunta abierta: ¿en amistosos el mercado sobrevalora al favorito con plantel recortado? | 1 |
| 2026-11-15 | 2359 | Los tres boletos de Progol compartían el mismo pick sencillo en 8 de 14 partidos (P3, P4, P7, P8, P9, P10, P11, P13). Cuando fallaron P3, P11 y P13 cayeron los tres a la vez. No es un patrón estadístico sino de diseño: los boletos no estaban diversificados entre sí. Aprobado por el usuario el 15-nov; ver Reglas vigentes. | 1 |
| 2026-11-15 | 2359 | Los picks contra el público del boleto agresivo (P1 local o empate, P5 empate) fallaron los dos: ganaron los que el público prefería. Dos casos no dicen nada sobre la estrategia; se sigue midiendo. | 1 |
| 2026-11-17 | 2359 | Al cierre, en los 19 partidos con mercado, el porcentaje de venta del público tuvo mejor log-loss (0.931) que el mercado (0.973) y que el modelo (0.983). La ventaja pareada del público sobre el mercado es 0.041 ± 0.052: dentro del ruido. Un concurso no basta; si se repite en tres, probar el público como tercer estimador de la mezcla. | 1 |
| 2026-11-19 | 2359 y MS 822 | Los dobles L/V perdieron contra el empate en 3 de 5 partidos distintos (P14 y R5 en el 2359, M4 en Media Semana 822; ganaron P6 y M3). El modelo daba al empate entre 25% y 28% en cada uno, así que se esperaban 1.3. No es señal de que el modelo subestime el empate: en los 26 partidos con estimación hubo 4 empates contra 6.4 ± 2.2 esperados. Por ahora es mala suerte en dónde cayeron; se sigue contando. | 2 |

## Bitácora

### 2026-11-14, concurso 2359, corte 11:15 CDMX (1 de 21 partidos)

- P3 Japón 3-2 Brasil, salió L. El modelo le daba 23.6% a Japón; el favorito era Brasil con 52%.
- Los tres boletos de Progol llevaban V fijo en este partido, así que el máximo posible ya es 13 aciertos.
- Log-loss en ese partido: modelo 1.442, mercado 1.426, Elo 1.493, público 1.598. Con un partido no se concluye nada.
- Pesos: sin cambio (1 partido en el historial, mínimo 60).

### 2026-11-15, concurso 2359, corte 08:00 CDMX (13 de 21 partidos)

Resultados nuevos (12): P1 Querétaro 0-1 Monterrey (V), P2 Red Bulls 1-0 América (L), P5 Irlanda del Norte 1-0 Ucrania (L), P11 Mirassol 0-0 Atlético Mineiro (E), P12 Criciúma 0-1 Novorizontino (V), P13 Sport 3-0 Goiás (L), P14 Cerezo 1-1 Urawa (E), R1 Jamaica 3-2 México (L), R2 Georgia 0-2 Hungría (V), R3 Noruega 3-1 Gales (L), R4 Suecia 3-2 Bosnia (L), R7 Kashima 3-2 Yokohama (L).

Aciertos por boleto, sobre lo jugado:

| Boleto | Progol (8 jugados) | Máximo posible | Revancha (5 jugados) | Máximo posible |
|---|---|---|---|---|
| Conservador | 4 | 10 | 4 | 6 |
| Balanceado | 3 | 9 | 3 | 5 |
| Agresivo | 2 | 8 | 3 | 5 |

Modelo contra mercado (12 partidos con momios): log-loss 1.043 del modelo contra 1.026 del mercado; diferencia -0.012 ± 0.008 a favor del mercado. Brier 0.620 contra 0.609. El público sacó 1.003 de log-loss, mejor que ambos en esta muestra. Con 13 partidos ninguna de estas diferencias es concluyente.

Qué falló:
- P3, P11, P13: sencillos al favorito en los tres boletos; salió otro resultado. En P13 Goiás era favorito del mercado (49%) y perdió 3-0 ante un Sport que no se jugaba nada.
- R1: México era favorito con 64% y perdió 3-2 en Kingston; fallaron los tres boletos de Revancha.
- P14: el empate (25%) quedó fuera incluso del doble L/V del conservador.
- P1 y P5: el agresivo fue contra el público y ganó el favorito del público.

Qué funcionó: el triple en P2 y P12 cubrió dos resultados que no eran el más probable; R3, R4 y R7 salieron con el favorito.

Pesos: sin cambio (6 partidos con mercado y Elo en el historial, mínimo 60).

### 2026-11-16, concurso 2359, corte 07:50 CDMX (19 de 21 partidos)

Resultados nuevos (6): P4 Panamá 2-0 Curazao (L), P6 Chipre 1-4 Montenegro (V), P7 Bélgica 4-1 Italia (L), P8 España 2-3 Inglaterra (V), R5 Letonia 0-0 Armenia (E), R6 Croacia 2-1 Chequia (L). Faltan P9 y P10 (lunes).

| Boleto | Progol (12 jugados) | Máximo posible | Revancha (final, 7) |
|---|---|---|---|
| Conservador | 7 | 9 | 6 |
| Balanceado | 6 | 8 | 4 |
| Agresivo | 5 | 7 | 4 |

Ningún boleto de Progol puede llegar a 10 aciertos, que fue el último nivel premiado en el 2358. La Revancha quedó en 6 de 7 para el conservador; solo cobra si nadie hizo 7 (premios aún no publicados).

Modelo contra mercado (18 partidos): log-loss 1.003 contra 0.991, diferencia -0.007 ± 0.011, dentro del ruido. Público 0.961: sigue por delante de ambos en este concurso. Acierto del favorito: modelo 11 de 19, público 10 de 19.

Qué falló hoy: P8, España era favorita con 60% y perdió en casa; iba sencilla en los tres boletos. R5, el empate (28%) quedó fuera del doble L/V de dos boletos.
Qué funcionó: P4, P6 y P7 con el favorito; R6 Croacia.

Pesos: sin cambio (12 partidos con mercado y Elo, mínimo 60).

### 2026-11-16, revisión del código (sin resultados nuevos)

Dos revisores leyeron `modelo.py`, `boletos.py` y `auditoria.py`, y un segundo agente intentó refutar cada hallazgo. Quedaron seis defectos confirmados, ya corregidos. Ninguno cambiaba un boleto entregado.

| Archivo | Defecto | Efecto |
|---|---|---|
| `auditoria.py` | El renglón `final` incluía a P2 (sin momios, 1/3 parejo) y lo contaba como favorito acertado porque ganó el local | Cifras de la bitácora infladas, ver abajo |
| `auditoria.py` | Buscaba resultados con prefijos fijos P y R | El boleto de Media Semana (M1 a M9) habría salido con 0 aciertos |
| `auditoria.py` | Calificaba como "público" el relleno de 33/33/33 | Habría ensuciado la observación abierta sobre el público |
| `auditoria.py` | Un resultado vacío o mal escrito contaba como victoria local | Latente |
| `boletos.py` | `mejor_complemento` devolvía un boleto que no cumplía la separación mínima cuando no había ninguno válido | Latente (hoy nadie la llama) |
| `modelo.py` | `elo_1x2` se pegaba al borde con más de 558 puntos de diferencia de rating | Latente (el máximo usado es 363) |

Correcciones a cifras ya escritas en esta bitácora, concurso 2359:
- Corte del 16-nov: en los 18 partidos con mercado el modelo tuvo log-loss 0.998 (no 1.003, que era sobre 19) contra 0.991 del mercado. La diferencia pareada, -0.007 ± 0.011, estaba bien. Acierto del favorito: modelo 10 de 18, mercado 11 de 18, público 10 de 19.
- Corte del 15-nov: en los 12 partidos con mercado el modelo tuvo 1.038 (no 1.043, que era sobre 13).
- Las conclusiones no cambian: la diferencia con el mercado sigue dentro del ruido.

Segunda pasada, sobre las propias correcciones: otros dos revisores intentaron romperlas y recalcularon aparte el boleto de Media Semana 822. No hallaron ningún número equivocado ni regresión; `historial.csv` quedó idéntico byte a byte. Sí dejaron nueve hallazgos menores, todos atendidos:
- Cinco eran pruebas que no detectaban lo que decían probar. `pruebas.py` ahora afirma valores concretos (Shin contra un valor resuelto aparte, Elo hasta 600 puntos, aciertos de favorito, Brier a mano, Revancha, auditoría del 2359) y detecta 24 regresiones sembradas a propósito.
- `auditoria.py` avisa cuando un resultado está mal capturado o su clave no es un partido de la salida, en vez de ignorarlo en silencio; un público en ceros se trata como dato faltante; la etiqueta "sin favorito" distingue entre partido sin estimación y empate en el máximo.
- `boletos.py`: la búsqueda ya encuentra boleto cuando los triples obligados no coinciden con los partidos más parejos (antes devolvía None). No afectaba a ningún boleto entregado.

### 2026-11-17, concurso 2359, cierre (21 de 21 partidos)

Resultados nuevos (2): P9 Islas Feroe 1-0 Moldavia (L) y P10 Alemania 5-0 Países Bajos (L), cada uno con dos fuentes y confirmado por un segundo agente. Las 21 letras registradas coinciden con la combinación oficial de Lotería Nacional: Progol V L L L L V L V L L E V L E; Revancha L V L L E L L.

| Boleto | Progol: aciertos (esperados) | Revancha: aciertos (esperados) | ¿Cobró? |
|---|---|---|---|
| Conservador | 9 de 14 (8.9) | 6 de 7 (5.5) | No |
| Balanceado | 8 de 14 (8.7) | 4 de 7 (5.2) | No |
| Agresivo, el recomendado | 7 de 14 (8.5) | 4 de 7 (5.2) | No |

Premios oficiales (mascarilla del 16-nov, por quiniela sencilla):

| Juego | Aciertos | Quinielas ganadoras | Premio |
|---|---|---|---|
| Progol | 14 | 1 | $9,028,361.25 |
| Progol | 13 | 16 | $87,208.87 |
| Progol | 12 | 231 | $5,285.38 |
| Progol | 11 | 1,991 | $613.22 |
| Progol | 10 | 11,306 | $123.41 |
| Revancha | 7 | 3,748 | $859.54 |

Ningún boleto cobró: Progol paga desde 10 aciertos y el mejor hizo 9; Revancha solo paga 7 y el mejor hizo 6. Bolsa garantizada del Progol 2360: 5 millones.

Modelo contra mercado, en los 19 partidos con momios: log-loss 0.983 contra 0.973, diferencia pareada -0.010 ± 0.011; Brier 0.577 contra 0.572. Público en esos mismos 19: 0.931. Elo 0.951 y Poisson 0.923, los dos sobre 14 partidos. Acierto del favorito: modelo 11 de 19, mercado 12 de 19, público 12 de 21.

Calibración del modelo en los 20 partidos con estimación (esperado ± una desviación):
- Ganó el favorito en 12; se esperaban 10.4 ± 2.2.
- Salió el resultado menos probable en 5; se esperaban 4.4 ± 1.8.
- Hubo 3 empates; se esperaban 4.9 ± 1.9.
Nada se sale de lo esperable.

Qué falló:
- P3, P8, P11 y P13 iban en sencillo y con el mismo pick en los tres boletos; fallaron los cuatro. P14 llevaba doble L/V y salió empate.
- El agresivo quedó 1.5 aciertos por debajo de lo esperado: sus dos apuestas contra el público (P1 y P5) fallaron, además de las cinco casillas anteriores.
- En Revancha, México (64%) perdió en Kingston y tumbó a los tres boletos.

Qué dice el propio modelo sobre el perfil: la probabilidad de llegar a 10 aciertos era 37% para el conservador y 28% para el agresivo. El agresivo cambia unos 9 puntos de probabilidad de cobrar algo por una parte mayor de la bolsa de primer lugar. Es el costo conocido del perfil, no un error; queda anotado para decidir con ese número delante.

Pesos: sin cambio (13 partidos con mercado y Elo en el historial, mínimo 60).

### 2026-11-19, Media Semana 822, corte 07:55 CDMX (6 de 9 partidos)

Falla de proceso, antes que nada: la revisión final programada para el martes 17 a las 11:15 no se ejecutó. La sesión no procesó nada entre el martes 17 hacia las 08:00 y el jueves 19 a las 07:44, y el aviso llegó con casi dos días de retraso, así que el usuario no recibió la confirmación prometida antes del cierre de las 13:00. El boleto vigente era el de la relectura del lunes a las 20:00. La auditoría del martes (cierre del 2359) también quedó a medias y se terminó hoy.

Resultados (cada uno con dos fuentes): M1 México 1-0 Jamaica (L; sin tiempo extra, global 3-3 y pasó México por goles de visitante), M3 Dinamarca 2-3 Noruega (V), M4 Polonia 1-1 Suecia (E), M5 Rep. Irlanda 3-0 Kosovo (L), M6 Cruzeiro 2-1 Palmeiras (L), M7 Corinthians 4-0 Botafogo (L). Faltan M2, M8 y M9, que se juegan hoy.

Boleto (1 L, 2 V, 3 LV, 4 LV, 5 L, 6 LEV, 7 L, 8 LEV, 9 LV; $1,080): 5 de 6. Falló M4: llevaba doble L/V y salió el empate, al que el modelo daba 26.2%. Ya no puede hacer 9; el máximo es 8, y 8 solo cobra si nadie hace 9.

Qué falló y por qué:
- La casilla 4 se decidió por un margen que no distingue nada: el boleto elegido tenía 4.11% de probabilidad de 9 aciertos y el segundo, con triple en el 4 y doble L/V en el 6, tenía 4.07%. El segundo va 6 de 6.
- ¿Habría cambiado algo la revisión del martes? Por lo que se puede reconstruir, no en esa casilla. Pinnacle alargó el empate de Polonia-Suecia de 3.71 (lunes 20:10) a 3.95-3.99 (martes entre 11:09 y 12:15), es decir, lo hizo menos probable (de 25.8% a 24.1% sin margen), mientras el empate de Cruzeiro-Palmeiras se quedó en 3.41-3.42. Aplicando ese movimiento a los dos partidos, el mismo boleto sube a 4.19% y la alternativa se queda en 4.07%: el triple seguía en el 6. Fuentes: steamwatch.io (historial de Pinnacle de Polonia-Suecia) y titan007 (historial de Pinnacle de Cruzeiro-Palmeiras), leídas el 19-nov. No se reconstruyeron los otros siete partidos.
- No hubo error de datos ni de cálculo: salió un resultado de 26%.

Estimadores en los 6 partidos: modelo 0.858 y mercado 0.858 de log-loss (diferencia +0.000 ± 0.023); público 0.847. Acumulado de los dos concursos, 25 partidos con mercado y público: público 0.911, mercado 0.945, modelo 0.953. La ventaja del público sobre el mercado es 0.034 ± 0.044 y la del mercado sobre el modelo 0.007 ± 0.010: las dos dentro del ruido. La observación sobre el público se contará como segunda vez cuando cierre el 822.

Público del 822 (oficial, acumulado al 16-nov): el boleto iba contra el público en la casilla 2 (Lyonnes: 34.5% del público contra 48.7% del modelo).

Idea para decidir cuando dos boletos empatan, pendiente de que el usuario la apruebe: si la diferencia en probabilidad de acertar todo es menor que el margen de error y ya hay porcentajes del público, desempatar por el que cubre resultados menos jugados (comparte la bolsa con menos gente). En este concurso el empate del partido 4 lo llevaba 20.2% del público y el del partido 6, 25.5%: el desempate habría elegido el triple en el 4. No se podía aplicar: los porcentajes salieron 37 minutos antes del cierre. Antes de usarla hay que fijar qué diferencia cuenta como empate.

Concursos a la venta: Progol 2360 (hasta el viernes 20-nov a las 21:00, bolsa garantizada de 5 millones). La página oficial de Media Semana sigue mostrando el 822; el 823 no está publicado.

Pesos: sin cambio (17 partidos con mercado y Elo en el historial, mínimo 60).

### 2026-11-20, Media Semana 822, cierre de partidos (9 de 9)

Resultados nuevos (3, dos fuentes cada uno): M2 Arsenal F 0-2 Lyonnes F (V), M8 São Paulo 0-1 Fluminense (V), M9 Orlando 1-3 Cincinnati (V).

Boleto: 8 de 9. El único fallo fue M4 (doble L/V, salió empate). La apuesta contra el público en la casilla 2 (Lyonnes) acertó. Combinación oficial y premios: NO ENCONTRADOS todavía; el 20-nov a las 07:45 la página oficial seguía mostrando el 821. Falta saber si hubo ganadores de 9; si no los hubo, 8 aciertos cobra.

Estimadores en los 9 partidos: modelo 0.895 y mercado 0.892 de log-loss (diferencia -0.003 ± 0.015); público 0.933. En este concurso el público quedó peor que el mercado, al revés que en el 2359, así que la observación sobre el público no se repite y se queda en 1. Acumulado de 28 partidos con mercado: modelo 0.954, mercado 0.947.

Pesos: sin cambio (17 partidos con mercado y Elo, mínimo 60).

### 2026-11-21, cierre oficial de Media Semana 822 y primer partido del 2360

Media Semana 822: la combinación oficial (L V V E L L L V V, mascarilla del 20-nov) coincide con las 9 letras registradas. Hubo 36 quinielas con 9 aciertos, $63,577.70 cada una (dato de Reporte Índigo; el bloque de premios de la mascarilla no salió en la lectura). El boleto hizo 8 y no cobró: Media Semana solo paga el mayor número de aciertos.

Progol 2360 (boleto ligero de $1,080, solo mercado): P1 Juárez 3-3 Atlas (E). Llevaba V sencillo con 49.8%; el empate tenía 25.6%. Ya no puede hacer 14. Faltan 13 partidos.

Pesos: sin cambio.

### 2026-11-22, Progol 2360 con 12 de 14 partidos

Marcadores del viernes y sábado leídos de quinielaganadora.com (una sola fuente, marcador de partido completo; se cotejan con la combinación oficial al cierre). P14 fue final de copa: si hubo tiempo extra, el 0-2 puede no ser el de 90 minutos. Faltan P6 y P12, que se juegan hoy.

El boleto de $1,080 lleva 6 de 12. Fallos: P1, P7 y P13 (puse V, salió E), P5 (puse V, salió L), P10 y P11 (puse L, salió V). Los tres dobles (P2, P3, P4) y el triple de P8 entraron; los seis fallos fueron sencillos. Tope alcanzable: 8, así que ya no llega a 10 y no cobra. El boleto hipotético de $4,860 iría en 7 de 12.

El favorito del mercado ganó 3 de 11 y el log-loss del mercado fue 1.119, peor que tirar al azar (1.099). Es una jornada de 12 partidos y no alcanza para concluir nada: el acumulado del mercado sigue en 0.998 sobre 40 partidos. Este boleto fue solo mercado (modo ligero), así que modelo y mercado son el mismo número y la jornada no aporta a la comparación entre ellos.

Pesos: sin cambio (17 partidos con mercado y Elo, mínimo 60). Sin regla nueva.

### 2026-11-22, diagnóstico del 2360 (lo pidió el usuario)

Tres comprobaciones, ninguna encontró un error que corregir:

1. Entradas. Los momios que usé (betexplorer, 20-nov 13:55) contra el cierre de la misma página (leído hoy) en los cinco partidos de Liga MX ya jugados: Juárez–Atlas 3.67/3.55/1.89 contra 3.64/3.66/1.93; Pachuca–Toluca 2.63/3.84/2.22 contra 2.61/3.88/2.32; Santos–León 2.31/3.59/2.64 contra 2.22/3.55/2.97; Pumas–Monterrey 2.50/3.46/2.50 contra 2.62/3.39/2.56; Tigres–América 3.29/3.51/2.00 contra 3.28/3.65/2.04. Mismo local, mismo favorito, ningún pick cambia. Los otros siete jugados no se cotejaron contra el cierre (habría costado cinco lecturas más). Palmeiras–Flamengo: dos páginas confirman a Flamengo como favorito; la magnitud (54% en mi lectura de 3 casas) queda sin verificar.
2. Armado. Busqué el boleto que maximiza llegar a 10, a 11 y a 12 aciertos en vez de a 14. En el 2360 y en el 2359 sale exactamente el mismo boleto que el entregado. No hay otro objetivo que hubiera dado otra combinación.
3. Azar. Con mis propias probabilidades el boleto esperaba 6.9 aciertos en estos 12 partidos; hizo 6. Quedar en 6 o menos tenía 39% de probabilidad. Log-loss observado 1.119 contra 1.067 esperado, z = 0.71.

Lo que sí explica el resultado es la jornada: el favorito promedió 43.4% (47.8% en el 2359) y con $1,080 la probabilidad de cobrar algo era 24.8% desde antes de jugar. Referencia de premios (2359, oficial): 10 aciertos pagaron $123.41 y 11 pagaron $613.22 por quiniela sencilla.

Rendimiento por peso en el 2360: P(14) por cada $1,000 gastados fue 0.053% con una sencilla de $15, 0.039% con $480, 0.033% con $1,080 y 0.024% con $4,860. Cada doble o triple adicional compra menos probabilidad que el anterior.

Sin cambio de pesos ni de código. Sin regla nueva.

### 2026-11-23, Progol 2360 con los 14 partidos

Entraron los dos que faltaban: P6 Guadalajara 1-0 Cruz Azul (L, lo llevaba sencillo) y P12 Lorient 1-1 Rennes (E, lo llevaba triple). El boleto de $1,080 terminó en 8 de 14 y no cobra (el premio empieza en 10). Los seis fallos fueron sencillos: tres empates (P1, P7, P13) y tres favoritos que perdieron (P5, P10, P11).

Mercado en los 14 partidos: log-loss 1.113, favorito 4 de 13. Acumulado del mercado: 1.002 en 42 partidos. El boleto fue solo mercado, así que no hay comparación modelo contra mercado en este concurso.

Pendiente: la mascarilla oficial del 23-nov no estaba publicada a las 07:45 (404). Falta cotejar combinación y premios, y confirmar P14 a 90 minutos.

Pesos: sin cambio (17 partidos con mercado y Elo, mínimo 60). Sin regla nueva.

### 2026-11-23, boleto de Media Semana 823 (versión ligera)

Lo pidió el usuario con captura de la boleta el 22-nov. Los partidos 1 a 4 venían sin equipos; se llenaron con la tabla final del Apertura 2026 (El Financiero, ESPN y Mediotiempo coinciden): Pachuca–Guadalajara, León–Cruz Azul, Monterrey–América, Toluca–Atlas. No se leyó Lotería Nacional: el número 823 y las fechas vienen de quinielaganadora.com y la hora de cierre quedó sin verificar.

Momios: promedio de betexplorer con 4 casas por partido, una lectura el 23-nov a las 12:05. Solo mercado.

Boleto de $1,080 (2 triples, 3 dobles): 1:LEV 2:LEV 3:LV 4:L 5:L 6:LV 7:V 8:V 9:LV. P(9) = 5.47%, P(8) = 20.6%. Comprobado por fuerza bruta sobre todas las combinaciones válidas.

### 2026-11-23 (22:08), relectura de Media Semana 823

El usuario mandó otra captura de la app con los equipos de los partidos 1 a 4 ya escritos; coinciden con lo deducido de la tabla, mismo local y visitante. Se releyeron los momios (betexplorer, 3 casas en Liga MX y 4 en Champions) y se usó esa lectura en los nueve partidos. El mayor cambio fue Monterrey–América: Monterrey pasó de 38.7% a 41.0% y América de 36.0% a 32.5%.

Boleto con la lectura nueva ($1,080): 1:LEV 2:V 3:LEV 4:L 5:L 6:LV 7:LV 8:V 9:LV, P(9) = 5.22%. El boleto del mediodía, evaluado con los momios nuevos, da 5.12%. Los cuatro mejores boletos quedan entre 5.15% y 5.22%: la diferencia es menor que el error de los momios, así que los dos boletos son equivalentes.
