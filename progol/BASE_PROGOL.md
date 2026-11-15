# Base Progol

Bitácora de lo que el modelo propuso contra lo que pasó. Se actualiza con cada auditoría diaria.

## Cómo se audita

1. Buscar en la web los marcadores de los partidos ya jugados y guardarlos con fuente en `resultados_<concurso>.json`. Cuenta el marcador a 90 minutos más compensación.
2. Correr `python3 auditoria.py <concurso>`. Calcula Brier y log-loss del modelo final, del mercado, del Elo, del Poisson y del público, cuenta aciertos por boleto y reescribe `historial.csv`.
3. Anotar aquí lo observado.

Nota práctica: las páginas de resultados de temporada completa de betexplorer son enormes. Para marcadores conviene la nota de resumen de la jornada (UEFA, medios) o una búsqueda por partido.

## Cuándo se cambia un valor del modelo

- Los pesos de la mezcla (hoy 75% mercado y 25% Elo en selecciones; 80% mercado y 20% Poisson en clubes con xG) solo se mueven cuando el historial tiene al menos 60 partidos con ambos estimadores y la mejora en log-loss supera dos errores estándar. `auditoria.py` hace esa prueba sola.
- Una regla nueva entra a "Reglas vigentes" solo si el mismo patrón aparece en al menos tres concursos distintos. Antes de eso vive en "Observaciones".
- Un solo resultado no cambia nada.

## Reglas vigentes

Ninguna estadística todavía.

Decisión de diseño aprobada por el usuario el 2026-11-15, a partir de Media Semana 822: si se juegan varios boletos en un concurso, deben diferir en los sencillos más inciertos. Se arma con `boletos.mejor_complemento`, que busca combinaciones que los boletos anteriores no cubren y exige al menos 2 partidos con picks sin traslape. No es una regla sobre probabilidades; es sobre cómo repartir el riesgo entre boletos.

## Observaciones (candidatas, sin confirmar)

| Fecha | Concurso | Observación | Veces vista |
|---|---|---|---|
| 2026-11-14 | 2359 | Amistoso de selecciones en sede neutral (Japón 3-2 Brasil): cayó el favorito del mercado, del Elo y del público. Brasil llegó sin jugadores de Flamengo ni Palmeiras y con cinco debutantes. Pregunta abierta: ¿en amistosos el mercado sobrevalora al favorito con plantel recortado? | 1 |
| 2026-11-15 | 2359 | Los tres boletos de Progol compartían el mismo pick sencillo en 8 de 14 partidos (P3, P4, P7, P8, P9, P10, P11, P13). Cuando fallaron P3, P11 y P13 cayeron los tres a la vez. No es un patrón estadístico sino de diseño: los boletos no estaban diversificados entre sí. Aprobado por el usuario el 15-nov; ver Reglas vigentes. | 1 |
| 2026-11-15 | 2359 | Los picks contra el público del boleto agresivo (P1 local o empate, P5 empate) fallaron los dos: ganaron los que el público prefería. Dos casos no dicen nada sobre la estrategia; se sigue midiendo. | 1 |

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
