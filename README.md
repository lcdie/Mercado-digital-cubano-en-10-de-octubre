# Mercado Inmobiliario Digital en Diez de Octubre, La Habana

**Trabajo de la asignatura Ciencia de Datos — Universidad de La Habana**  
**Facultad de Matemática y Computación (MATCOM)**  
**Profesor:** Yudivian Almeida Cruz

## Historia del proyecto

Este proyecto estudia el mercado inmobiliario digital de Diez de Octubre como un **problema social**: la opacidad de la información, la dolarización de los precios, la desigualdad entre barrios y las prácticas informales condicionan quién puede comprar o alquilar y en qué condiciones.

La pregunta inicial —**¿cuánto cuesta realmente vivir en Diez de Octubre?**— se responde con anuncios reales de Revolico, pero el análisis va más allá del precio promedio: mide cuánta información falta, en qué moneda se publica y qué barrios concentran la oferta. El objetivo es ofrecer una lectura clara, sin tecnicismos, para cualquier persona interesada en comprar o alquilar vivienda en el municipio.

## Objetivos

- Analizar la oferta inmobiliaria publicada en plataformas digitales cubanas enfocada al municipio Diez de Octubre.
- Caracterizar precios, tipos de inmueble, zonas, moneda declarada y características físicas.
- Responder 30 preguntas de investigación coherentes entre sí, comunicables a personas sin conocimientos técnicos ni del tema inmobiliario.
- Proporcionar una base replicable y abierta para futuros análisis del mercado digital cubano.

## Fuentes de datos

| Fuente | Uso en el proyecto |
|--------|--------------------|
| **Revolico** (scraping propio) | Fuente principal: **83 publicaciones confirmadas** dentro de Diez de Octubre, con precios, tipos, zonas y moneda cuando están disponibles. |
| **Anuario Estadístico de Cuba (ONEI)** | Contexto oficial del municipio (población, vivienda y tenencia); no se usa para calcular precios ni proporciones de la muestra digital. |
| **Facebook** (grupos de compraventa) | **39 publicaciones confirmadas** dentro del municipio, integradas en la base final. Aportan precio y descripción, pero muchas no tienen título ni texto crudo homogéneo. |
| **Base unificada verificada** | **122 publicaciones confirmadas** (83 Revolico + 39 Facebook) tras comprobar cada una contra el polígono municipal con el título como evidencia principal. Es el universo del informe A-F. |
| **GeoJSON provincial de La Habana** | `datos/geo/lha.geojson`: 15 municipios. Se usa para verificar la pertenencia real de cada publicación al municipio Diez de Octubre mediante el polígono municipal (`DPA 23.09`). |

> **El Caimán fue descartado:** sus datos no correspondían al municipio Diez de Octubre. No se usa en ninguna cifra del informe.

> Nota: este proyecto no aborda aspectos políticos ni hace comparativas que no sean directamente hacia el mercado inmobiliario.

## Universo y metodología

- **Universo final del informe A-F:** **122 publicaciones confirmadas** dentro de Diez de Octubre: 83 de Revolico + 39 de Facebook.
- **Base de análisis:** `datos/limpios/unificado_confirmados_diez_octubre.json`, obtenida de las 176 publicaciones unificadas (134 de Revolico + 42 de Facebook) tras la verificación municipal con regla de título.
- **Precios:** 107 publicaciones declaran precio: 106 en USD y 1 en CUP (un alquiler de 50,000 CUP); 15 no declaran precio. Los análisis de precio usan las 106 publicaciones en USD.
- **Compra:** 43 ventas explícitas con precio en USD. Media $26,023.26; mediana $20,000; P10–P90 $6,200–$60,000.
- **Alquiler:** 3 publicaciones; 1 declara precio en CUP, 2 no declaran precio y ninguna declara USD. No se puede estimar un precio de alquiler.
- **Valores extremos:** se reporta la mediana y el tramo P10–P90 junto a la media. En las 106 publicaciones con precio USD, el 80% central está entre $9,000 y $75,000.
- **Tamaño de muestra:** cada respuesta indica su `n`. Los subgrupos con `n < 10` se presentan como evidencia descriptiva, no como conclusión firme.
- **Clasificación:** tipo y operación se toman de los campos normalizados. La zona se completa con el texto declarado solo cuando el anuncio menciona el barrio o reparto; no se infiere una ubicación que no aparezca en la publicación.
- **Recencia:** Revolico no expone la fecha de publicación; `fecha_verificacion` registra el momento de captura (corte 2026-10-31). Facebook tiene fechas relativas o ausentes.
- **Fuentes integradas:** Revolico aporta título, enlace, ubicación de ficha y precio; Facebook aporta precio y descripción, pero muchas publicaciones no tienen título ni texto crudo homogéneo. Por eso la operación queda «sin clasificar» con más frecuencia en Facebook y la medición de lenguaje informal solo es posible en Revolico.
- **Campo `municipio`:** no es fiable. Todos los anuncios aparecen como «Diez de Octubre», incluso los de otros municipios. Por eso la verificación prioriza el título y usa el polígono municipal como comprobación independiente.
- **Base histórica de 134:** se conserva para reproducir la versión revisada del cuestionario original y la trazabilidad. No es comparable con el informe A-F recalculado sobre 122.

## Verificación real de pertenencia municipal

La etiqueta «Diez de Octubre» de la base de 134 no equivale a pertenencia verificada. Para comprobarlo se usó el **título como evidencia principal** y, solo cuando no aportaba señal, la ficha y el resto del texto:

1. el título de la publicación, que puede nombrar Diez de Octubre, un reparto interno (Santos Suárez, Lawton, La Víbora, Luyanó, El Sevillano, etc.) o un lugar externo;
2. la ubicación declarada por la propia ficha de Revolico (`data-cy="adLocation"`), usada como respaldo;
3. los topónimos de la zona, el grupo o la ubicación de la publicación;
4. la geocodificación de esos topónimos con Nominatim y su comprobación punto-en-polígono contra `datos/geo/lha.geojson`.

**Regla de título:** si el título nombra un lugar externo, la publicación se descarta aunque la ficha diga Diez de Octubre. Si nombra el municipio o un reparto interno, se confirma aunque la ficha declare Cerro o Arroyo Naranjo. Los casos ambiguos se conservan con confianza media y se documentan.

| Resultado | Revolico (n=134) | Facebook (n=42) | Unificado (n=176) |
|---|---:|---:|---:|
| SÍ, dentro de Diez de Octubre | 83 | 39 | 122 |
| NO, otro municipio | 46 | 0 | 46 |
| CONTRADICTORIO | 0 | 0 | 0 |
| INDETERMINADO | 5 | 3 | 8 |

**Hallazgo:** de los 134 anuncios llamados «estrictos», **83 están confirmados** en Diez de Octubre: 73 tienen ficha que declara el municipio y 10 se confirman por mención interna en el título (8 con ficha de otro municipio y 2 sin ficha recuperable). **46 fichas declaran otro municipio** y 5 no son verificables. La base depurada queda en **122 registros** (83 Revolico + 39 Facebook) en `datos/limpios/unificado_confirmados_diez_octubre.json`.

Los 8 casos que antes se marcaban como contradictorios tenían un título con un reparto interno y quedaron confirmados por la regla de título: El Mónaco, Ampliación de Sevillano, Reparto Flores, Santos Suárez, Ampliación del Sevillano, 10 de Octubre, Calzada 10 de Octubre y Luyanó.

**Nada se elimina:** los 55 registros no incluidos (46 de otro municipio, 8 indeterminados y la publicación de Facebook rechazada previamente) se conservan íntegros en `datos/limpios/descartados_diez_octubre.json` y `datos/limpios/descartados_diez_octubre.csv`, con su motivo de descarte, su registro original y el registro unificado exacto.

El informe A-F ya fue recalculado con esos **122** registros. La base canónica de 134 y la versión revisada del cuestionario original se conservan como referencia histórica y no son comparables con el informe actual.

El detalle publicación por publicación está en `analisis/verificacion_municipal_geojson_20261104.md`.

## Estructura del repositorio

```text
proyecto-mercado-10-octubre/
├── README.md
├── analisis/
│   ├── informe_final.md                 # Informe A-F sobre las 122 publicaciones confirmadas
│   ├── informe_final.pdf                # Entrega académica en PDF
│   ├── informe_30_preguntas_originales_reemplazadas.md   # Versión histórica paralela sobre la base de 134
│   ├── informe_30_preguntas_originales_reemplazadas.pdf  # PDF de la versión histórica paralela
│   ├── reporte_limpieza_facebook_20261104.md              # Limpieza y unificación de Facebook
│   ├── verificacion_municipal_geojson_20261104.md         # Verificación publicación por publicación contra el polígono
│   ├── telefonos_y_enlaces.txt          # Teléfonos y enlaces de anuncios
│   └── limpieza/                        # Material histórico de limpieza manual
├── datos/
│   ├── brutos/
│   │   ├── facebook_crudos_20261104.json       # Captura original de Facebook (43 publicaciones)
│   │   ├── revolico_crudos_limpio_final.json    # Base histórica de 134 anuncios de Revolico
│   │   └── revolico_ubicaciones_pagina.json     # Ubicación declarada por cada ficha de Revolico
│   ├── geo/
│   │   ├── lha.geojson                          # 15 municipios de La Habana
│   │   └── geocoding_lha.json                   # Caché de geocodificación de topónimos
│   └── limpios/
│       ├── anuncios_eliminados_por_filtro_final.json  # 136 rechazados y su motivo
│       ├── facebook_publicaciones_limpias.json  # Facebook tras filtro y normalización (42)
│       ├── facebook_eliminados_por_filtro.json  # Publicación de Facebook rechazada y motivo
│       ├── datos_unificados_facebook_revolico.json   # Base unificada limpia (176: 134 Revolico + 42 Facebook)
│       ├── reporte_analisis_precios_rango_p10_p90.txt
│       ├── verificacion_municipal_revolico.json      # Verificación municipal de los 134 anuncios
│       ├── verificacion_municipal_facebook.json      # Verificación municipal de Facebook (42 + 1 rechazada)
│       ├── verificacion_municipal_unificado.json     # Verificación municipal de los 176 registros
│       ├── verificacion_municipal.csv                # Resumen tabular de la verificación
│       ├── descartados_diez_octubre.json             # Registros no incluidos, íntegros y con motivo
│       ├── descartados_diez_octubre.csv              # Versión tabular de los descartados
│       └── unificado_confirmados_diez_octubre.json   # Base final: 122 registros confirmados (universo del informe A-F)
├── scripts/
│   ├── analisis_final_30_preguntas.py   # Generador canónico del informe A-F
│   ├── analisis_30_preguntas_originales_reemplazadas.py  # Generador de la versión revisada
│   ├── analisis_precios_rango_p10_p90.py
│   ├── generar_pdf_informe.py           # Conversión Markdown -> PDF (acepta --input/--output)
│   ├── limpieza_final_municipio.py
│   ├── limpiar_facebook.py              # Limpieza y normalización de Facebook
│   ├── mezclar_facebook_revolico.py     # Unificación de las bases limpias
│   ├── geo_municipio.py                 # Polígono municipal, point-in-polygon y geocodificación
│   ├── verificar_ubicaciones_revolico.py        # Extrae la ubicación de cada ficha de Revolico
│   ├── verificar_municipio_publicaciones.py     # Verificación municipal y reporte
│   ├── verificar_y_actualizar_anuncios.py
│   ├── limpiar_datos_brutos.py
│   ├── generar_lista_limpia.py
│   ├── agregar_permuta.py
│   └── extraer_fechas_publicacion.py
├── src/
│   └── scrape_revolico.py               # Descarga de anuncios de Revolico
├── fuentes/
│   └── anuario_estadistico_notas.md     # Notas de fuentes oficiales
├── requirements.txt                     # Dependencias de análisis
├── requirements-docs.txt                # Dependencias para generar el PDF
└── LICENSE                              # Licencia MIT
```

> `datos/brutos/*.json` está en `.gitignore`; la base final de Revolico y la captura de Facebook se versionaron con `git add -f`. Si se regeneran, hay que repetir ese paso.

## Las 30 preguntas de investigación

Las preguntas se organizan en seis bloques sociales. Cada respuesta del informe final indica su `n`, su nivel de evidencia y, cuando corresponde, la ausencia de datos como hallazgo.

### Bloque A: Precios de referencia (5)

- **A1.** ¿Cuál es el precio promedio de compra en USD?
- **A2.** ¿Cuál es la mediana y el rango P10–P90 del precio de compra en USD?
- **A3.** ¿Cuál es el precio promedio o mediano del alquiler?
- **A4.** ¿Qué proporción de alquileres declara precio y en qué moneda?
- **A5.** ¿La compra declara precio más que el alquiler?

### Bloque B: Desigualdades territoriales (5)

- **B1.** ¿Qué zonas concentran la mayor oferta?
- **B2.** ¿Qué zona tiene el precio promedio más alto?
- **B3.** ¿Qué zona tiene la mediana más alta?
- **B4.** ¿La brecha La Víbora–Lawton se mantiene al usar medianas?
- **B5.** ¿La falta de zona afecta igual a compra y alquiler?

### Bloque C: Dolarización (5)

- **C1.** ¿Qué porcentaje de anuncios con moneda declarada está en USD?
- **C2.** ¿Qué porcentaje del total está en USD?
- **C3.** ¿La dolarización varía por tipo de inmueble?
- **C4.** ¿La dolarización varía por zona?
- **C5.** ¿Cuánto podría variar la dolarización si los anuncios sin precio fueran CUP o USD?

### Bloque D: Opacidad de la información (5)

- **D1.** ¿Qué porcentaje no declara precio?
- **D2.** ¿Qué porcentaje no especifica zona?
- **D3.** ¿Cuántos anuncios carecen de precio y zona a la vez?
- **D4.** ¿Qué porcentaje tiene información mínima completa (precio + zona)?
- **D5.** ¿La opacidad es mayor en alquiler que en venta?

### Bloque E: Prácticas informales (5)

- **E1.** ¿Qué porcentaje usa lenguaje informal («oportunidad», «ganga», «permuta», «intercambio» o «cambio»)?
- **E2.** ¿Qué palabras informales dominan?
- **E3.** ¿Los anuncios informales declaran precio más que los neutros?
- **E4.** ¿La informalidad se concentra en alguna operación?
- **E5.** ¿Los anuncios sin clasificar son más opacos que los clasificados?

### Bloque F: Tipos de inmueble y accesibilidad (5)

- **F1.** ¿Qué tipo de inmueble se publica más?
- **F2.** ¿Qué tipo tiene el precio medio más bajo?
- **F3.** ¿Qué tipo tiene la mediana más baja?
- **F4.** ¿La diferencia se mantiene en el rango P10–P90?
- **F5.** ¿Qué tipo concentra más opacidad de precio y zona?

## Versión revisada del cuestionario original

Además del informe A-F, el repositorio conserva una segunda versión que parte del **cuestionario original de 30 preguntas** y mantiene su numeración. Se conservan **20 preguntas** y se reemplazan **10** que no tenían respaldo suficiente en la base histórica de 134 anuncios:

> **Importante:** esta versión paralela sigue calculada sobre los **134 anuncios de Revolico**, no sobre los 122 confirmados. Se conserva por trazabilidad metodológica y no debe compararse con el informe A-F recalculado.

| # | Pregunta original | Motivo | Reemplazo |
|---|---|---|---|
| 10 | ¿Qué tipo de inmueble concentra el precio máximo declarado? | Depende de un solo anuncio (n = 1). | ¿Cuál es la mediana del precio en USD por tipo de inmueble? |
| 12 | ¿Qué tipo de inmueble domina en la zona con el precio promedio más alto? | La Víbora solo tiene 9 anuncios con precio (n = 9). | ¿La declaración de precio depende de que el anuncio identifique zona? |
| 13 | ¿Cuál es la cantidad más común de cuartos/habitaciones? | Solo 14 anuncios permiten extraer un número explícito de cuartos. | ¿Qué proporción de anuncios es totalmente opaca? |
| 14 | ¿Cómo varía el precio según el número de cuartos? | Solo 12 anuncios combinan cuartos y precio en USD. | ¿Qué proporción de anuncios ofrece información completa (precio y zona)? |
| 15 | ¿Qué porcentaje menciona garaje y cómo se relaciona con el precio? | Solo 7 anuncios mencionan garaje. | ¿La opacidad de precio y zona es mayor en alquiler o en venta? |
| 16 | ¿Cuántos anuncios especifican 'planta baja' y cuál es su precio promedio? | Solo 8 anuncios mencionan planta baja o bajos. | ¿Qué tipo de inmueble presenta mayor opacidad? |
| 20 | ¿Qué zona tiene el precio promedio más alto? | La Víbora tiene 9 anuncios y un valor extremo de $180,000. | ¿Qué porcentaje de anuncios queda dentro del tramo P10–P90? |
| 22 | ¿Hay diferencia de precios entre zonas? | Se apoya en grupos de 9 y 10 anuncios y en medias sensibles a extremos. | ¿Cuánto cambia el precio promedio al recortar 10% de cada cola? |
| 26 | ¿Los anuncios informales declaran precio más que los neutros? | Solo 15 anuncios usan lenguaje informal. | ¿Cómo se distribuye la informalidad según la operación? |
| 29 | ¿Cuántos anuncios parecen de particulares frente a agencias? | La base no tiene campo de vendedor ni de agencia. | ¿Qué proporción no declara operación y cómo se distribuye por tipo? |

El informe completo está en `analisis/informe_30_preguntas_originales_reemplazadas.md` y su PDF en `analisis/informe_30_preguntas_originales_reemplazadas.pdf`. Todas las respuestas usan la base histórica de 134 anuncios, indican `n` y nivel de evidencia, y tratan la ausencia de datos como hallazgo. Esta versión no se recalculó con los 122 porque su propósito es conservar el cuestionario original y su reemplazo, no sustituir al informe A-F.

## Trazabilidad del cambio de universo

La evolución de la base tiene tres hitos:

1. **Universo inicial de 171 anuncios:** incluía 37 que mencionaban otros municipios. Quedó supersedido.
2. **Base estricta de 134 anuncios de Revolico:** aplicó un filtro por título y enlace, pero seguía siendo una muestra *etiquetada* como Diez de Octubre, no verificada.
3. **Universo verificado de 122 publicaciones:** la comprobación con el título como evidencia principal y el polígono municipal confirma 83 anuncios de Revolico y 39 de Facebook dentro del municipio. El informe A-F se recalcula sobre esta base.

De los 176 registros unificados quedan fuera 46 de otro municipio y 8 indeterminados. Los 8 casos antes contradictorios se confirmaron por la regla de título. Esa exclusión reduce la muestra, pero evita atribuir a Diez de Octubre precios y zonas de otros municipios. El detalle publicación por publicación está en `analisis/verificacion_municipal_geojson_20261104.md`; los descartados se conservan en `datos/limpios/descartados_diez_octubre.json`.

La versión revisada del cuestionario original sigue sobre los 134 y se mantiene como referencia histórica; no es comparable con el A-F actual. El detalle de las preguntas reemplazadas está en la sección anterior.

## Cómo regenerar el informe

Desde la raíz del proyecto:

```bash
# 1. Bases limpias y unificación
python3 scripts/limpieza_final_municipio.py
python3 scripts/limpiar_facebook.py
python3 scripts/mezclar_facebook_revolico.py

# 2. Verificación municipal con el GeoJSON
python3 scripts/verificar_ubicaciones_revolico.py
python3 scripts/verificar_municipio_publicaciones.py

# 3. Informe A-F sobre las 122 publicaciones confirmadas
python3 scripts/analisis_final_30_preguntas.py

# 4. Material histórico y reportes auxiliares (siguen sobre 134)
python3 scripts/analisis_30_preguntas_originales_reemplazadas.py
python3 scripts/analisis_precios_rango_p10_p90.py
```

El orden importa: la verificación municipal debe ejecutarse **antes** del informe A-F, porque `analisis_final_30_preguntas.py` lee `verificacion_municipal_unificado.json` y se queda solo con `resultado == "SÍ"`.

- `limpieza_final_municipio.py` lee `datos/brutos/revolico_crudos_limpio.json` (270 anuncios), aplica el filtro estricto y escribe la base histórica de 134 y los 136 rechazados.
- `limpiar_facebook.py` lee `facebook_crudos_20261104.json`, aplica el mismo filtro municipal y de precio, y escribe 42 publicaciones limpias y 1 rechazo.
- `mezclar_facebook_revolico.py` une ambas bases en `datos_unificados_facebook_revolico.json` (176 registros).
- `verificar_ubicaciones_revolico.py` descarga y guarda la ubicación declarada por cada ficha de Revolico.
- `verificar_municipio_publicaciones.py` aplica la regla de título (el título decide; la ficha y el resto del texto son respaldo), comprueba los topónimos contra el polígono de `datos/geo/lha.geojson`, geocodifica con Nominatim y escribe la verificación municipal, la base de 122 confirmados y los 55 descartados íntegros. Usa la caché `datos/geo/geocoding_lha.json`.
- `analisis_final_30_preguntas.py` lee la base unificada, filtra los confirmados y escribe `analisis/informe_final.md` con las 30 preguntas A1–F5.
- `analisis_30_preguntas_originales_reemplazadas.py` y `analisis_precios_rango_p10_p90.py` se mantienen sobre la base histórica de 134 y no alimentan el informe A-F.

La fecha de generación cambia en cada ejecución, aunque las cifras se mantengan.

## Cómo generar la entrega en PDF

```bash
python3 -m venv .venv-docs
source .venv-docs/bin/activate
pip install -r requirements-docs.txt
python3 scripts/generar_pdf_informe.py
python3 scripts/generar_pdf_informe.py \
    --input analisis/informe_30_preguntas_originales_reemplazadas.md \
    --output analisis/informe_30_preguntas_originales_reemplazadas.pdf \
    --subtitle "Versión revisada — 20 preguntas originales y 10 reemplazos"
```

El PDF se guarda en `analisis/informe_final.pdf` (o en la ruta indicada con `--output`) e incluye portada, tablas, numeración de páginas y los datos académicos (MATCOM y profesor).

## Pipeline de datos (resumen)

1. `src/scrape_revolico.py`: descarga anuncios de Revolico.
2. `scripts/verificar_y_actualizar_anuncios.py`: verifica anuncios activos y agrega nuevos.
3. `scripts/limpiar_datos_brutos.py`: elimina anomalías graves.
4. `scripts/limpieza_final_municipio.py`: aplica el filtro estricto de Diez de Octubre y precio mínimo; produce la base histórica de 134 anuncios.
5. `scripts/limpiar_facebook.py`: aplica el mismo filtro municipal y de precio a las 43 publicaciones de Facebook, normaliza sus campos y produce 42 registros limpios y 1 rechazo documentado.
6. `scripts/mezclar_facebook_revolico.py`: unifica las bases limpias de Revolico y Facebook; produce 176 registros con fuente, tipo, zona y operación normalizados.
7. `scripts/verificar_ubicaciones_revolico.py`: extrae la ubicación declarada por cada ficha de Revolico.
8. `scripts/verificar_municipio_publicaciones.py`: verifica publicación por publicación con el título como evidencia principal y el polígono de Diez de Octubre como comprobación; produce el reporte, la base de 122 confirmados y los 55 descartados conservados.
9. `scripts/analisis_final_30_preguntas.py`: filtra los 122 confirmados y genera el informe A-F con las 30 preguntas.
10. `scripts/analisis_30_preguntas_originales_reemplazadas.py`: genera la versión histórica del cuestionario original (20 preguntas conservadas + 10 reemplazos) sobre 134.
11. `scripts/analisis_precios_rango_p10_p90.py`: genera el reporte de P10–P90 sobre 134.

> El informe A-F usa la base verificada de 122 publicaciones. La base unificada de 176 es el insumo de la verificación, y la base de 134 se conserva solo como referencia histórica. Los 55 registros no incluidos no se borran: quedan en `datos/limpios/descartados_diez_octubre.json` con su motivo.

## Herramientas utilizadas

- **Python** con `requests` y `BeautifulSoup` para el scraping.
- **Pandas** y **Matplotlib/Seaborn** para análisis y visualizaciones.
- **Markdown + WeasyPrint** para la entrega en PDF.
- No se usan Excel, SQL ni Power BI.
- Las dependencias de análisis están en `requirements.txt`; las de documentación, en `requirements-docs.txt`.

## Limitaciones

- Los datos del informe provienen de Revolico y Facebook (122 publicaciones confirmadas). No representan la totalidad del mercado físico: las viviendas que no se publican, o que se publican en canales cerrados, no aparecen en la base.
- **La base de 134 era una muestra etiquetada, no verificada:** la comprobación con la regla de título y el GeoJSON confirma 83 anuncios de Revolico dentro de Diez de Octubre; 46 fichas declaran otro municipio y 5 no son verificables. El informe A-F ya usa la base depurada de 122.
- La verificación municipal depende de la ubicación que declara el anunciante y de topónimos geocodificados a un punto representativo, no de la dirección exacta de la propiedad. El polígono tiene 11 vértices y no resuelve casos catastrales a pocos metros del borde.
- Facebook se integró con 39 publicaciones confirmadas, pero su esquema es heterogéneo: muchas no tienen título ni texto crudo homogéneo, lo que eleva el «sin clasificar» y limita la medición de informalidad a Revolico.
- **15 de 122 publicaciones (12.3%)** no declaran precio y **31 (25.4%)** no especifican zona. No se imputan valores ni ubicaciones: la ausencia se reporta como hallazgo.
- **Solo 82 de 122 (67.2%)** permiten cruzar precio y zona; **6 (4.9%)** carecen de ambos datos.
- La clasificación de tipo y operación se basa en campos normalizados, y la zona se completa con el texto declarado. Puede contener errores en títulos ambiguos.
- Los subgrupos por zona (n = 5–25) y por tipo son pequeños; sus promedios y medianas se presentan como evidencia descriptiva.
- No hay base para estimar el precio de alquiler: solo 3 publicaciones de alquiler, 1 con precio en CUP y ninguna en USD.
- Revolico no expone fecha de publicación; `fecha_verificacion` registra el momento de captura. Facebook tiene fechas relativas o ausentes.
- El anuncio de $180,000 está clasificado como «Inmueble» porque su título no especifica «Casa»; no se reclasifica sin evidencia textual. Ese valor atípico infla la media de La Víbora, por lo que se recomienda usar la mediana.
- La base contiene un par duplicado entre fuentes (`facebook-35` y `revolico-58326838`, misma propiedad y precio). Se conserva para no alterar el universo de 122; el `n` efectivo sería 121 si se eliminara.

## Exposición

El proyecto incluye materiales para una exposición de aproximadamente 5–10 minutos, pensada para personas sin conocimientos técnicos ni del tema inmobiliario. Se recomienda presentar:

1. El problema social: opacidad, dolarización, desigualdad territorial e informalidad en el mercado inmobiliario digital.
2. La fuente y la corrección de la base: de 176 publicaciones unificadas a **122 confirmadas** dentro de Diez de Octubre (83 de Revolico + 39 de Facebook); quedan fuera 46 de otro municipio y 8 indeterminadas, y los 55 registros excluidos se conservan íntegros con su motivo.
3. Los hallazgos principales: precio mediano de compra, brecha territorial medida con medianas, dolarización y opacidad.
4. Qué significa esto para una persona común: no solo cuánto cuesta, sino qué información falta y quién puede acceder a ella.
5. Limitaciones y ausencia de datos como parte del resultado.
