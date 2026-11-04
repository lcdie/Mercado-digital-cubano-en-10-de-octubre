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
| **Facebook** (grupos de compraventa) | Fuente explorada: 37 publicaciones revisadas, excluidas del análisis cuantitativo por falta de un esquema homogéneo y de municipio normalizado. Se conservan para una ampliación futura. |

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
- **Facebook:** no se integra en las cifras. Sus registros usan otro esquema (precio anidado, ubicación en texto libre, sin municipio normalizado), por lo que mezclarlos sin normalizar habría contaminado el universo limpio de Revolico.
- **Campo `municipio`:** no es fiable. Todos los anuncios aparecen como «Diez de Octubre», incluso los de otros municipios. Por eso el filtro revisa título y enlace, y la exclusión municipal tiene prioridad sobre ese campo.

## Estructura del repositorio

```text
proyecto-mercado-10-octubre/
├── README.md
├── analisis/
│   ├── informe_final.md                 # Informe final con las 30 preguntas
│   ├── informe_final.pdf                # Entrega académica en PDF
│   ├── telefonos_y_enlaces.txt          # Teléfonos y enlaces de anuncios
│   └── limpieza/                        # Material histórico de limpieza manual
├── datos/
│   ├── brutos/
│   │   └── revolico_crudos_limpio_final.json    # Base de análisis (134 anuncios)
│   └── limpios/
│       ├── anuncios_eliminados_por_filtro_final.json  # 136 rechazados y su motivo
│       ├── datos_unificados_facebook_revolico.json   # Facebook + Revolico (410 registros, no usado en el informe)
│       └── reporte_analisis_precios_rango_p10_p90.txt
├── scripts/
│   ├── analisis_final_30_preguntas.py   # Generador canónico del informe
│   ├── analisis_precios_rango_p10_p90.py
│   ├── generar_pdf_informe.py           # Conversión Markdown -> PDF
│   ├── limpieza_final_municipio.py
│   ├── verificar_y_actualizar_anuncios.py
│   ├── limpiar_datos_brutos.py
│   ├── generar_lista_limpia.py
│   ├── agregar_permuta.py
│   ├── extraer_fechas_publicacion.py
│   └── mezclar_facebook_revolico*.py
├── src/
│   └── scrape_revolico.py               # Descarga de anuncios de Revolico
├── fuentes/
│   └── anuario_estadistico_notas.md     # Notas de fuentes oficiales
├── requirements.txt                     # Dependencias de análisis
├── requirements-docs.txt                # Dependencias para generar el PDF
└── LICENSE                              # Licencia MIT
```

> `datos/brutos/*.json` está en `.gitignore`; la base final se versionó con `git add -f`. Si se regenera, hay que repetir ese paso.

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

## Trazabilidad del cambio respecto a la versión anterior

La versión anterior respondía 30 preguntas sobre 171 anuncios, pero 37 de ellos mencionaban otros municipios y contaminaban la base. Esas cifras quedan supersedidas por la base estricta de 134 anuncios.

Además, cinco preguntas originales no eran estimables con los datos disponibles: mediana del alquiler, comparación de precios compra–alquiler, precio por metro cuadrado, zonas por operación y precio promedio en CUP. En esta versión se reemplazan por preguntas que sí pueden responderse, incluyendo varias que miden la ausencia de información. El detalle completo está en `analisis/informe_final.md`.

## Cómo regenerar el informe

Desde la raíz del proyecto:

```bash
python3 scripts/limpieza_final_municipio.py
python3 scripts/analisis_final_30_preguntas.py
python3 scripts/analisis_precios_rango_p10_p90.py
```

El primer script lee `datos/brutos/revolico_crudos_limpio.json` (270 anuncios), aplica el filtro estricto y escribe `datos/brutos/revolico_crudos_limpio_final.json` (134 anuncios) y `datos/limpios/anuncios_eliminados_por_filtro_final.json` (136 rechazados). El segundo lee la base de 134 y escribe `analisis/informe_final.md`. La fecha de generación cambia en cada ejecución, aunque las cifras se mantengan.

## Cómo generar la entrega en PDF

```bash
python3 -m venv .venv-docs
source .venv-docs/bin/activate
pip install -r requirements-docs.txt
python3 scripts/generar_pdf_informe.py
```

El PDF se guarda en `analisis/informe_final.pdf` e incluye portada, tablas, numeración de páginas y los datos académicos (MATCOM y profesor).

## Pipeline de datos (resumen)

1. `src/scrape_revolico.py`: descarga anuncios de Revolico.
2. `scripts/verificar_y_actualizar_anuncios.py`: verifica anuncios activos y agrega nuevos.
3. `scripts/limpiar_datos_brutos.py`: elimina anomalías graves.
4. `scripts/limpieza_final_municipio.py`: aplica el filtro estricto de Diez de Octubre y precio mínimo; produce la base de 134 anuncios.
5. `scripts/analisis_final_30_preguntas.py`: genera el informe final con las 30 preguntas A1–F5.
6. `scripts/analisis_precios_rango_p10_p90.py`: genera el reporte de P10–P90.

> Los scripts `mezclar_facebook_revolico*.py` requieren exportaciones locales de Facebook y no forman parte de la generación del informe final; se conservan como material de exploración.

## Herramientas utilizadas

- **Python** con `requests` y `BeautifulSoup` para el scraping.
- **Pandas** y **Matplotlib/Seaborn** para análisis y visualizaciones.
- **Markdown + WeasyPrint** para la entrega en PDF.
- No se usan Excel, SQL ni Power BI.
- Las dependencias de análisis están en `requirements.txt`; las de documentación, en `requirements-docs.txt`.

## Limitaciones

- Los datos provienen únicamente de Revolico; no representan la totalidad del mercado físico.
- Facebook se exploró (37 publicaciones), pero se excluyó del análisis cuantitativo por falta de un esquema homogéneo y de municipio normalizado.
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
2. La fuente y la corrección de la base: 134 anuncios estrictos de Diez de Octubre (37 anuncios contaminados retirados).
3. Los hallazgos principales: precio mediano de compra, brecha territorial medida con medianas, dolarización y opacidad.
4. Qué significa esto para una persona común: no solo cuánto cuesta, sino qué información falta y quién puede acceder a ella.
5. Limitaciones y ausencia de datos como parte del resultado.
