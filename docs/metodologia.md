# Decisiones metodológicas

Este documento explica los criterios de inclusión y exclusión, la delimitación territorial y temporal, el tratamiento de monedas y precios, y las decisiones de clasificación territorial y georreferenciación.

## 1. Criterios de inclusión y exclusión

### Inclusión (resultado SÍ)
Una publicación se confirma dentro de Diez de Octubre cuando:

- El **título** nombra Diez de Octubre o un reparto interno del municipio (Santos Suárez, Lawton, La Víbora, Luyanó, El Sevillano, El Mónaco, Santa Catalina, etc.), **o**
- Cuando el título no aporta señal, la ficha de Revolico declara Diez de Octubre, **o**
- Cuando ni título ni ficha aportan señal, el texto declarado (enlace, grupo, ubicación o zona) menciona un reparto interno.

### Exclusión (resultado NO)
Una publicación se descarta cuando:

- El **título** nombra un lugar externo a Diez de Octubre (otro municipio, provincia o localidad), aunque la ficha declare Diez de Octubre.
- Ejemplos descartados por título: Artemisa, Boca Ciega, Casino Deportivo, Consolación del Sur, Mantilla, Náutico, Pimienta, San Agustín, Víbora Park.

### Indeterminadas
Cuando ninguna evidencia alcanza para decidir, la publicación queda como `INDETERMINADO` y se excluye del universo final, pero se conserva en los descartes con su motivo.

## 2. Delimitación territorial y temporal

- **Territorial:** Municipio Diez de Octubre, La Habana, Cuba. Polígono DPA 23.09 (`datos/geo/lha.geojson`, 11 vértices). No se incorporan otros municipios ni provincias.
- **Temporal:** Corte único de Revolico el 2026-10-31. Captura de Facebook el 2026-11-04. No hay serie temporal.

## 3. Tratamiento de monedas y precios

- **USD:** moneda principal. 106 anuncios declaran USD (86.9% del universo).
- **CUP:** 1 anuncio declara CUP (un alquiler). No se convierte a USD por falta de un tipo de cambio oficial o de mercado claramente definido para el corte. Se reporta como hallazgo, no como precio comparable.
- **Sin precio:** 15 anuncios (12.3%). Se conservan y se reportan como opacidad; no se imputan.
- **Precios de oferta:** los valores son precios publicados, no precios de transacción.

## 4. Clasificación territorial y georreferenciación

- **Regla de título primero:** el campo `municipio` del scraper no es fiable (asigna "Diez de Octubre" a anuncios de otros municipios). Por eso el título tiene prioridad sobre la ficha.
- **Geocodificación:** los topónimos se geocodificaron con Nominatim y se comprobó punto-en-polígono contra `datos/geo/lha.geojson`.
- **Casos ambiguos:** «Ampliación del Sevillano» y «Reparto Flores» se conservan con confianza media y la ambigüedad se documenta en el motivo.
- **Límite del polígono:** es una simplificación de 11 vértices; no resuelve casos catastrales a pocos metros del borde.

## 5. Limitaciones y sesgos

- **Muestra no probabilística:** 122 publicaciones no son necesariamente representativas del universo de viviendas del municipio.
- **Precios de oferta:** no son precios de transacción.
- **Alquiler:** solo 3 publicaciones, 1 con precio en CUP y ninguna en USD. No se puede estimar un precio de alquiler.
- **Campos ausentes:** no hay datos homogéneos de metros cuadrados, estado legal, número de baños, año de construcción, vendedor o agencia.
- **Sesgo de publicación:** las viviendas que no se publican, o que se publican en canales cerrados, no aparecen en la base.
- **Duplicado entre fuentes:** 1 par (`facebook-35` / `revolico-58326838`, misma propiedad y precio). Se conserva para no alterar el universo; n efectivo sería 121.
- **No se imputan valores ausentes:** las ausencias se reportan como indicador de opacidad.
