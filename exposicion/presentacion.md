# Mercado Inmobiliario Digital en Diez de Octubre, La Habana
## Análisis de opacidad, dolarización y desigualdad territorial a partir de anuncios publicados

**Proyecto de Ciencia de Datos — Universidad de La Habana**  
**Facultad de Matemática y Computación (MATCOM)**  
**Profesor:** Yudivian Almeida Cruz  
**Fecha:** Noviembre de 2026  
**Universo:** 122 publicaciones confirmadas (83 de Revolico + 39 de Facebook)

---

## 1. Problema de investigación

**Pregunta central:** ¿Cómo se configura el mercado inmobiliario digital de Diez de Octubre y qué implica la opacidad de la información para el acceso a la vivienda en el municipio?

**Subpreguntas:**  
¿En qué moneda se publican las ofertas? ¿Cómo se distribuyen los precios entre zonas? ¿Qué información falta en los anuncios y qué prácticas informales aparecen? ¿Qué tan confiable es la ubicación declarada en los anuncios digitales?

**Objetivo:** Caracterizar la oferta inmobiliaria publicada en plataformas digitales enfocada al municipio Diez de Octubre, midiendo precios, tipos de inmueble, zonas, moneda declarada y opacidad de la información, sin imputar valores ausentes.

---

## 2. Delimitación y alcance del estudio

**Ámbito geográfico:** Municipio Diez de Octubre, La Habana. No se incorporan otros municipios ni provincias.  
**Ámbito temporal:** Corte de Revolico (2026-10-31) y captura de Facebook (2026-11-04). No hay serie temporal.  
**Tipo de datos:** Precios de oferta (no de transacción). No se imputan valores ausentes.  
**Justificación temática:** Diez de Octubre combina alta densidad habitacional, barrios con identidad propia y presencia importante de anuncios digitales, lo que lo hace un caso relevante para estudiar desigualdad territorial en el mercado inmobiliario digital.

---

## 3. Fuentes de datos y obtención

| Fuente | Tipo | Cantidad confirmada | Corte |
|---|---|---|---|
| Revolico | Portal de anuncios clasificados | 83 publicaciones | 2026-10-31 |
| Facebook | Grupos y páginas de compraventa | 39 publicaciones | 2026-11-04 |
| **Total** | | **122 publicaciones** | |

**Limitación de fuentes:** No se incorporan otras plataformas (Cubisima, HogarEnCuba) ni entrevistas formales. Las 13 entrevistas de audio y 86 capturas de Facebook se conservan como evidencia cualitativa complementaria en `evidencias/`, no como muestra estadística.

---

## 4. Metodología de verificación municipal

**Problema detectado:** El campo `municipio` del scraper de Revolico no es fiable: asigna «Diez de Octubre» a anuncios que en su ficha declaran otro municipio.

**Regla aplicada — Título como evidencia principal:**

1. Si el **título** nombra Diez de Octubre o un reparto interno (Santos Suárez, Lawton, La Víbora, Luyanó, El Sevillano, etc.), se confirma.
2. Si el **título** nombra un lugar externo (Otro municipio, provincia o localidad), se descarta aunque la ficha declare Diez de Octubre.
3. Solo cuando el título no aporta señal se recurre a la ficha, el enlace, el grupo, la ubicación o la zona.
4. Los topónimos se geocodificaron con Nominatim y se comprobó punto-en-polígono contra `datos/geo/lha.geojson` (DPA 23.09, 11 vértices).

**Resultado de verificación:**

| Resultado | Revolico (n=134) | Facebook (n=42) | Unificado (n=176) |
|---|---:|---:|---:|
| SÍ, dentro de Diez de Octubre | 83 | 39 | **122** |
| NO, otro municipio | 46 | 0 | 46 |
| CONTRADICTORIO | 0 | 0 | 0 |
| INDETERMINADO | 5 | 3 | 8 |

**No se elimina información:** Los 55 registros descartados se conservan íntegros en `datos/limpios/descartados_diez_octubre.json` y `.csv`, con motivo, evidencia y registro unificado exacto.

---

## 5. Universo de análisis: 122 publicaciones confirmadas

| Indicador | Valor | Lectura |
|---|---|---|
| Publicaciones confirmadas | 122 | Universo canónico del informe |
| Revolico / Facebook | 83 / 39 | Integración de fuentes heterogéneas |
| Precios en USD | 106 (86.9%) | Dolarización predominante |
| Precio en CUP | 1 (0.8%) | No convertido a USD |
| Sin precio | 15 (12.3%) | Reportado como opacidad |
| Zona identificada | 91 (74.6%) | 84 en ficha + 7 recuperadas del texto |
| Sin zona | 31 (25.4%) | Reportado como opacidad |
| Precio y zona | 82 (67.2%) | Permite cruce de ambos datos |
| Sin precio ni zona | 6 (4.9%) | Opacidad total |
| Duplicado entre fuentes | 1 par | `facebook-35` / `revolico-58326838`; n efectivo 121 |

---

## 6. Precios de compra (ventas en USD, n = 43)

| Estadístico | Valor |
|---|---|
| Mediana | $20.000,00 USD |
| Media | $26.023,26 USD |
| P10 | $6.200,00 USD |
| P90 | $60.000,00 USD |
| Mínimo | $2.500,00 USD |
| Máximo | $180.000,00 USD |

**Interpretación académica:** La media supera a la mediana en $6.023,26 USD, lo que indica que la distribución está sesgada hacia la derecha por valores extremos (máximo $180.000). La mediana ($20.000) representa mejor el precio típico de compra que la media. El 80% central de las ofertas se ubica entre $6.200 y $60.000 USD.

---

## 7. Dolarización del mercado

| Métrica | Valor |
|---|---|
| Anuncios con moneda declarada en USD | 106 de 107 (99,1%) |
| USD sobre el total del universo | 106 de 122 (86,9%) |
| Precio en CUP | 1 anuncio (0,8%), no convertido a USD |
| Sin precio declarado | 15 publicaciones (12,3%) |

**Interpretación académica:** El mercado digital de Diez de Octubre funciona predominantemente en divisas. Quien solo dispone de CUP enfrenta una barrera de acceso estructural: solo 1 de 122 anuncios declara precio en CUP, y ese anuncio corresponde a un alquiler. La dolarización no es solo un fenómeno monetario; es un mecanismo de selección del acceso a la vivienda publicada.

---

## 8. Desigualdad territorial entre zonas

**Cuatro zonas principales concentran 69 de 91 publicaciones con zona (75,8%):**

| Zona | Publicaciones | Media (USD) | Mediana (USD) |
|---|---:|---:|---:|
| Santos Suárez | 26 | $31.565,22 | $22.500,00 |
| Lawton | 19 | $20.656,25 | $20.000,00 |
| La Víbora | 12 | $49.590,91 | $26.000,00 |
| El Sevillano | 12 | $39.700,00 | $36.000,00 |

**Interpretación académica:**  
- La Víbora tiene la **media más alta** (n = 11) pero su mediana es inferior a la de El Sevillano. La diferencia se explica por valores extremos (máximo $180.000), que inflan el promedio pero no afectan la mediana.  
- El Sevillano tiene la **mediana más alta** entre zonas con n ≥ 10 ($36.000), lo que sugiere que su precio típico es superior al de La Víbora a pesar de una media menor.  
- **Conclusión metodológica:** Para comparar barrios con subgrupos pequeños y valores extremos, la mediana es un estimador más robusto que la media.

---

## 9. Opacidad de la información

| Indicador | Valor | % |
|---|---|---|
| Publicaciones sin precio | 15 de 122 | 12,3% |
| Publicaciones sin zona | 31 de 122 | 25,4% |
| Publicaciones con precio y zona | 82 de 122 | 67,2% |
| Publicaciones sin precio ni zona | 6 de 122 | 4,9% |

**Interpretación académica:** La ausencia de datos no se trata como un defecto técnico, sino como un rasgo del mercado. Quien no puede verificar precio o zona queda expuesto a la intermediación informal. La opacidad mide quién tiene acceso a información verificable y quién depende de intermediarios.

---

## 10. Prácticas informales y tipos de inmueble

| Indicador | Valor |
|---|---|
| Lenguaje informal (oportunidad, permuta, cambio) | 12 publicaciones (9,8%) |
| Todas las informales provienen de Revolico | Cota inferior (Facebook no aporta texto suficiente) |
| Apartamento — media / mediana | $18.181,82 / $15.000,00 USD (n = 33) |
| Casa — media / mediana | $42.842,11 / $33.000,00 USD (n = 57) |

**Interpretación académica:** La informalidad se concentra en venta y en publicaciones sin operación declarada. No aparece en alquiler. El tipo de inmueble más publicado es la casa (63 anuncios), pero el apartamento es el más accesible en precio.

---

## 11. Control de calidad y reproducibilidad

| Componente | Implementación | Resultado |
|---|---|---|
| Cifras de control | `scripts/cifras_control.py` | 36/36 verificadas |
| Pruebas de contrato | `tests/test_verificacion.py` | 8/8 pasando |
| Integración continua | `.github/workflows/ci.yml` | Ejecuta pruebas y cifras en cada push |
| Versiones fijadas | `requirements.txt` | `==` para reproducibilidad |
| Pipeline maestro | `scripts/run_all.sh` | 4 pasos en un comando |
| Diccionario de datos | `data_dictionary.md` | Convenciones de nulos, cobertura por campo |
| Bitácora de cambios | `bitacora_cambios.md` | Historia 134 → 122 |

**Proceso de reproducción:**  
`git clone` → `pip install -r requirements.txt` → `bash scripts/run_all.sh` → verificar que `cifras_control.py` imprime 36 OK y que las 8 pruebas de contrato pasan.

---

## 12. Limitaciones y sesgos

| Limitación | Implicación |
|---|---|
| Muestra no probabilística | 122 publicaciones no representan necesariamente el universo de viviendas del municipio |
| Precios de oferta | Valores publicados, no precios de transacción |
| Sin serie temporal | Corte único de Revolico (2026-10-31); Facebook sin fechas homogéneas |
| Campos ausentes | 0/122 para habitaciones y baños; 0/122 para superficie homogénea; no se puede calcular precio por m² |
| Alquiler no estimable | 3 publicaciones, 1 con precio en CUP, ninguno en USD |
| Sesgo de publicación | Viviendas no publicadas o en canales cerrados no aparecen |
| No imputación | Ausencias reportadas como opacidad; no se rellenan con medias ni ceros |

---

## 13. Conclusiones

1. **Mercado altamente dolarizado:** 86,9% del universo declara USD. El único precio en CUP corresponde a un alquiler. Quien solo tiene CUP enfrenta barrera de acceso estructural.
2. **Precios típicos inferiores al promedio:** La mediana de compra ($20.000) es muy inferior a la media ($26.023), lo que demuestra que los valores extremos distorsionan el promedio. Para comparar barrios, la mediana es más robusta.
3. **Alquiler no estimable:** Solo 3 publicaciones de alquiler, ninguna en USD. No es posible comparar compra y alquiler con esta base.
4. **Desigualdad territorial real:** Las cuatro zonas principales concentran el 75,8% de la oferta con zona identificada. La Víbora lidera la media por valores extremos; El Sevillano lidera la mediana entre zonas con n ≥ 10.
5. **Opacidad como mecanismo de desigualdad:** El 4,9% de los anuncios no tiene precio ni zona; el 25,4% no especifica zona. La ausencia de información no es un defecto menor: es parte del funcionamiento del mercado.
6. **Base verificada vs. base etiquetada:** El universo de 122 publicaciones verificadas es más riguroso que la base histórica de 134 anuncios etiquetados (no verificados). No son comparables.

---

## 14. Trabajo futuro y líneas de extensión

- Incorporar fuentes adicionales (Cubisima, HogarEnCuba) manteniendo la regla de verificación título-primero.
- Realizar clustering de características textuales (garaje, patio, azotea, terraza) para segmentar la oferta por atributos no capturados en el tipo de inmueble.
- Explorar series temporales con capturas periódicas para observar variaciones de precios y opacidad en el tiempo.
- Ampliar la cobertura de habitaciones, baños y superficie mediante extracción de texto libre en anuncios de Revolico.
- Triangular con entrevistas cualitativas (13 grabaciones disponibles en `evidencias/entrevistas_audio/`) para validar hallazgos de opacidad y dolarización desde la perspectiva de los actores del mercado.

---

## 15. Guion para el presentador (aproximadamente 10 minutos)

**Diapositiva 1 (1 min):** Presentar el título, el contexto universitario y la pregunta central. Subrayar que no es solo "cuánto cuesta", sino cómo funciona el mercado digital y qué información falta.

**Diapositiva 2 (1 min):** Explicar por qué Diez de Octubre y por qué el corte temporal es único.

**Diapositiva 3 (1,5 min):** Mostrar las fuentes. Hacer hincapié en que son solo dos plataformas y que Facebook tiene información limitada.

**Diapositiva 4 (2 min):** Esta es la diapositiva más importante metodológicamente. Explicar el problema del campo `municipio` no fiable y por qué se usó el título como evidencia principal. Mostrar la tabla de verificación y los 55 descartes conservados. Un profesor valorará que no se borró información.

**Diapositiva 5 (1 min):** Mostrar la tabla de cobertura. Señalar que el 12,3% no declara precio y el 25,4% no especifica zona.

**Diapositiva 6 (1,5 min):** Presentar mediana y media. Hacer hincapié en que la mediana es el estimador más robusto dado el sesgo por valores extremos.

**Diapositiva 7 (1,5 min):** Mostrar la dolarización. Conectar con la barrera de acceso para quien solo tiene CUP.

**Diapositiva 8 (2 min):** Comparar La Víbora (media alta, mediana menor) con El Sevillano (mediana más alta). Explicar por qué los valores extremos inflan la media pero no la mediana.

**Diapositiva 9 (1,5 min):** Presentar la opacidad como hallazgo, no como error. Mencionar que quien no puede verificar queda expuesto a intermediación.

**Diapositiva 10 (1 min):** Informalidad y tipos de inmueble. Mencionar que la informalidad es una cota inferior porque solo se mide en Revolico.

**Diapositiva 11 (1,5 min):** Mostrar el pipeline de reproducibilidad. Un profesor académico valorará que alguien más pueda reproducir los resultados ejecutando `run_all.sh` y verificando con `cifras_control.py` y las pruebas.

**Diapositiva 12 (1 min):** Listar limitaciones sin ocultarlas. Esto demuestra honestidad intelectual.

**Diapositiva 13 (1,5 min):** Conclusiones. Sintetizar los 6 hallazgos principales.

**Diapositiva 14 (0,5 min):** Trabajo futuro y agradecimiento.

---

**Nota para el presentador:** Durante la exposición, si el profesor pregunta por las entrevistas, responda que se usaron como evidencia cualitativa suelta (13 grabaciones anónimas en `evidencias/entrevistas_audio/`) y que no se calcularon porcentajes ni se hicieron mapeos por zonas porque no constituyen una muestra representativa del municipio.
