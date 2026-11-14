# Base Progol

Bitácora de lo que el modelo propuso contra lo que pasó. Se actualiza con cada auditoría diaria.

## Cómo se audita

1. Buscar en la web los marcadores de los partidos ya jugados y guardarlos con fuente en `resultados_<concurso>.json`. Cuenta el marcador a 90 minutos más compensación.
2. Correr `python3 auditoria.py <concurso>`. Calcula Brier y log-loss del modelo final, del mercado, del Elo, del Poisson y del público, cuenta aciertos por boleto y reescribe `historial.csv`.
3. Anotar aquí lo observado.

## Cuándo se cambia un valor del modelo

- Los pesos de la mezcla (hoy 75% mercado y 25% Elo en selecciones; 80% mercado y 20% Poisson en clubes con xG) solo se mueven cuando el historial tiene al menos 60 partidos con ambos estimadores y la mejora en log-loss supera dos errores estándar. `auditoria.py` hace esa prueba sola.
- Una regla nueva entra a "Reglas vigentes" solo si el mismo patrón aparece en al menos tres concursos distintos. Antes de eso vive en "Observaciones".
- Un solo resultado no cambia nada.

## Reglas vigentes

Ninguna todavía.

## Observaciones (candidatas, sin confirmar)

| Fecha | Concurso | Observación | Veces vista |
|---|---|---|---|
| 2026-11-14 | 2359 | Amistoso de selecciones en sede neutral (Japón 3-2 Brasil): cayó el favorito del mercado, del Elo y del público. Brasil llegó sin jugadores de Flamengo ni Palmeiras y con cinco debutantes. Pregunta abierta: ¿en amistosos el mercado sobrevalora al favorito con plantel recortado? | 1 |

## Bitácora

### 2026-11-14, concurso 2359, corte 11:15 CDMX (1 de 21 partidos)

- P3 Japón 3-2 Brasil, salió L. El modelo le daba 23.6% a Japón; el favorito era Brasil con 52%.
- Los tres boletos de Progol llevaban V fijo en este partido, así que el máximo posible ya es 13 aciertos.
- Log-loss en ese partido: modelo 1.442, mercado 1.426, Elo 1.493, público 1.598. Con un partido no se concluye nada.
- Pesos: sin cambio (1 partido en el historial, mínimo 60).
