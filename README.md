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
| **Revolico** (scraping propio) | Fuente principal y única usada en los cálculos: **134 anuncios estrictos** de Diez de Octubre, con precios, tipos, zonas y moneda cuando están disponibles. |
| **Anuario Estadístico de Cuba (ONEI)** | Contexto oficial del municipio (población, vivienda y tenencia); no se usa para calcular precios ni proporciones de la muestra digital. |
| **Facebook** (grupos de compraventa) | Fuente explorada: **43 publicaciones capturadas**, **42 conservadas** tras aplicar el mismo filtro municipal y de precio que a Revolico. Se integran en una base unificada separada (176 registros: 134 de Revolico + 42 de Facebook), no usada en el informe A-F. |

> **El Caimán fue descartado:** sus datos no correspondían al municipio Diez de Octubre. No se usa en ninguna cifra del informe.

> Nota: este proyecto no aborda aspectos políticos ni hace comparativas que no sean directamente hacia el mercado inmobiliario.

## Universo y metodología

- **Universo final:** **134 anuncios estrictos** de Revolico, todos del municipio Diez de Octubre.
- **Corrección de la base:** la fuente completa tiene 270 anuncios. El filtro estricto descarta 136: 133 por mencionar otro municipio o localidad y 3 por precio inferior a 1,000 USD. La versión anterior del informe usaba 171 anuncios; de ellos, 37 mencionaban otros municipios y fueron retirados.
- **Precios:** 116 anuncios declaran precio en USD, 1 en CUP y 17 no declaran precio. Los análisis de precio usan los 116 en USD.
- **Compra:** 46 ventas explícitas con precio USD. Media $22,597.83; mediana $16,000; P10–P90 $6,500–$43,500.
- **Alquiler:** 9 anuncios; 1 declara precio en CUP (50,000 CUP), 8 no declaran precio y ninguno declara USD. No se puede estimar un precio de alquiler.
- **Valores extremos:** se reporta la mediana y el tramo P10–P90 junto a la media. En el conjunto de los 116 anuncios con precio USD, el 80% central está entre $7,750 y $75,000.
- **Tamaño de muestra:** cada respuesta indica su `n`. Los subgrupos con `n < 10` se presentan como evidencia descriptiva, no como conclusión firme.
- **Clasificación:** tipo, zona y operación se infieren de palabras clave del título y del enlace. Puede contener errores.
- **Recencia:** Revolico no expone la fecha de publicación; el ID numérico del enlace se usa como proxy.
- **Facebook:** 43 publicaciones capturadas; 42 conservadas y 1 rechazada por mencionar Santa Amalia, fuera del filtro estricto. Se normalizaron tipo, zona, operación, distribución y contacto. La base unificada limpia queda en 176 registros (134 Revolico + 42 Facebook) y no se usa para las cifras del informe A-F, porque su esquema original no comparte el municipio normalizado de Revolico.
- **Campo `municipio`:** no es fiable. Todos los anuncios aparecen como «Diez de Octubre», incluso los de otros municipios. Por eso el filtro revisa título y enlace, y la exclusión municipal tiene prioridad sobre ese campo.

## Estructura del repositorio

```text
proyecto-mercado-10-octubre/
├── README.md
├── analisis/
│   ├── informe_final.md                 # Informe final A-F con las 30 preguntas
│   ├── informe_final.pdf                # Entrega académica en PDF
│   ├── informe_30_preguntas_originales_reemplazadas.md   # Versión revisada: 20 preguntas originales + 10 reemplazos
│   ├── informe_30_preguntas_originales_reemplazadas.pdf  # PDF de la versión revisada
│   ├── reporte_limpieza_facebook_20261104.md              # Limpieza y unificación de Facebook
│   ├── telefonos_y_enlaces.txt          # Teléfonos y enlaces de anuncios
│   └── limpieza/                        # Material histórico de limpieza manual
├── datos/
│   ├── brutos/
│   │   ├── facebook_crudos_20261104.json       # Captura original de Facebook (43 publicaciones)
│   │   └── revolico_crudos_limpio_final.json    # Base de análisis (134 anuncios)
│   └── limpios/
│       ├── anuncios_eliminados_por_filtro_final.json  # 136 rechazados y su motivo
│       ├── facebook_publicaciones_limpias.json  # Facebook tras filtro y normalización (42)
│       ├── facebook_eliminados_por_filtro.json  # Publicación de Facebook rechazada y motivo
│       ├── datos_unificados_facebook_revolico.json   # Base unificada limpia (176: 134 Revolico + 42 Facebook)
│       └── reporte_analisis_precios_rango_p10_p90.txt
├── scripts/
│   ├── analisis_final_30_preguntas.py   # Generador canónico del informe A-F
│   ├── analisis_30_preguntas_originales_reemplazadas.py  # Generador de la versión revisada
│   ├── analisis_precios_rango_p10_p90.py
│   ├── generar_pdf_informe.py           # Conversión Markdown -> PDF (acepta --input/--output)
│   ├── limpieza_final_municipio.py
│   ├── limpiar_facebook.py              # Limpieza y normalización de Facebook
│   ├── mezclar_facebook_revolico.py     # Unificación de las bases limpias
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

Además del informe A-F, el repositorio incluye una segunda versión que parte del **cuestionario original de 30 preguntas** y conserva su numeración. Se mantienen **20 preguntas** y se reemplazan **10** que no tenían respaldo suficiente en la base de 134 anuncios:

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

El informe completo está en `analisis/informe_30_preguntas_originales_reemplazadas.md` y su PDF en `analisis/informe_30_preguntas_originales_reemplazadas.pdf`. Todas las respuestas usan la base corregida de 134 anuncios, indican `n` y nivel de evidencia, y tratan la ausencia de datos como hallazgo.

## Trazabilidad del cambio respecto a la versión anterior

La versión anterior respondía 30 preguntas sobre 171 anuncios, pero 37 de ellos mencionaban otros municipios y contaminaban la base. Esas cifras quedan supersedidas por la base estricta de 134 anuncios.

Además, cinco preguntas originales no eran estimables con los datos disponibles: mediana del alquiler, comparación de precios compra–alquiler, precio por metro cuadrado, zonas por operación y precio promedio en CUP. En esta versión se reemplazan por preguntas que sí pueden responderse, incluyendo varias que miden la ausencia de información. El detalle completo está en `analisis/informe_final.md`.

Esta trazabilidad corresponde al informe A-F. La versión revisada del cuestionario original, con sus 10 reemplazos, se documenta en la sección anterior y en `analisis/informe_30_preguntas_originales_reemplazadas.md`.

## Cómo regenerar el informe

Desde la raíz del proyecto:

```bash
python3 scripts/limpieza_final_municipio.py
python3 scripts/analisis_final_30_preguntas.py
python3 scripts/analisis_30_preguntas_originales_reemplazadas.py
python3 scripts/analisis_precios_rango_p10_p90.py
python3 scripts/limpiar_facebook.py
python3 scripts/mezclar_facebook_revolico.py
```

El primer script lee `datos/brutos/revolico_crudos_limpio.json` (270 anuncios), aplica el filtro estricto y escribe `datos/brutos/revolico_crudos_limpio_final.json` (134 anuncios) y `datos/limpios/anuncios_eliminados_por_filtro_final.json` (136 rechazados). El segundo lee la base de 134 y escribe `analisis/informe_final.md`. El tercero lee la misma base y escribe la versión revisada del cuestionario original. `limpiar_facebook.py` lee la captura `facebook_crudos_20261104.json`, aplica el mismo filtro municipal y de precio, y escribe la base limpia de Facebook y sus rechazos. `mezclar_facebook_revolico.py` une las dos bases limpias en `datos_unificados_facebook_revolico.json`. La fecha de generación cambia en cada ejecución, aunque las cifras se mantengan.

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
4. `scripts/limpieza_final_municipio.py`: aplica el filtro estricto de Diez de Octubre y precio mínimo; produce la base de 134 anuncios.
5. `scripts/limpiar_facebook.py`: aplica el mismo filtro municipal y de precio a las 43 publicaciones de Facebook, normaliza sus campos y produce 42 registros limpios y 1 rechazo documentado.
6. `scripts/mezclar_facebook_revolico.py`: unifica las bases limpias de Revolico y Facebook; produce 176 registros con fuente, tipo, zona y operación normalizados.
7. `scripts/analisis_final_30_preguntas.py`: genera el informe final con las 30 preguntas A1–F5.
8. `scripts/analisis_30_preguntas_originales_reemplazadas.py`: genera la versión revisada del cuestionario original (20 preguntas conservadas + 10 reemplazos).
9. `scripts/analisis_precios_rango_p10_p90.py`: genera el reporte de P10–P90.

> La base unificada de 176 registros es material de exploración y no alimenta las cifras del informe A-F. El informe sigue usando solo los 134 anuncios estrictos de Revolico.

## Herramientas utilizadas

- **Python** con `requests` y `BeautifulSoup` para el scraping.
- **Pandas** y **Matplotlib/Seaborn** para análisis y visualizaciones.
- **Markdown + WeasyPrint** para la entrega en PDF.
- No se usan Excel, SQL ni Power BI.
- Las dependencias de análisis están en `requirements.txt`; las de documentación, en `requirements-docs.txt`.

## Limitaciones

- Los datos del informe provienen únicamente de Revolico; no representan la totalidad del mercado físico. La base unificada añade 42 publicaciones de Facebook con fines exploratorios, pero no se usa en las cifras del informe.
- Facebook se exploró (43 publicaciones; 42 tras el filtro municipal y de precio) y se normalizó, pero no se integró al análisis cuantitativo porque su esquema original no comparte el municipio normalizado de Revolico.
- **17 de 134 anuncios (12.7%)** no declaran precio y **80 (59.7%)** no especifican zona. No se imputan valores ni ubicaciones: la ausencia se reporta como hallazgo.
- **Solo 51 de 134 (38.1%)** permiten cruzar precio y zona; **14 (10.4%)** carecen de ambos datos.
- La clasificación de tipo, zona y operación se basa en palabras clave y puede contener errores.
- Los subgrupos por zona (n = 5–14) y por tipo son pequeños; sus promedios y medianas se presentan como evidencia descriptiva.
- No hay base para estimar el precio de alquiler: solo 9 anuncios de alquiler, 1 con precio en CUP y ninguno en USD.
- Revolico no expone fecha de publicación; el ID del enlace es solo un proxy de recencia.
- El anuncio de $180,000 está clasificado como «Inmueble» porque su título no especifica «Casa»; no se reclasifica sin evidencia textual. Ese valor atípico infla la media de La Víbora, por lo que se recomienda usar la mediana.

## Exposición

El proyecto incluye materiales para una exposición de aproximadamente 5–10 minutos, pensada para personas sin conocimientos técnicos ni del tema inmobiliario. Se recomienda presentar:

1. El problema social: opacidad, dolarización, desigualdad territorial e informalidad en el mercado inmobiliario digital.
2. La fuente y la corrección de la base: 134 anuncios estrictos de Diez de Octubre (136 anuncios descartados: 133 por otro municipio o localidad y 3 por precio inferior a 1,000 USD).
3. Los hallazgos principales: precio mediano de compra, brecha territorial medida con medianas, dolarización y opacidad.
4. Qué significa esto para una persona común: no solo cuánto cuesta, sino qué información falta y quién puede acceder a ella.
5. Limitaciones y ausencia de datos como parte del resultado.
