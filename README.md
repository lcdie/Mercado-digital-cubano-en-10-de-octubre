# Mercado Inmobiliario Digital en Diez de Octubre, La Habana

**Trabajo de la asignatura Ciencia de Datos — Universidad de La Habana**  
**Facultad de Matemática y Computación (MATCOM)**  
**Profesor:** Yudivian Almeida Cruz

## Historia del proyecto

Este proyecto responde a una pregunta sencilla: **¿Cuánto cuesta realmente vivir en el municipio Diez de Octubre, La Habana?**

Una persona que quiera comprar o alquilar una vivienda en esa zona no tiene una referencia clara de precios ni de qué tipo de inmuebles están disponibles en el mercado digital. Con este trabajo se caracteriza el mercado inmobiliario local usando:

1. Anuncios reales publicados en línea (Revolico).
2. Datos oficiales del Anuario Estadístico de Cuba (ONEI) como contexto general.

El objetivo es ofrecer una guía clara, sin tecnicismos, para cualquier persona interesada en comprar o alquilar vivienda en Diez de Octubre: cuánto cuesta, en qué zona, qué características afectan el precio y en qué moneda se declaran los anuncios.

## Objetivos

- Analizar la oferta inmobiliaria publicada en plataformas digitales cubanas enfocada al municipio Diez de Octubre.
- Caracterizar precios, tipos de inmueble, zonas, moneda declarada y características físicas.
- Responder 30 preguntas de investigación coherentes entre sí, comunicables a personas sin conocimientos técnicos ni del tema inmobiliario.
- Proporcionar una base replicable y abierta para futuros análisis del mercado digital cubano.

## Fuentes de datos

| Fuente | Uso en el proyecto |
|--------|--------------------|
| **Revolico** (scraping propio) | Fuente principal y única usada en los cálculos: 171 anuncios limpios de Diez de Octubre con precios, tipos, zonas y moneda. |
| **Anuario Estadístico de Cuba (ONEI)** | Contexto oficial del municipio (población, vivienda y tenencia); no se usa para calcular precios de la muestra digital. |
| **Facebook** (grupos de compraventa) | Fuente explorada: 37 publicaciones revisadas, excluidas del análisis cuantitativo por falta de un esquema homogéneo y de municipio normalizado. Se conservan para una ampliación futura. |

> **El Caimán fue descartado:** sus datos no correspondían al municipio Diez de Octubre. No se usa en ninguna cifra del informe.

> Nota: este proyecto no aborda aspectos políticos ni hace comparativas que no sean directamente hacia el mercado inmobiliario.

## Universo y metodología

- **Universo final:** 171 anuncios limpios de Revolico, todos del municipio Diez de Octubre.
- **Precios:** 136 anuncios declaran precio en USD, 1 en CUP y 34 no declaran precio. Los análisis de precio usan los 136 en USD.
- **Valores extremos:** se reporta la mediana y el tramo P10–P90 junto a la media. P10 = $8,000, P90 = $70,000; 110 anuncios quedan dentro del tramo.
- **Tamaño de muestra:** cada respuesta indica su `n`. Los subgrupos con `n < 10` se presentan como evidencia descriptiva, no como conclusión firme.
- **Clasificación:** tipo, zona y características se infieren de palabras clave del título y del enlace. Puede contener errores.
- **Recencia:** Revolico no expone la fecha de publicación; el ID numérico del enlace se usa como proxy.
- **Facebook:** no se integra en las cifras. Sus registros usan otro esquema (precio anidado, ubicación en texto libre, sin municipio normalizado), por lo que mezclarlos sin normalizar habría contaminado el universo limpio de Revolico.

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
│   │   └── revolico_crudos_limpio_final.json    # Base de análisis (171 anuncios)
│   └── limpios/
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

### Bloque A: Precios del mercado (6)

1. ¿Cuál es el precio promedio de los anuncios con precio declarado en USD en Diez de Octubre?
2. ¿Cuál es el precio mediano de los anuncios con precio declarado en USD?
3. ¿Cuál es el rango de precios que cubre el 80% central de los anuncios?
4. ¿Cuáles son el anuncio más caro y el más barato publicados?
5. ¿Qué proporción de anuncios no declara precio?
6. ¿Qué tan dispersos son los precios respecto a la media?

### Bloque B: Tipos de inmueble (6)

7. ¿Cuáles son los tipos de inmueble más publicados?
8. ¿Qué porcentaje son casas independientes frente a apartamentos?
9. ¿Cuál es el precio promedio por tipo de inmueble (anuncios con precio en USD)?
10. ¿Qué tipo de inmueble concentra el precio máximo declarado?
11. ¿Cuántos anuncios se identifican como venta, alquiler o sin clasificar?
12. ¿Qué tipo de inmueble domina en la zona con el precio promedio más alto?

### Bloque C: Características físicas (6)

13. ¿Cuál es la cantidad más común de cuartos/habitaciones?
14. ¿Cómo varía el precio según el número de cuartos?
15. ¿Qué porcentaje de anuncios menciona garaje y cómo se relaciona con el precio?
16. ¿Cuántos anuncios especifican «planta baja» y cuál es su precio promedio?
17. ¿Qué proporción de anuncios incluye al menos una característica física explícita?
18. ¿Qué características físicas se mencionan con más frecuencia?

### Bloque D: Ubicación dentro de Diez de Octubre (6)

19. ¿Qué zonas o barrios aparecen con más frecuencia en los anuncios?
20. ¿Qué zona tiene el precio promedio más alto entre los anuncios con precio en USD?
21. ¿Qué zona tiene la mayor cantidad de anuncios publicados?
22. ¿Hay diferencia de precios entre zonas dentro del mismo municipio?
23. ¿Qué proporción de los anuncios con zona identificada se concentra en las cuatro zonas principales?
24. ¿Cuántos anuncios no especifican zona dentro del municipio?

### Bloque E: Moneda y mercado informal (6)

25. ¿Qué proporción de anuncios con moneda declarada usa USD frente a CUP?
26. ¿Los anuncios con lenguaje informal declaran precio con más frecuencia que los anuncios con lenguaje neutro?
27. ¿Qué porcentaje de anuncios incluye palabras de mercado informal?
28. ¿Qué rango de precios es más frecuente entre los anuncios con precio en USD?
29. ¿Cuántos anuncios parecen de particulares frente a posibles anuncios repetidos o agencias?
30. ¿Qué recomendación práctica se puede hacer a alguien que quiera comprar o alquilar en Diez de Octubre?

## Preguntas sustituidas

Cinco preguntas del cuestionario original no tenían base suficiente y se sustituyeron por preguntas respondibles. La sustitución está documentada en el informe final.

| # | Pregunta original | Motivo | Pregunta actual |
|---|---|---|---|
| 2 | Mediana del precio de alquiler | Solo 2 alquileres declaran precio (1 USD, 1 CUP) | Mediana de los anuncios con precio en USD |
| 6 | ¿Es más caro comprar que alquilar? | Solo 1 alquiler tiene precio en USD | Dispersión de precios respecto a la media |
| 17 | Precio promedio por metro cuadrado | Solo 3 anuncios mencionan metraje | Proporción con al menos una característica física |
| 23 | Zonas con más venta y alquiler | Solo una zona tiene algún alquiler | Concentración en las cuatro zonas principales |
| 26 | Precio promedio en CUP | Solo 1 anuncio declara precio en CUP | Lenguaje informal y declaración de precio |

Además, **Q1** se reformuló de «precio de venta» a «anuncios con precio declarado en USD», porque solo 50 anuncios se identifican explícitamente como venta. Por la misma razón, **Q20** y **Q28** se expresan sobre anuncios con precio en USD. El subconjunto de ventas explícitas se reporta por separado (media $22,880, mediana $17,000, n = 50).

## Cómo regenerar el informe

Desde la raíz del proyecto:

```bash
python3 scripts/analisis_final_30_preguntas.py
python3 scripts/analisis_precios_rango_p10_p90.py
```

El primer script lee `datos/brutos/revolico_crudos_limpio_final.json` y escribe `analisis/informe_final.md`. La fecha de generación cambia en cada ejecución, aunque las cifras se mantengan.

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
4. `scripts/limpieza_final_municipio.py`: aplica el filtro estricto de Diez de Octubre y precio mínimo.
5. `scripts/analisis_final_30_preguntas.py`: genera el informe final.
6. `scripts/analisis_precios_rango_p10_p90.py`: genera el reporte de P10–P90.

## Herramientas utilizadas

- **Python** con `requests` y `BeautifulSoup` para el scraping.
- **Pandas** y **Matplotlib/Seaborn** para análisis y visualizaciones.
- **Markdown + WeasyPrint** para la entrega en PDF.
- No se usan Excel, SQL ni Power BI.
- Las dependencias de análisis están en `requirements.txt`; las de documentación, en `requirements-docs.txt`.

## Limitaciones

- Los datos provienen únicamente de Revolico; no representan la totalidad del mercado físico.
- Facebook se exploró (37 publicaciones), pero se excluyó del análisis cuantitativo por falta de un esquema homogéneo y de municipio normalizado.
- 34 de 171 anuncios (19.9%) no declaran precio y 117 (68.4%) no especifican zona. No se imputan valores ni ubicaciones.
- La clasificación de tipo, zona y características se basa en palabras clave y puede contener errores.
- Los subgrupos por zona, garaje, planta baja y número de cuartos son pequeños; sus promedios son descriptivos.
- No hay base para analizar el alquiler: solo 1 anuncio de alquiler declara precio en USD y 1 en CUP.
- Revolico no expone fecha de publicación; el ID del enlace es solo un proxy de recencia.
- El anuncio de $180,000 está clasificado como «Inmueble» porque su título no especifica «Casa»; no se reclasifica sin evidencia textual.

## Exposición

El proyecto incluye materiales para una exposición de aproximadamente 5–10 minutos, pensada para personas sin conocimientos técnicos ni del tema inmobiliario. Se recomienda presentar:

1. El problema: ¿cuánto cuesta vivir en Diez de Octubre?
2. La fuente: anuncios reales de Revolico + contexto del Anuario Estadístico.
3. Los 3 hallazgos más importantes: precio mediano, zona más cara y tipo más común.
4. Qué significa esto para una persona común.
5. Limitaciones de los datos.
