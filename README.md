# Mercado Inmobiliario Digital en Diez de Octubre, La Habana

**Trabajo de la asignatura Ciencia de Datos — Universidad de La Habana**  
**Facultad de Matemática y Computación (MATCOM)**  
**Profesor:** Yudivian Almeida Cruz

---

## Resumen

Este proyecto estudia el mercado inmobiliario digital de Diez de Octubre como un **problema social**: la opacidad de la información, la dolarización de los precios, la desigualdad entre barrios y las prácticas informales condicionan quién puede comprar o alquilar y en qué condiciones.

La pregunta inicial —**¿cuánto cuesta realmente vivir en Diez de Octubre?**— se responde con anuncios reales de Revolico y Facebook, pero el análisis va más allá del precio promedio: mide cuánta información falta, en qué moneda se publica y qué barrios concentran la oferta. El objetivo es ofrecer una lectura clara, sin tecnicismos, para cualquier persona interesada en comprar o alquilar vivienda en el municipio.

---

## Resumen en cifras (entrega final)

| Indicador | Valor | Fuente |
|---|---|---|
| **Universo verificado** | 122 publicaciones confirmadas | `datos/limpios/unificado_confirmados_diez_octubre.json` |
| **Revolico confirmadas** | 83 publicaciones | Corte 2026-10-31 |
| **Facebook confirmadas** | 39 publicaciones | Captura 2026-11-04 |
| **Descartados conservados** | 55 registros íntegros con motivo | `datos/limpios/descartados_diez_octubre.json` |
| **Precios en USD** | 106 de 122 (86.9%) | Análisis de precio |
| **Precio en CUP** | 1 de 122 (0.8%) | No convertido a USD |
| **Sin precio** | 15 de 122 (12.3%) | Reportado como opacidad |
| **Ventas explícitas en USD** | n = 43 | Media $26,023.26; mediana $20,000; P10–P90 $6,200–$60,000 |
| **Zona identificada** | 91 de 122 (74.6%) | 84 en ficha + 7 recuperadas del texto |
| **Sin zona** | 31 de 122 (25.4%) | Reportado como opacidad |
| **Precio y zona** | 82 de 122 (67.2%) | Permite cruce de ambos datos |
| **Sin precio ni zona** | 6 de 122 (4.9%) | Reportado como opacidad |
| **Duplicado entre fuentes** | 1 par | `facebook-35` / `revolico-58326838`; n efectivo 121 |
| **Pruebas de contrato** | 8/8 pasando | `tests/test_verificacion.py` |
| **Cifras de control** | 36/36 verificadas | `scripts/cifras_control.py` |
| **Entrevistas** | 41 (13 de audio + 24 de texto) | `evidencias/entrevistas_audio/` |
| **Capturas de Facebook** | 86 capturas de pantalla | `evidencias/facebook_fotos/` |

---

## Alcance del proyecto

Este trabajo analiza el mercado inmobiliario digital de **Diez de Octubre** específicamente. No incorpora otras provincias ni otros municipios de La Habana, y no estudia determinantes de precio fuera de este alcance. Las preguntas de investigación se centran en:

- Precios de referencia (compra y alquiler)
- Desigualdad territorial entre barrios del municipio
- Dolarización de los precios
- Opacidad de la información (precio y zona ausentes)
- Prácticas informales (oportunidad, permuta, cambio)
- Tipos de inmueble y accesibilidad

El informe final responde **30 preguntas** organizadas en seis bloques (A–F), cada una con su `n` y nivel de evidencia.

---

## Resultados principales (presentación)

Estos son los hallazgos clave del estudio, respaldados por los datos verificados y las visualizaciones en `graficos/`.

| Gráfica | Pregunta respondida | Qué muestra |
|---|---|---|
| `graficos/grafico_1_precios_venta_usd.png` | A2 — ¿Cuál es la mediana y el rango P10–P90 del precio de compra? | Distribución de 43 ventas en USD: mediana $20.000, media $26.023, P10–P90 $6.200–$60.000. La media supera la mediana por valores extremos. |
| `graficos/grafico_2_oferta_por_zona.png` | B1 — ¿Qué zonas concentran la mayor oferta? | Top-8 zonas con más anuncios. Santos Suárez, Lawton, La Víbora y El Sevillano concentran el 75.8% de las publicaciones con zona. |
| `graficos/grafico_3_media_mediana_zona.png` | B3 — ¿Qué zona tiene la mediana más alta? | Comparación media vs mediana por zona (n ≥ 5). El Sevillano lidera la mediana ($36.000), La Víbora lidera la media ($49.591) por valores extremos. |
| `graficos/grafico_4_moneda.png` | C1 — ¿Qué porcentaje de anuncios con moneda declarada está en USD? | 106 de 107 anuncios con moneda declarada están en USD (99.1%); 1 en CUP; 15 sin precio. |
| `graficos/grafico_5_opacidad.png` | D3 — ¿Cuántos anuncios carecen de precio y zona a la vez? | 67.2% tiene precio y zona; 4.9% no tiene ninguno de los dos; 25.4% sin zona; 12.3% sin precio. |

Todos los gráficos se generan con `python3 graficos/generar_graficas.py` a partir de `datos/limpios/unificado_confirmados_diez_octubre.json`.

**Informe completo:** `analisis/informe_final.md` (Markdown) y `analisis/informe_final.pdf` (PDF, 16 páginas).

**¿Qué hace singular a este estudio?** Se enfoca exclusivamente en el municipio Diez de Octubre (no en La Habana entera), aplica la **título como evidencia principal** para verificar la pertenencia municipal (corrigiendo que el campo `municipio` del scraper no es fiable), conserva íntegros los 55 registros descartados con su motivo, y reporta la ausencia de datos (sin precio, sin zona) como hallazgo, no como defecto.

---

## Estructura del repositorio

```
proyecto-mercado-10-octubre/
├── README.md
├── AGENTS.md                       # Invariantes del pipeline
├── bitacora_cambios.md             # Historia del cambio 134 → 122
├── data_dictionary.md              # Diccionario de datos y convenciones
├── fuentes/
│   ├── anuario_estadistico_notas.md    # Notas de fuentes oficiales (ONEI)
│   └── recursos_utilizados.md          # Enlaces web de fuentes primarias
├── datos/
│   ├── brutos/                     # Capturas originales (no versionadas del todo)
│   ├── geo/                        # GeoJSON municipal y caché de geocodificación
│   └── limpios/                    # Bases limpias, confirmados y descartados
├── scripts/
│   ├── verificar_municipio_publicaciones.py  # Verificación título-primero + polígono
│   ├── analisis_final_30_preguntas.py        # Generador del informe A-F
│   ├── cifras_control.py                     # Control de cifras (solo lectura)
│   ├── generar_pdf_informe.py                # Markdown → PDF
│   ├── run_all.sh                            # Pipeline en un comando
│   └── ... (otros scripts de limpieza y análisis)
├── src/
│   └── scrape_revolico.py              # Scraper de Revolico
├── tests/
│   ├── __init__.py
│   └── test_verificacion.py            # 8 pruebas de contrato
├── .github/
│   └── workflows/
│       └── ci.yml                      # Integración continua
├── requirements.txt                  # Dependencias de análisis (versiones fijadas)
├── requirements-docs.txt             # Dependencias para generar el PDF
└── LICENSE                           # Licencia MIT
```

---

## Pipeline de entrega (4 pasos)

Desde la raíz del proyecto, ejecutar en este orden:

```bash
# 1. Verificación municipal (título primero + polígono + geocodificación)
python3 scripts/verificar_municipio_publicaciones.py

# 2. Informe A-F (30 preguntas sobre las 122 confirmadas)
python3 scripts/analisis_final_30_preguntas.py

# 3. Control de cifras (valida 36 cifras contra los datos generados)
python3 scripts/cifras_control.py

# 4. Pruebas de contrato (8 pruebas, sin red)
python3 -m unittest discover -s tests -t .
```

El paso 1 produce `datos/limpios/unificado_confirmados_diez_octubre.json` (122 confirmados) y
`datos/limpios/descartados_diez_octubre.json` (55 descartes íntegros con motivo).

El paso 2 genera `analisis/informe_final.md`.

El paso 3 valida que todas las cifras del informe coincidan con los datos.

El paso 4 ejecuta las pruebas de contrato que protegen el universo (122 confirmados, 55
descartes, integridad de registros, no solapamiento, estadísticos de ventas, duplicado conocido).

Para regenerar el PDF:

```bash
.venv-docs/bin/python scripts/generar_pdf_informe.py
```

O en un solo comando:

```bash
bash scripts/run_all.sh
```

---

## Metodología y verificación municipal

### Regla de título primero

El campo `municipio` del scraper no es fiable: asigna «Diez de Octubre» a anuncios que en su ficha declaran otro municipio. Por eso se aplicó el **título como evidencia principal**:

- Si el título nombra Diez de Octubre o un reparto interno (Santos Suárez, Lawton, La Víbora, Luyanó, El Sevillano, etc.), la publicación se confirma.
- Si el título nombra un lugar externo (Otro municipio, provincia o localidad), se descarta aunque la ficha diga Diez de Octubre.
- Solo cuando el título no aporta señal se recurre a la ficha de Revolico y al resto del texto (enlace, grupo, ubicación o zona).
- Los topónimos se geocodificaron con Nominatim y se comprobó punto-en-polígono contra `datos/geo/lha.geojson` (DPA 23.09).

### Resultados de la verificación

| Resultado | Revolico (n=134) | Facebook (n=42) | Unificado (n=176) |
|---|---:|---:|---:|
| SÍ, dentro de Diez de Octubre | 83 | 39 | **122** |
| NO, otro municipio | 46 | 0 | 46 |
| CONTRADICTORIO | 0 | 0 | 0 |
| INDETERMINADO | 5 | 3 | 8 |

Los **55 registros no incluidos** (46 `NO`, 8 `INDETERMINADO` y 1 fuera del universo: `facebook-27`) se conservan íntegros en `datos/limpios/descartados_diez_octubre.json` y `.csv`, con su motivo, su registro original y el registro unificado exacto. No se elimina información.

---

## Control de calidad y pruebas

- **`scripts/cifras_control.py`**: imprime y valida 36 cifras del informe (conteos, precios, zonas, opacidad, duplicados, cobertura por campo). Sale con código 0 si todo cuadra.
- **`tests/test_verificacion.py`**: 8 pruebas de contrato que protegen el universo verificado. Ejecutar con `python3 -m unittest discover -s tests -t .`.
- **`.github/workflows/ci.yml`**: integración continua que ejecuta pruebas y cifras de control en cada push.
- **`data_dictionary.md`**: diccionario de datos, convenciones de nulos (nunca se imputan), cobertura por campo y estadísticos clave.
- **`bitacora_cambios.md`**: historia del cambio de universo 134 → 122, regla de título, archivos regenerados y decisiones manuales.

---

## Las 30 preguntas de investigación

Las preguntas se organizan en seis bloques sociales. Cada respuesta del informe final indica su `n`, su nivel de evidencia (sólida, descriptiva o no estimable) y, cuando corresponde, la ausencia de datos como hallazgo.

- **Bloque A — Precios de referencia** (A1–A5): precio promedio, mediana y P10–P90 de compra; alquiler sin precio estimable; proporción de alquileres con precio.
- **Bloque B — Desigualdades territoriales** (B1–B5): zonas con mayor oferta, zona con media y mediana más altas, brecha La Víbora–Lawton, falta de zona por operación.
- **Bloque C — Dolarización** (C1–C5): proporción en USD sobre moneda declarada y sobre total; variación por tipo y zona; cota superior si los sin precio fueran USD o CUP.
- **Bloque D — Opacidad de la información** (D1–D5): sin precio, sin zona, sin ambos, información mínima completa, opacidad por operación.
- **Bloque E — Prácticas informales** (E1–E5): lenguaje informal, palabras dominantes, declaración de precio, concentración por operación, opacidad de sin clasificar.
- **Bloque F — Tipos de inmueble y accesibilidad** (F1–F5): tipo más publicado, tipo más barato por media y mediana, mantenimiento de la diferencia en P10–P90, tipo más opaco.

El informe completo está en `analisis/informe_final.md` y su entrega en `analisis/informe_final.pdf`.

---

## Limitaciones y alcance

- **Muestra no probabilística:** 122 publicaciones es una base pequeña y no necesariamente representativa del universo de viviendas del municipio. No hay serie temporal: el corte de Revolico es único (2026-10-31) y Facebook no tiene fechas homogéneas.
- **Integración de fuentes heterogéneas:** Revolico y Facebook no comparten esquema. Facebook aporta descripciones y precios, pero muchas publicaciones no tienen título ni texto crudo homogéneo, lo que eleva el «sin clasificar» y reduce la medición de informalidad a Revolico. Las comparaciones entre fuentes deben leerse como descriptivas.
- **Verificación municipal:** el polígono es una simplificación de 11 vértices y no resuelve casos catastrales a pocos metros del borde. La regla de título usa la mención textual del anuncio; cuando el título es ambiguo (por ejemplo, «Ampliación del Sevillano» o «Reparto Flores»), la publicación se conserva con confianza media y la ambigüedad se documenta. Las 8 indeterminadas se excluyen, lo que puede introducir un sesgo de selección.
- **Campos ausentes:** no hay datos homogéneos de metros cuadrados, estado legal, número de baños, año de construcción, vendedor o agencia. Solo 6 publicaciones de Facebook traen `area_m2`, y ninguna de Revolico: no se puede calcular precio por m² ni distinguir particulares de intermediarios.
- **Alquiler:** solo 3 publicaciones, 1 con precio y ninguno en USD. No se puede estimar un precio de alquiler ni comparar compra y alquiler.
- **Precios de oferta:** los valores son precios publicados, no precios de transacción. La diferencia entre lo que se pide y lo que se paga no es observable con estos datos.
- **Sesgo de publicación:** las viviendas que no se publican, o que se publican en canales cerrados, no aparecen en la base. La opacidad medida es la del mercado digital visible, no la del mercado total.
- **No se imputan valores:** una publicación sin precio, sin zona o sin operación no se elimina del universo. Se conserva y se contabiliza como indicador de opacidad, porque su ausencia también describe el mercado.

---

> **Nota sobre la evidencia:** los precios son precios de oferta, no de transacción. No hay datos homogéneos de metros cuadrados, habitaciones, baños, estado legal ni año de construcción. Las ausencias se reportan; no se imputan.

## Herramientas utilizadas

Este proyecto fue desarrollado utilizando el siguiente conjunto de herramientas:

### Entorno de desarrollo
- **Archlinux** — Sistema operativo utilizado para todo el desarrollo.
- **Vim y Visual Studio Code** — Editores de código utilizados para escribir y editar los scripts y la documentación.
- **Python 3.x** — Lenguaje de programación principal.

### Librerías y paquetes de Python
- **pandas** — Manipulación y análisis de datos tabulares.
- **matplotlib / seaborn** — Generación de visualizaciones estadísticas (gráficos de exposición).
- **requests** — Peticiones HTTP para scraping y obtención de datos.
- **BeautifulSoup4** — Parseo de HTML para extracción de anuncios de Revolico.
- **weasyprint** — Conversión de Markdown a PDF para el informe final.
- **markdown** — Procesamiento de archivos Markdown.

### Herramientas geoespaciales y de datos
- **GeoJSON municipal DPA 23.09** (`datos/geo/lha.geojson`) — Polígono de La Habana para verificación punto-en-polígono.
- **Nominatim / OpenStreetMap** — Geocodificación de topónimos a coordenadas (caché en `datos/geo/geocoding_lha.json`).
- **ONEI / Anuario Estadístico de Cuba** — Contexto oficial de población, vivienda y tenencia (`fuentes/anuario_estadistico_notas.md`).

### Herramientas de control de calidad y reproducibilidad
- **Git / GitHub** — Control de versiones y alojamiento del repositorio (`lcdie/Mercado-digital-cubano-en-10-de-octubre`).
- **GitHub Actions** — Integración continua que ejecuta pruebas y cifras de control en cada push.
- **OpenCode (Nemotron 3.5 Super VL Free)** — Asistente de IA utilizado para redactar scripts, documentar, estructurar el repositorio, revisar consistencia de cifras y redactar el informe y la presentación. Todas las decisiones de análisis y clasificación municipal fueron validadas por el autor del proyecto.
- **Deepseek y ChatGPT** — Modelos de lenguaje adicionales utilizados para revisar código, generar ideas y redactar secciones del informe. Todas las decisiones finales fueron revisadas y validadas por el autor del proyecto.

### Herramientas de captura y transcripción
- **whisper.cpp (modelo base)** — Transcripción automática de las 13 grabaciones de audio de entrevistas (`evidencias/entrevistas_audio/`). Las transcripciones no se incluyen en el repositorio para proteger la privacidad de los entrevistados.
- **Samsung Galaxy A56** — Dispositivo móvil utilizado para grabar las entrevistas de audio.
- **Capturas de pantalla** — 86 capturas de publicaciones de Facebook (`evidencias/facebook_fotos/`), utilizadas como evidencia visual de anuncios publicados.

### Herramientas de análisis estadístico
- **Python `statistics`** — Cálculo de mediana, percentiles P10 y P90.
- **`collections.Counter`** — Conteo de frecuencias por fuente, zona, tipo de inmueble, operación y moneda.
- **JSON** — Formato de almacenamiento de bases de datos limpias y descartes.

### Bases de datos
No se utilizó ningún sistema de gestión de bases de datos relacional o NoSQL. Todos los datos se almacenan en archivos JSON y CSV planos.

## Referencias

- **ONEI.** *Anuario Estadístico de Cuba*. Oficina Nacional de Estadística e Información, República de Cuba. Notas de uso en `fuentes/anuario_estadistico_notas.md`.
- **OpenStreetMap / Nominatim.** Servicio de geocodificación usado para traducir topónimos a coordenadas; resultados cacheados en `datos/geo/geocoding_lha.json`.
- **GeoJSON municipal.** `datos/geo/lha.geojson`, copia versionada del polígono de La Habana; SHA-256 `b9bbcce811d9bbfcee15f5e904d97dc24cf044cabcf17a870487ad361bb7c9e6`.
- **Revolico.** Portal de anuncios clasificados; captura del 2026-10-31. `https://www.revolico.com`.
- **Facebook.** Publicaciones de grupos y páginas de compraventa; captura del 2026-11-04. `https://www.facebook.com`. No se reproducen enlaces individuales ni nombres de grupos por privacidad.

## Evidencia cualitativa complementaria

Además de los 122 anuncios verificados, el proyecto incluye evidencia cualitativa que no forma parte del universo cuantitativo, pero que aporta contexto sobre la percepción del mercado en Diez de Octubre:

- **41 entrevistas** (13 de audio y 24 de texto, E-01 a E-41): grabaciones anónimas de residentes sobre su experiencia buscando, comprando, vendiendo o alquilando vivienda en el municipio. No constituyen una muestra representativa; se usan como evidencia cualitativa suelta que ilustra temas como opacidad, dolarización e informalidad.
- **86 capturas de pantalla de Facebook**: anuncios publicados en grupos y páginas de compraventa, capturados entre octubre y noviembre de 2026. Se usan como referencia visual del tipo de publicaciones que circulan en canales informales.

> **Nota:** ni las entrevistas ni las capturas de Facebook se contabilizan como parte del universo de 122 publicaciones verificadas. No se hace mapeo por zonas ni se calculan porcentajes sobre ellas; se presentan como acompañamiento cualitativo del informe principal.

> **Nota sobre la evidencia:** los precios son precios de oferta, no de transacción. No hay datos homogéneos de metros cuadrados, habitaciones, baños, estado legal ni año de construcción. Las ausencias se reportan; no se imputan.

---

**Proyecto de Ciencia de Datos — Universidad de La Habana**  
Facultad de Matemática y Computación (MATCOM)  
Profesor: **Yudivian Almeida Cruz**  
Repositorio: `Mercado-digital-cubano-en-10-de-octubre`
