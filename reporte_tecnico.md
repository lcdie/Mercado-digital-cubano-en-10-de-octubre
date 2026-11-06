# Reporte Técnico — Mercado Inmobiliario Digital en Diez de Octubre, La Habana

**Proyecto:** Ciencia de Datos — Universidad de La Habana, Facultad de Matemática y Computación (MATCOM)  
**Profesor:** Yudivian Almeida Cruz  
**Tema:** Opacidad, dolarización, desigualdad territorial e informalidad del mercado inmobiliario digital de Diez de Octubre  
**Versión:** 1.0 — Entrega final  
**Fecha:** Noviembre de 2026  
**Universo canónico:** 122 publicaciones confirmadas (83 de Revolico + 39 de Facebook)

---

## 1. Resumen ejecutivo

Este reporte documenta el proceso completo de obtención, verificación, limpieza, análisis y control de calidad del mercado inmobiliario digital de Diez de Octubre, La Habana, a partir de anuncios publicados en Revolico y Facebook.

El universo final del análisis es de **122 publicaciones confirmadas dentro del municipio**, obtenidas tras verificar 176 publicaciones unificadas contra un polígono municipal y aplicar la **regla de título como evidencia principal**. De las 176 publicaciones, 46 pertenecen a otro municipio, 8 son indeterminadas y 1 (`facebook-27`) ya estaba fuera de la base unificada. Los 55 registros descartados se conservan íntegros con su motivo de descarte, su registro original y su registro unificado exacto.

Los hallazgos principales son:

- **Dolarización:** 106 de 107 publicaciones con moneda declarada (99,1 %) están en USD; en el total, el 86,9 % del universo declara USD.
- **Precio de compra:** mediana de $20.000 USD, media de $26.023,26 USD, P10–P90 de $6.200–$60.000 USD (n = 43 ventas explícitas en USD).
- **Alquiler:** no es estimable; solo 3 publicaciones, 1 con precio en CUP y ninguna en USD.
- **Opacidad:** 15 publicaciones (12,3 %) no declaran precio; 31 (25,4 %) no especifican zona; solo 82 (67,2 %) permiten cruzar precio y zona; 6 (4,9 %) carecen de ambos datos.
- **Desigualdad territorial:** las cuatro zonas principales (Santos Suárez, Lawton, La Víbora, El Sevillano) concentran 69 de 91 publicaciones con zona (75,8 %). La Víbora tiene la media más alta entre zonas con n ≥ 10 ($49.590,91 USD, n = 11); El Sevillano tiene la mediana más alta ($36.000 USD, n = 10).
- **Duplicado conocido:** 1 par entre fuentes (`facebook-35` / `revolico-58326838`, misma propiedad y precio); se conserva y el n efectivo es 121.

---

## 2. Objetivos y alcance

### Objetivo general

Analizar la oferta inmobiliaria publicada en plataformas digitales enfocada al municipio Diez de Octubre, caracterizando precios, tipos de inmueble, zonas, moneda declarada y opacidad de la información, sin imputar valores ausentes.

### Alcance temático

Este reporte se limita a **Diez de Octubre**. No incorpora otros municipios de La Habana, ni fuentes como Cubisima o HogarEnCuba, ni entrevistas, ni tasas de cambio, ni determinantes de precio fuera de este municipio. Esa decisión respeta la independencia temática del proyecto frente a otros trabajos de la misma asignatura.

### Preguntas de investigación

El informe final responde **30 preguntas** organizadas en seis bloques:

- **Bloque A — Precios de referencia** (A1–A5)
- **Bloque B — Desigualdades territoriales** (B1–B5)
- **Bloque C — Dolarización** (C1–C5)
- **Bloque D — Opacidad de la información** (D1–D5)
- **Bloque E — Prácticas informales** (E1–E5)
- **Bloque F — Tipos de inmueble y accesibilidad** (F1–F5)

Cada respuesta indica su `n`, nivel de evidencia (sólida, descriptiva o no estimable) y trata la ausencia de datos como hallazgo, no como defecto.

---

## 3. Obtención de datos

### 3.1 Fuentes primarias

| Fuente | Tipo | Enlace web | Corte / Captura | Confirmadas |
|---|---|---|---|---|
| Revolico | Portal de anuncios clasificados | https://www.revolico.com | 2026-10-31 | 83 |
| Facebook | Grupos y páginas de compraventa | https://www.facebook.com | 2026-11-04 | 39 |

- **Revolico:** Se extrajeron título, precio, enlace, fecha de verificación y zona cuando estaban disponibles. No expone fecha de publicación; `fecha_verificacion` registra el momento de captura.
- **Facebook:** Se capturaron precio y descripción. Muchas publicaciones no tienen título ni texto crudo homogéneo; por privacidad no se reproducen enlaces individuales ni nombres de grupos.

### 3.2 Recursos geoespaciales y oficiales

| Recurso | Uso | Archivo |
|---|---|---|
| GeoJSON municipal de La Habana (DPA 23.09) | Comprobación punto-en-polígono | `datos/geo/lha.geojson` |
| Nominatim / OpenStreetMap | Geocodificación de topónimos | `datos/geo/geocoding_lha.json` |
| ONEI — Anuario Estadístico de Cuba | Contexto oficial de población y vivienda | `fuentes/anuario_estadistico_notas.md` |

---

## 4. Metodología

### 4.1 Pipeline de datos

El pipeline se ejecuta en cuatro pasos, definidos en `scripts/run_all.sh`:

1. **Verificación municipal:** título primero + polígono municipal + geocodificación (`scripts/verificar_municipio_publicaciones.py`).
2. **Informe A-F:** 30 preguntas sobre las 122 confirmadas (`scripts/analisis_final_30_preguntas.py`).
3. **Control de cifras:** validación de 36 cifras contra los datos generados (`scripts/cifras_control.py`).
4. **Pruebas de contrato:** 8 pruebas automatizadas sin red (`tests/test_verificacion.py`).

### 4.2 Regla de verificación municipal (título primero)

El campo `municipio` del scraper no es fiable: asigna «Diez de Octubre» a anuncios de otros municipios. Por eso se aplicó el título como evidencia principal:

- **SÍ:** el título nombra Diez de Octubre o un reparto interno del municipio.
- **NO:** el título nombra un lugar externo a Diez de Octubre, aunque la ficha declare el municipio.
- **INDETERMINADO:** ninguna evidencia alcanza para decidir.
- Solo si el título no aporta señal se usa la ficha, el enlace, el grupo, la ubicación o la zona como respaldo.
- Los topónimos se geocodificaron con Nominatim y se comprobó punto-en-polígono contra `datos/geo/lha.geojson`.

### 4.3 Limpieza y unificación

- 134 anuncios de Revolico etiquetados como Diez de Octubre + 42 de Facebook = 176 registros unificados.
- Tras verificación: 122 confirmados (83 Revolico + 39 Facebook), 46 NO, 8 INDETERMINADO, 0 CONTRADICTORIO.
- Los 55 descartes se conservan íntegros en `datos/limpios/descartados_diez_octubre.json` y `.csv`, con motivo, evidencia, `registro_original` y `registro_unificado` exacto. No se elimina información.

---

## 5. Base de datos

### 5.1 Universo final

| Métrica | Valor |
|---|---|
| Publicaciones confirmadas | 122 |
| Revolico confirmadas | 83 |
| Facebook confirmadas | 39 |
| Descartados conservados | 55 (47 NO, 8 INDETERMINADO, 1 fuera del universo) |
| Registros unificados totales | 176 |
| Base histórica no verificada (referencia) | 134 (no comparable) |

### 5.2 Cobertura por campo

| Campo | Cobertura | n | Lectura |
|---|---:|---:|---|
| Precio en USD | 86,9 % | 106/122 | Base principal de análisis de precio |
| Precio en CUP | 0,8 % | 1/122 | No convertido a USD |
| Sin precio | 12,3 % | 15/122 | Reportado como opacidad |
| Zona identificada | 74,6 % | 91/122 | 84 en ficha + 7 recuperadas del texto |
| Sin zona | 25,4 % | 31/122 | Reportado como opacidad |
| Operación declarada | 43,4 % | 53/122 | 50 ventas, 3 alquileres, 69 sin clasificar |
| Precio y zona | 67,2 % | 82/122 | Permite cruce de ambos datos |
| Sin precio ni zona | 4,9 % | 6/122 | Reportado como opacidad |
| Habitaciones | 0,0 % | 0/122 | No hay campo homogéneo |
| Baños | 0,0 % | 0/122 | No hay campo homogéneo |
| Superficie (m²) | 4,9 % | 6/122 | Solo Facebook (`area_m2`) |
| Teléfono | 23,8 % | 29/122 | Contacto declarado |
| Enlace | 68,0 % | 83/122 | Todos de Revolico |

### 5.3 Esquema de datos

Cada registro de `unificado_confirmados_diez_octubre.json` contiene:

- `id_unico`, `fuente` (`revolico` / `facebook`)
- `publicacion` (título, enlace, fecha, grupo, autor)
- `precio` (monto, moneda, negociable, nota, monto_actual)
- `operacion` (Venta / Alquiler / Sin clasificar)
- `detalles_propiedad` (tipo, tipo_original, ubicación, zona, distribución)
- `contacto` (teléfono, método)
- `equipamiento_incluido`, `servicios_y_caracteristicas`, `extras`
- `verificacion_municipal` (resultado, confianza, evidencia_principal, motivo, ficha)
- `posibles_duplicados`, `fecha_verificacion`

Cada registro de `descartados_diez_octubre.json` conserva además `motivo_descarte`, `en_universo_unificado`, `registro_original` y `registro_unificado`.

---

## 6. Resultados principales

### 6.1 Precios de compra (ventas en USD)

| Estadístico | Valor | n |
|---|---|---|
| Mediana | $20.000,00 | 43 |
| Media | $26.023,26 | 43 |
| P10 | $6.200,00 | 43 |
| P90 | $60.000,00 | 43 |
| Mínimo | — | 43 |
| Máximo | — | 43 |

### 6.2 Dolarización

| Métrica | Valor |
|---|---|
| Publicaciones con moneda declarada en USD | 106 de 107 (99,1 %) |
| USD sobre el total del universo | 106 de 122 (86,9 %) |
| Cota superior posible (incluyendo sin precio) | 99,2 % |
| Único precio en CUP | Alquiler (no convertido) |

### 6.3 Desigualdad territorial

| Zona | Media (USD) | Mediana (USD) | n |
|---|---|---|---|
| El Mónaco | $57.666,67 | $33.000,00 | 6 |
| La Víbora | $49.590,91 | $26.000,00 | 11 |
| El Sevillano | $39.700,00 | $36.000,00 | 10 |
| Santa Catalina | $37.200,00 | $35.000,00 | 5 |
| Santos Suárez | $31.565,22 | $22.500,00 | 23 |
| Luyano | $25.928,57 | $25.000,00 | 7 |
| Lawton | $20.656,25 | $20.000,00 | 16 |

- Top-4 zonas concentran 69 de 91 publicaciones con zona (75,8 %).
- Entre n ≥ 10: media más alta = La Víbora; mediana más alta = El Sevillano.
- Entre n ≥ 5: media más alta = El Mónaco; mediana más alta = El Sevillano.

### 6.4 Opacidad

| Indicador | Valor | % |
|---|---|---|
| Sin precio | 15 de 122 | 12,3 % |
| Sin zona | 31 de 122 | 25,4 % |
| Precio y zona | 82 de 122 | 67,2 % |
| Sin precio ni zona | 6 de 122 | 4,9 % |

### 6.5 Prácticas informales

- 12 publicaciones (9,8 %) usan lenguaje informal («oportunidad», «ganga», «permuta», «intercambio», «cambio»).
- Todas son de Revolico; el dato es una cota inferior.

### 6.6 Tipos de inmueble

| Tipo | Media (USD) | Mediana (USD) | n |
|---|---|---|---|
| Apartamento | $18.181,82 | $15.000,00 | 33 |
| Casa | $42.842,11 | $33.000,00 | 57 |
| Inmueble (sin tipo específico) | — | — | 19 |
| Cuarto | — | — | 2 |

- El apartamento es la opción más accesible.
- El duplicado conocido (`facebook-35` / `revolico-58326838`, misma propiedad y precio) se conserva; n efectivo = 121.

---

## 7. Control de calidad y pruebas

### 7.1 Cifras de control

`scripts/cifras_control.py` valida 36 cifras del informe contra los datos generados. Todas coinciden (resultado: OK). Cubre: conteos por fuente, composición de descartes, precios USD/CUP/sin precio, estadísticos de ventas, zonas, opacidad, duplicado, cobertura por campo y porcentajes clave.

### 7.2 Pruebas de contrato

`tests/test_verificacion.py` contiene 8 pruebas de contrato:

1. Universo confirmado = 122.
2. Fuentes = 83 Revolico / 39 Facebook.
3. Descartados = 55 y composición correcta.
4. Descartados conservan `registro_original` y `registro_unificado`.
5. Confirmados y descartados no se solapan.
6. Ningún confirmado tiene título de lugar externo.
7. Estadísticos de ventas USD correctos.
8. Duplicado conocido y n efectivo = 121.

Resultado: 8/8 pasando.

### 7.3 Integración continua

`.github/workflows/ci.yml` ejecuta pruebas y cifras de control en cada push a `main`.

### 7.4 Documentación de soporte

- `AGENTS.md`: invariantes del pipeline (título primero, no borrar descartes, universo 122, no añadir fuentes ajenas).
- `data_dictionary.md`: diccionario de datos, convenciones de nulos, cobertura por campo.
- `bitacora_cambios.md`: historia 134 → 122, regla de título, archivos regenerados.
- `fuentes/recursos_utilizados.md`: enlaces web de fuentes primarias.

---

## 8. Limitaciones

- **Muestra no probabilística:** 122 publicaciones es una base pequeña y no necesariamente representativa del universo de viviendas del municipio.
- **Sin serie temporal:** corte único de Revolico (2026-10-31); Facebook sin fechas homogéneas.
- **Integración heterogénea:** Revolico y Facebook no comparten esquema; la medición de informalidad es una cota inferior (solo Revolico).
- **Verificación municipal:** polígono de 11 vértices; no resuelve casos catastrales al borde; depende de topónimos declarados.
- **Campos ausentes:** no hay metros cuadrados, habitaciones, baños, estado legal, año de construcción, vendedor o agencia homogéneos.
- **Alquiler:** no estimable (3 publicaciones, 1 con precio en CUP, ninguna en USD).
- **Precios de oferta:** no son precios de transacción.
- **No se imputan valores:** ausentes se reportan como opacidad; nunca se rellenan con ceros, medias ni valores plausibles.
- **Duplicado conocido:** 1 par entre fuentes; se conserva para no alterar el universo acordado.

---

## 9. Conclusiones

1. El mercado inmobiliario digital de Diez de Octubre está fuertemente dolarizado (86,9 % del universo en USD), lo que crea una barrera de acceso estructural para quien solo tiene CUP.
2. El precio mediano de compra ($20.000 USD) es muy inferior a la media ($26.023,26 USD), lo que indica que la media sobreestima el precio típico debido a valores extremos.
3. No es posible estimar el precio de alquiler con esta base; esa ausencia es un hallazgo sobre el funcionamiento del segmento.
4. Existe desigualdad territorial: La Víbora lidera la media entre zonas con n ≥ 10, mientras que El Sevillano lidera la mediana; los valores extremos inflan el promedio en La Víbora.
5. La opacidad es importante: 25,4 % sin zona, 12,3 % sin precio, 4,9 % sin ambos. La ausencia de información es un mecanismo de desigualdad.
6. La base verificada de 122 publicaciones es más rigurosa que la base histórica de 134 anuncios etiquetados (no verificados); no son comparables.
7. Los 55 descartes se conservan íntegros, lo que permite auditoría y reproducción completa del proceso de exclusión.

---

## 10. Referencias

- **ONEI.** *Anuario Estadístico de Cuba*. Oficina Nacional de Estadística e Información, República de Cuba. `fuentes/anuario_estadistico_notas.md`.
- **OpenStreetMap / Nominatim.** Geocodificación de topónimos; caché local en `datos/geo/geocoding_lha.json`.
- **GeoJSON municipal.** `datos/geo/lha.geojson`; SHA-256 `b9bbcce811d9bbfcee15f5e904d97dc24cf044cabcf17a870487ad361bb7c9e6`.
- **Revolico.** `https://www.revolico.com`. Captura 2026-10-31.
- **Facebook.** `https://www.facebook.com` (grupos y páginas de compraventa). Captura 2026-11-04. No se reproducen enlaces individuales por privacidad.

---

## 11. Archivos del repositorio

| Ruta | Contenido |
|---|---|
| `analisis/informe_final.md` | Informe A-F con las 30 preguntas |
| `analisis/informe_final.pdf` | Entrega académica en PDF (16 páginas) |
| `analisis/verificacion_municipal_geojson_20261104.md` | Reporte de verificación municipal |
| `datos/limpios/unificado_confirmados_diez_octubre.json` | Base final de 122 confirmados |
| `datos/limpios/descartados_diez_octubre.json` / `.csv` | 55 descartes íntegros con motivo |
| `scripts/cifras_control.py` | 36 cifras de control (solo lectura) |
| `tests/test_verificacion.py` | 8 pruebas de contrato |
| `scripts/run_all.sh` | Pipeline en un comando |
| `.github/workflows/ci.yml` | Integración continua |
| `AGENTS.md` | Invariantes del pipeline |
| `data_dictionary.md` | Diccionario de datos |
| `bitacora_cambios.md` | Historia del cambio 134 → 122 |
| `fuentes/recursos_utilizados.md` | Enlaces web de fuentes primarias |
| `README.md` | Documentación principal del proyecto |

---

> **Nota sobre la evidencia:** los precios son precios de oferta, no de transacción. No hay datos homogéneos de metros cuadrados, habitaciones, baños, estado legal ni año de construcción. Las ausencias se reportan; no se imputan. Cualquier cifra citada de este reporte puede ser verificada ejecutando `scripts/cifras_control.py` y `tests/test_verificacion.py`.

## 16. Herramientas utilizadas

Este proyecto fue desarrollado utilizando el siguiente conjunto de herramientas:

### Entorno de desarrollo
- **Python 3.x** — Lenguaje de programación principal.
- **Archlinux** — Sistema operativo utilizado para todo el desarrollo.
- **Vim y Visual Studio Code** — Editores de código utilizados para escribir y editar los scripts y la documentación.

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
- **whisper.cpp (modelo base)** — Transcripción automática de las 37 grabaciones de audio de entrevistas (`evidencias/entrevistas_audio/`). Las transcripciones no se incluyen en el repositorio para proteger la privacidad de los entrevistados.
- **Samsung Galaxy A56** — Dispositivo móvil utilizado para grabar las entrevistas de audio.
- **Capturas de pantalla** — 86 capturas de publicaciones de Facebook (`evidencias/facebook_fotos/`), utilizadas como evidencia visual de anuncios publicados.

### Herramientas de análisis estadístico
- **Python `statistics`** — Cálculo de mediana, percentiles P10 y P90.
- **`collections.Counter`** — Conteo de frecuencias por fuente, zona, tipo de inmueble, operación y moneda.
- **JSON** — Formato de almacenamiento de bases de datos limpias y descartes.

### Bases de datos
No se utilizó ningún sistema de gestión de bases de datos relacional o NoSQL. Todos los datos se almacenan en archivos JSON y CSV planos.

