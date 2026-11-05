# Mercado inmobiliario digital en Diez de Octubre
## Opacidad, dolarización, desigualdad territorial e informalidad

**Fecha de generación:** 05/11/2026 01:00
**Corte de los datos:** 2026-10-31 (Revolico); Facebook sin fecha homogénea
**Universo:** 122 publicaciones confirmadas dentro del municipio (83 de Revolico + 39 de Facebook)
**Verificación espacial:** polígono municipal DPA `23.09` de `datos/geo/lha.geojson`
**Base de datos:** `datos/limpios/unificado_confirmados_diez_octubre.json`

## Resumen ejecutivo

Esta versión no usa los 134 anuncios que el scraper *etiquetaba* como Diez de Octubre. Usa las **122 publicaciones que la verificación espacial confirmó dentro del municipio**: 83 de Revolico y 39 de Facebook. De las 176 publicaciones unificadas, 46 pertenecen a otro municipio y 8 no son verificables; todas quedan fuera. La clasificación aplica el **título como evidencia principal**: si nombra Diez de Octubre o un reparto interno, confirma; si nombra un lugar externo, descarta. La ficha y el resto del texto solo se usan cuando el título no aporta señal. El detalle está en `analisis/verificacion_municipal_geojson_20261104.md`.
Los **55 registros no incluidos** (46 `NO`, 8 `INDETERMINADO` y 1 fuera del universo) se conservan íntegros en `datos/limpios/descartados_diez_octubre.json` y `.csv`, con su motivo, su registro original y el registro unificado exacto.

Los hallazgos principales son:

- **Dolarización:** 106 de 107 publicaciones con moneda declarada están en USD (**99.1%**), y 106 de 122 del total (**86.9%**). El único precio declarado en CUP es un alquiler.
- **Precios de compra:** mediana **$20,000.00 USD**; P10–P90 **$6,200.00–$60,000.00 USD**; media **$26,023.26 USD** (n = 43 ventas explícitas con precio en USD).
- **Alquiler:** 1 de 3 alquileres declaran precio y **ninguno lo hace en USD**; el precio de alquiler no es estimable con esta base.
- **Opacidad:** 15 de 122 publicaciones (12.3%) no declaran precio; 31 (25.4%) no especifican zona; solo 82 (67.2%) permiten cruzar precio y zona.
- **Desigualdad territorial:** las cuatro zonas principales concentran 69 de 91 publicaciones con zona identificada (75.8%). Entre las zonas con n ≥ 10, La Víbora tiene la media más alta ($49,590.91 USD, n = 11) y El Sevillano la mediana más alta ($36,000.00 USD, n = 10); entre las de n ≥ 5, El Mónaco lidera la media ($57,666.67 USD, n = 6), pero la mediana más alta sigue siendo la de El Sevillano ($36,000.00 USD, n = 10).
- **Informalidad:** 12 de 122 publicaciones (9.8%) usan lenguaje de oportunidad, permuta o cambio. Todas son de Revolico: Facebook no aporta texto suficiente para medir esta dimensión, así que el dato es una cota inferior.
- **Tipo de inmueble:** el apartamento es la opción más accesible: media **$18,181.82 USD** y mediana **$15,000.00 USD** (n = 33), frente a la casa con media **$42,842.11 USD** y mediana **$33,000.00 USD** (n = 57).

La ausencia de datos no se trata como un simple defecto: se mide y se reporta como un rasgo del mercado. Una publicación sin precio, sin zona o sin operación limita la capacidad de comparar y de verificar, y esa limitación es parte del problema social que el estudio documenta.

## Introducción: por qué este mercado es un problema social

El acceso a la vivienda en La Habana no depende solo de la oferta y la demanda. En un mercado digital con precios en divisas, ubicaciones incompletas y publicaciones que no declaran si se vende o se alquila, la información se convierte en un recurso desigual. Quien tiene acceso a divisas, a contactos y a tiempo para verificar puede comparar; quien no lo tiene queda expuesto a la opacidad y a la intermediación informal.

Este informe estudia cuatro dimensiones de ese problema:

1. **Precios:** ¿cuánto cuesta comprar y cuánto alquilar, y con qué dispersión? La media sola engaña; por eso se reportan mediana y P10–P90.
2. **Territorio:** ¿la oferta y los precios se distribuyen de forma desigual entre los barrios del mismo municipio?
3. **Dolarización:** ¿en qué medida el mercado funciona en USD y qué implica para quien solo tiene CUP?
4. **Opacidad e informalidad:** ¿cuánta información falta y qué prácticas (lenguaje de oportunidad, permuta, publicaciones sin operación) aparecen en los anuncios?

Diez de Octubre es un caso relevante porque combina alta densidad de vivienda, barrios con identidad propia (Santos Suárez, Lawton, La Víbora, Luyano, El Sevillano) y una presencia importante de anuncios digitales. La comparación entre barrios permite observar si el mercado reproduce o atenúa las desigualdades territoriales.

## Metodología y verificación municipal

### Por qué el universo es 122 y no 134

El campo `municipio` del scraper no es fiable: asigna «Diez de Octubre» a anuncios que en su ficha declaran otro municipio. Para corregirlo se usó el **título como evidencia principal**. Si el título nombra Diez de Octubre o un reparto interno, la publicación se confirma; si nombra un municipio, reparto o localidad externa, se descarta. Solo cuando el título no aporta señal se recurre a la ficha de Revolico y al resto del texto (enlace, grupo, ubicación o zona). Los topónimos se geocodificaron con Nominatim y se comprobaron punto-en-polígono contra `datos/geo/lha.geojson`.

| Resultado | Revolico (n=134) | Facebook (n=42) | Unificado (n=176) |
|---|---:|---:|---:|
| SÍ, dentro de Diez de Octubre | 83 | 39 | 122 |
| NO, otro municipio | 46 | 0 | 46 |
| CONTRADICTORIO | 0 | 0 | 0 |
| INDETERMINADO | 5 | 3 | 8 |

La base final son las **122 publicaciones con resultado SÍ**. Las 46 de otro municipio y las 8 indeterminadas se excluyen. Los 8 casos que la regla anterior marcaba como contradictorios tenían un título con un reparto interno y se confirman por la regla de título. Esa exclusión reduce el tamaño de la muestra, pero evita atribuir a Diez de Octubre precios y zonas que pertenecen a otros municipios.
Los **55 registros no incluidos** se conservan íntegros: 46 `NO`, 8 `INDETERMINADO` y 1 que ya estaba fuera de la base unificada (`facebook-27`). Cada uno guarda su motivo, la evidencia, el registro original y el registro unificado exacto en `datos/limpios/descartados_diez_octubre.json` y `.csv`.

La verificación tiene un límite explícito: el polígono es una simplificación de 11 vértices y no resuelve casos catastrales a pocos metros del borde. Además, la ficha se apoya en la ubicación que declara el anunciante, no en la dirección exacta de la propiedad. La regla de título puede confirmar un anuncio con ficha mal declarada, y los casos indeterminados son aquellos en los que ninguna evidencia alcanza para decidir.

### Fuentes y normalización

- **Revolico:** 83 publicaciones confirmadas. Aportan título, enlace, fecha de verificación y, en la mayoría de los casos, precio anidado en `precio.monto`.
- **Facebook:** 39 publicaciones confirmadas. Aportan precio y descripción, pero muchas no tienen título ni texto crudo homogéneo. Por eso la operación queda «sin clasificar» con más frecuencia y la medición de lenguaje informal solo es posible en Revolico.
- **Precio:** se usa `precio.monto` y, cuando falta, `precio.monto_actual` (un caso de Facebook con rebaja: 15,000 USD). Los precios en CUP no se convierten a USD porque no hay un tipo de cambio único y defendible para el corte.
- **Zona:** se usa el campo normalizado `detalles_propiedad.zona`. Si viene vacío o «No especificado», se busca el nombre del barrio o reparto en el texto declarado. No se infiere una zona que el anuncio no mencione.
- **Tipo y operación:** se usan los campos normalizados `detalles_propiedad.tipo` y `operacion`. No se reclasifica la operación por el precio ni por el título: si el anuncio no la declara, queda «sin clasificar». Es una regla conservadora y reproducible.
- **Subgrupos pequeños:** los grupos con n < 10 se presentan como evidencia descriptiva, no como conclusión firme. Las zonas con n < 5 no se usan para comparar promedios.
- **Ausencia:** una publicación sin precio, sin zona o sin operación no se elimina del universo. Se conserva y se contabiliza como indicador de opacidad, porque su ausencia también describe el mercado.

### Trazabilidad del cambio respecto al informe anterior

El informe anterior respondía 30 preguntas sobre 134 anuncios de Revolico etiquetados como Diez de Octubre. La verificación muestra que 83 de esos 134 están confirmados en el municipio: 73 con ficha que declara Diez de Octubre y 10 por mención interna en el título. Esta versión recalcula el informe con las 122 publicaciones confirmadas e incorpora 39 de Facebook. No es una actualización de cifras: es un cambio de universo. Las cifras anteriores no deben compararse directamente con las de este informe.

Las 30 preguntas A1–F5 se conservan. Cinco preguntas originales del cuestionario base siguen sin ser estimables con estos datos (mediana del alquiler, comparación compra–alquiler, precio por metro cuadrado, zonas por operación y precio promedio en CUP); en su lugar se mantienen preguntas que miden la ausencia de información.

## Las 30 preguntas y sus respuestas

Cada pregunta indica su nivel de evidencia: ✅ sólida (n ≥ 30 o censo completo del subgrupo), 🟡 descriptiva (n = 5–29) y 🔴 no estimable (la ausencia es el hallazgo).

### Bloque A: Precios de referencia

**A1. ¿Cuál es el precio promedio de compra en USD?** ✅ (n = 43)

> **$26,023.26 USD** entre las 43 ventas explícitas con precio en USD. Si se incluyen todas las publicaciones con precio USD (ventas y publicaciones sin operación declarada; no hay alquileres en USD), la media sube a **$36,000.00 USD** (n = 106), porque las publicaciones sin operación declarada incluyen inmuebles de mayor precio. La media de compra es una referencia, no el precio típico: la mediana es bastante menor (A2).

**A2. ¿Cuál es la mediana y el rango P10–P90 del precio de compra en USD?** ✅ (n = 43)

> Mediana **$20,000.00 USD**. El 80% central de las ventas está entre **$6,200.00 USD** (P10) y **$60,000.00 USD** (P90). El mínimo es **$2,500.00 USD** y el máximo **$70,000.00 USD**. La mediana es menor que la media ($26,023.26), señal de una distribución sesgada a la derecha: unas pocas publicaciones muy caras elevan el promedio.

**A3. ¿Cuál es el precio promedio o mediano del alquiler?** 🔴 (no estimable)

> **No estimable.** Hay 3 publicaciones de alquiler: 1 declara precio (uno solo, en CUP: 50,000 CUP) y 2 no lo declaran (66.7%). Ningún alquiler tiene precio en USD. No se puede calcular una media ni una mediana en USD, y el único precio en CUP no es comparable sin un tipo de cambio explícito. La ausencia de precio de alquiler es el hallazgo, no una limitación menor.

**A4. ¿Qué proporción de alquileres declara precio y en qué moneda?** ✅ (censo de 3 alquileres)

> **1 de 3 (33.3%)** declaran precio. Ese único anuncio está en **CUP** (50,000 CUP); **0 de 3** lo declaran en USD. Los otros 2 alquileres no permiten conocer ni siquiera el orden de magnitud del precio. Con solo 3 casos, la proporción es un censo del subgrupo, no una estimación del mercado.

**A5. ¿La compra declara precio más que el alquiler?** ✅ (censo de ventas y alquileres)

> Sí. **43 de 50 ventas (86.0%)** declaran precio, frente a **1 de 3 alquileres (33.3%)**. La brecha es de **52.7 puntos porcentuales**. El mercado de compra es mucho más transparente en precio que el de alquiler, que funciona casi por contacto directo. La conclusión es descriptiva: el alquiler tiene solo 3 casos.

### Bloque B: Desigualdades territoriales

**B1. ¿Qué zonas concentran la mayor oferta?** ✅ (91 publicaciones con zona identificada)

> - Santos Suárez: **26 anuncios** (28.6% de las publicaciones con zona)
> - Lawton: **19 anuncios** (20.9% de las publicaciones con zona)
> - La Víbora: **12 anuncios** (13.2% de las publicaciones con zona)
> - El Sevillano: **12 anuncios** (13.2% de las publicaciones con zona)
> - Luyano: **7 anuncios** (7.7% de las publicaciones con zona)
> - El Mónaco: **6 anuncios** (6.6% de las publicaciones con zona)
> - Santa Catalina: **5 anuncios** (5.5% de las publicaciones con zona)
> - Calzada 10 de Octubre: **2 anuncios** (2.2% de las publicaciones con zona)
> - Vía Blanca: **1 anuncio** (1.1% de las publicaciones con zona)
> - Vista Alegre: **1 anuncio** (1.1% de las publicaciones con zona)
>
> **91 de 122 publicaciones (74.6%)** especifican zona; **31 (25.4%)** no lo hacen. Las cuatro zonas principales —Santos Suárez, Lawton, La Víbora, El Sevillano— reúnen **69 de 91 (75.8%)** de la oferta con zona identificada: la información territorial está concentrada en pocos barrios.

**B2. ¿Qué zona tiene el precio promedio más alto?** 🟡 (n = 6 en El Mónaco)

> **El Mónaco**, con una media de **$57,666.67 USD** (n = 6). Es un resultado descriptivo: el grupo tiene menos de 10 publicaciones y su media puede estar influida por valores extremos. Si se exige n ≥ 10, la zona con media más alta es **La Víbora** ($49,590.91 USD, n = 11).

> Orden por media entre las zonas con n ≥ 5:
>
> - El Mónaco: media **$57,666.67 USD**, mediana **$33,000.00 USD** (n = 6)
> - La Víbora: media **$49,590.91 USD**, mediana **$26,000.00 USD** (n = 11)
> - El Sevillano: media **$39,700.00 USD**, mediana **$36,000.00 USD** (n = 10)
> - Santa Catalina: media **$37,200.00 USD**, mediana **$35,000.00 USD** (n = 5)
> - Santos Suárez: media **$31,565.22 USD**, mediana **$22,500.00 USD** (n = 23)
> - Luyano: media **$25,928.57 USD**, mediana **$25,000.00 USD** (n = 7)
> - Lawton: media **$20,656.25 USD**, mediana **$20,000.00 USD** (n = 16)

**B3. ¿Qué zona tiene la mediana más alta?** 🟡 (n = 10 en El Sevillano)

> **El Sevillano**, con una mediana de **$36,000.00 USD** (n = 10). Si se exige n ≥ 10, la mediana más alta corresponde a **El Sevillano** ($36,000.00 USD, n = 10).

> Orden por mediana entre las zonas con n ≥ 5:
>
> - El Sevillano: mediana **$36,000.00 USD** (n = 10)
> - Santa Catalina: mediana **$35,000.00 USD** (n = 5)
> - El Mónaco: mediana **$33,000.00 USD** (n = 6)
> - La Víbora: mediana **$26,000.00 USD** (n = 11)
> - Luyano: mediana **$25,000.00 USD** (n = 7)
> - Santos Suárez: mediana **$22,500.00 USD** (n = 23)
> - Lawton: mediana **$20,000.00 USD** (n = 16)

**B4. ¿La brecha La Víbora–Lawton se mantiene al usar medianas?** 🟡 (n = 11 y 16)

> **No se mantiene con la misma magnitud.** Por media, La Víbora ($49,590.91 USD) supera a Lawton ($20,656.25 USD) en **$28,934.66 USD**. Por mediana, la diferencia es de solo **$6,000.00 USD** ($26,000.00 frente a $20,000.00). La brecha por media es **4.8 veces** la brecha por mediana. El máximo de La Víbora ($180,000.00 USD) y su P90 ($100,000.00 USD) explican buena parte de la diferencia: la media describe el extremo alto, no el precio típico. Para comparar barrios conviene usar la mediana.

**B5. ¿La falta de zona afecta igual a compra y alquiler?** ✅ (censo de operaciones)

> No. La falta de zona es más frecuente en alquiler: **2 de 3 (66.7%)** alquileres no especifican zona, frente a **17 de 50 (34.0%)** ventas y **12 de 69 (17.4%)** publicaciones sin operación declarada. El alquiler combina las dos opacidades: casi nunca declara precio y casi nunca declara zona. Con solo 3 alquileres, la evidencia es descriptiva.

### Bloque C: Dolarización

**C1. ¿Qué porcentaje de publicaciones con moneda declarada está en USD?** ✅ (n = 107)

> **106 de 107 (99.1%)**. El único anuncio con moneda declarada que no está en USD es un alquiler en CUP (50,000 CUP). Las 15 publicaciones sin precio no declaran moneda y quedan fuera de este denominador.

**C2. ¿Qué porcentaje del total está en USD?** ✅ (n = 122)

> **106 de 122 (86.9%)**. El resto se reparte entre 15 publicaciones sin precio (12.3%) y 1 anuncio en CUP (0.8%). La dolarización es alta incluso cuando se cuenta a las publicaciones que no declaran precio.

**C3. ¿La dolarización varía por tipo de inmueble?** ✅ (publicaciones con precio)

> - Casa: **57 de 57 (100.0%)** en USD
> - Apartamento: **33 de 33 (100.0%)** en USD
> - Inmueble: **14 de 15 (93.3%)** en USD
> - Cuarto: **2 de 2 (100.0%)** en USD
>
> La dolarización es prácticamente total en todos los tipos con precio. El único anuncio en CUP es un alquiler clasificado como «Inmueble». No hay un tipo de inmueble que funcione principalmente en CUP.

**C4. ¿La dolarización varía por zona?** ✅ (82 publicaciones USD con zona)

> **No se puede medir variación territorial:** las **82 publicaciones** con precio USD y zona identificada están **todas en USD (100%)**. El único anuncio en CUP no especifica zona. La conclusión no es que todas las zonas estén dolarizadas por igual, sino que la base no permite compararlas: la ausencia de zona en el anuncio en CUP impide saber si hay barrios con precios en CUP.

**C5. ¿Cuánto podría variar la dolarización si las publicaciones sin precio fueran CUP o USD?** ✅ (cota inferior y superior)

> La proporción de USD en el total está acotada entre **86.9%** y **99.2%**. El límite inferior supone que las 15 publicaciones sin precio están en CUP; el superior, que están en USD. La diferencia entre ambos escenarios es de **12.3 puntos porcentuales**. La ausencia de precio y moneda impide conocer el valor exacto, pero permite afirmar que, en cualquier escenario, más de cuatro quintas partes del mercado está en USD o podría estarlo. Esa cota es un resultado, no una especulación.

### Bloque D: Opacidad de la información

**D1. ¿Qué porcentaje no declara precio?** ✅ (n = 122)

> **15 de 122 (12.3%)**. Son publicaciones que no permiten comparar precios sin contactar al vendedor. La ausencia es especialmente alta en alquiler (A4).

**D2. ¿Qué porcentaje no especifica zona?** ✅ (n = 122)

> **31 de 122 (25.4%)**. Sin zona no se puede verificar la ubicación ni comparar barrios. La cifra es menor que la del informe anterior porque esta base trae un campo de zona normalizado y se completó con el texto declarado; no porque el mercado se haya vuelto más transparente.

**D3. ¿Cuántas publicaciones carecen de precio y zona a la vez?** ✅ (n = 122)

> **6 de 122 (4.9%)**. En estas publicaciones no se puede saber ni cuánto cuesta ni dónde está. Son el núcleo más opaco del mercado digital.

**D4. ¿Qué porcentaje tiene información mínima completa (precio + zona)?** ✅ (n = 122)

> **82 de 122 (67.2%)**. Dos tercios de las publicaciones permiten cruzar precio y zona. Ese es el subconjunto sobre el que se pueden hacer comparaciones territoriales relativamente sólidas; el resto queda fuera por falta de un dato básico.

**D5. ¿La opacidad es mayor en alquiler que en venta?** ✅ (censo de operaciones)

> Sí, sobre todo en precio. En **alquiler**, **2 de 3 (66.7%)** no declaran precio y **2 de 3 (66.7%)** no declaran zona. En **venta**, **7 de 50 (14.0%)** no declaran precio y **17 de 50 (34.0%)** no declaran zona. El alquiler es el segmento más opaco en ambas dimensiones, aunque el grupo es muy pequeño.

### Bloque E: Prácticas informales

**E1. ¿Qué porcentaje usa lenguaje informal («oportunidad», «ganga», «permuta», «intercambio» o «cambio»)?** ✅ (n = 122)

> **12 de 122 (9.8%)**. El lenguaje informal no es mayoritario, pero aparece en una de cada doce publicaciones. Las 12 son de Revolico: Facebook no aporta texto suficiente para medir esta dimensión, así que el dato es una **cota inferior** del mercado unificado.

**E2. ¿Qué palabras informales dominan?** ✅ (n = 12)

> - «oportunidad»: **10 anuncios**
> - «cambio»: **1 anuncio**
> - «permuta»: **1 anuncio**
>
> «Oportunidad» es la palabra dominante; «permuta» y «cambio» aparecen en pocas publicaciones. Las palabras «ganga» e «intercambio» no aparecen en la base. La informalidad se expresa más como reclamo comercial que como trueque explícito.

**E3. ¿Las publicaciones informales declaran precio más que las neutras?** 🟡 (n = 12 informales)

> **11 de 12 (91.7%)** de las informales declaran precio, frente a **96 de 110 (87.3%)** de las neutras. La diferencia es de **4.4 puntos porcentuales**. El subgrupo informal es pequeño (n = 12), así que la diferencia es indicativa: no permite concluir que el lenguaje informal implique mayor transparencia.

**E4. ¿La informalidad se concentra en alguna operación?** ✅ (censo de 12 publicaciones informales)

> - Venta: **3 de 12 (25.0%)**
> - Alquiler: **0 de 12 (0.0%)**
> - Sin clasificar: **9 de 12 (75.0%)**
>
> La informalidad aparece en **venta** y en **publicaciones sin operación declarada**; **no aparece en alquiler**. Esto refuerza la lectura de que el alquiler se gestiona por otros canales (contacto directo, redes cerradas) y no necesita el reclamo de «oportunidad» en el título.

**E5. ¿Las publicaciones sin clasificar son más opacas que las clasificadas?** ✅ (censo de operaciones)

> **No.** Las publicaciones sin operación declarada son, en esta base, más completas que las ventas explícitas: **63 de 69 (91.3%)** declaran precio y **57 de 69 (82.6%)** declaran zona. En venta, esas proporciones son **86.0%** y **66.0%**; en alquiler, **33.3%** y **33.3%**. El grupo realmente opaco es el alquiler, no el de las publicaciones sin clasificar. La falta de etiqueta de operación no equivale a falta de información.

### Bloque F: Tipos de inmueble y accesibilidad

**F1. ¿Qué tipo de inmueble se publica más?** ✅ (n = 122)

> - Casa: **63 anuncios** (51.6%)
> - Apartamento: **38 anuncios** (31.1%)
> - Inmueble: **19 anuncios** (15.6%)
> - Cuarto: **2 anuncios** (1.6%)
>
> La casa es el tipo más publicado, seguida del apartamento. Entre ambos suman la mayor parte de la oferta; el «Inmueble» agrupa títulos que no especifican un tipo concreto.

**F2. ¿Qué tipo tiene el precio medio más bajo?** ✅ (n = 33 apartamentos)

> - Apartamento: media **$18,181.82 USD** (n = 33)
> - Casa: media **$42,842.11 USD** (n = 57)
> - Inmueble: media **$49,392.86 USD** (n = 14)
>
> El **apartamento** es la opción más accesible entre los tipos con n ≥ 10: su media es **$18,181.82 USD**, frente a **$42,842.11 USD** de la casa y **$49,392.86 USD** del inmueble sin tipo específico. La diferencia entre apartamento y casa es de **$24,660.29 USD**: el apartamento cuesta aproximadamente **57.6% menos** que la casa en promedio. El cuarto tiene n = 2 y no se usa para comparar.

**F3. ¿Qué tipo tiene la mediana más baja?** ✅ (n = 33 apartamentos)

> - Apartamento: mediana **$15,000.00 USD** (n = 33)
> - Casa: mediana **$33,000.00 USD** (n = 57)
> - Inmueble: mediana **$40,500.00 USD** (n = 14)
>
> El **apartamento** también tiene la mediana más baja: **$15,000.00 USD**, frente a **$33,000.00 USD** de la casa y **$40,500.00 USD** del inmueble. La mediana del apartamento es un **54.5% menor** que la de la casa. La conclusión se mantiene al pasar de la media a la mediana, lo que la hace más robusta frente a valores extremos.

**F4. ¿La diferencia se mantiene en el rango P10–P90?** ✅ (n = 33, 57 y 14)

> - Apartamento: P10 **$7,000.00 USD**, mediana **$15,000.00 USD**, P90 **$33,200.00 USD** (n = 33)
> - Casa: P10 **$14,400.00 USD**, mediana **$33,000.00 USD**, P90 **$86,000.00 USD** (n = 57)
> - Inmueble: P10 **$15,900.00 USD**, mediana **$40,500.00 USD**, P90 **$77,800.00 USD** (n = 14)
>
> Sí. El apartamento es más barato en los tres puntos de la distribución: su P10 ($7,000.00) es menor que el de la casa ($14,400.00) y que el del inmueble ($15,900.00); su P90 ($33,200.00) también es menor que el de la casa ($86,000.00) y el del inmueble ($77,800.00). El rango del apartamento es más estrecho y desplazado hacia abajo. Las distribuciones se solapan, pero el apartamento es consistentemente más accesible.

**F5. ¿Qué tipo concentra más opacidad de precio y zona?** ✅ (censo por tipo)

> - Inmueble: **4 de 19 (21.1%)** sin precio; **10 de 19 (52.6%)** sin zona
> - Casa: **6 de 63 (9.5%)** sin precio; **13 de 63 (20.6%)** sin zona
> - Apartamento: **5 de 38 (13.2%)** sin precio; **7 de 38 (18.4%)** sin zona
> - Cuarto: **0 de 2 (0.0%)** sin precio; **1 de 2 (50.0%)** sin zona
>
> El **Inmueble** (títulos que no especifican un tipo concreto) concentra la mayor opacidad entre los tipos con n ≥ 10: es el que tiene la mayor proporción sin precio y sin zona. La casa tiene más casos absolutos sin zona, pero en proporción el Inmueble la supera. El cuarto muestra una proporción alta, pero solo son 2 publicaciones: es evidencia descriptiva, no una conclusión. La opacidad de zona afecta a todos los tipos; la de precio se concentra en el Inmueble y el Apartamento.

## La ausencia como hallazgo

Los indicadores de ausencia no son un apéndice: son resultados del estudio. La tabla reúne los principales.

| Indicador | Resultado | Lectura social |
|---|---:|---|
| Publicaciones sin precio | **15/122 (12.3%)** | No se puede comparar sin contactar al vendedor. |
| Publicaciones sin zona | **31/122 (25.4%)** | No se puede verificar la ubicación ni comparar barrios. |
| Sin precio y sin zona | **6/122 (4.9%)** | Publicaciones completamente opacas en precio y ubicación. |
| Información completa (precio + zona) | **82/122 (67.2%)** | Dos tercios permiten un análisis mínimo. |
| Alquileres sin precio | **2/3 (66.7%)** | El mercado de alquiler es casi invisible en precios. |
| Alquileres sin zona | **2/3 (66.7%)** | Tampoco se puede ubicar la oferta de alquiler. |
| Publicaciones sin operación declarada | **69/122 (56.6%)** | Más de la mitad no dice si se vende o se alquila. |
| Sin característica física explícita | **78/122 (63.9%)** | La descripción del inmueble es mínima. |
| Totalmente opacas (sin precio, zona ni característica) | **3/122 (2.5%)** | No hay ningún dato útil para comparar. |
| Sin moneda declarada | **15/122 (12.3%)** | No se sabe si el precio, cuando exista, será en USD o CUP. |
| Duplicado entre fuentes | **1 par** | Misma propiedad publicada en Revolico y Facebook. |

La lectura social es directa: la opacidad no afecta a todos por igual. Quien puede llamar, visitar y verificar accede a la información que falta; quien depende del anuncio para comparar queda en desventaja. El alquiler, además, es el segmento con mayor ausencia de precio y zona, lo que sugiere que una parte importante de ese mercado opera por canales informales o de confianza previa.

> **Nota de duplicidad:** la base contiene un par de publicaciones que describen la misma propiedad y el mismo precio en Revolico y Facebook (`revolico-58326838`, `facebook-35`). Se conserva para no alterar el universo acordado de 122, pero el n efectivo sería 121 si se eliminara. El par no cambia las conclusiones: ambos registros son ventas en USD y no modifican las medianas de forma apreciable.

## Conclusiones

1. **La base verificada es de 122 publicaciones.** La versión anterior usaba 134 anuncios etiquetados como Diez de Octubre; la verificación confirmó 83 de Revolico. Con 39 de Facebook, esta versión usa las 122 publicaciones confirmadas (83 de Revolico + 39 de Facebook) y excluye 46 de otros municipios y 8 indeterminadas.
2. **El mercado está dolarizado.** 106 de 107 publicaciones con moneda declarada (99.1%) están en USD; en el total, la proporción es 86.9% y la cota superior posible es 99.2%. Quien no tiene divisas enfrenta una barrera de acceso estructural.
3. **El precio de compra típico es mucho menor que el promedio.** La mediana de las ventas con precio USD es $20,000.00 USD, mientras que la media es $26,023.26 USD. El 80% central está entre $6,200.00 y $60,000.00 USD (n = 43). La media sola sobreestima el precio al que se concentra la oferta.
4. **El alquiler no tiene precio estimable.** Solo 1 de 3 alquileres declara precio, y ninguno en USD. No se puede responder cuánto cuesta alquilar con esta base; esa ausencia es un hallazgo sobre el funcionamiento del segmento.
5. **La desigualdad territorial existe, pero hay que medirla con medianas.** Las cuatro zonas principales concentran 75.8% de las publicaciones con zona. Entre las zonas con n ≥ 10, La Víbora tiene la media más alta ($49,590.91 USD, n = 11) y El Sevillano la mediana más alta ($36,000.00 USD, n = 10); entre las de n ≥ 5, El Mónaco lidera la media ($57,666.67 USD, n = 6), pero la mediana más alta sigue siendo la de El Sevillano ($36,000.00 USD, n = 10). La diferencia entre media y mediana en La Víbora muestra que los valores extremos inflan el promedio.
6. **La opacidad es importante en zona y moderada en precio.** 25.4% no especifica zona, 12.3% no declara precio y 67.2% permite cruzar ambos datos. El 4.9% no tiene ninguno de los dos. La ausencia de información es un mecanismo de desigualdad: quien no puede verificar queda expuesto a la intermediación.
7. **La informalidad es visible pero no domina.** 9.8% usa lenguaje de oportunidad, permuta o cambio. Se concentra en venta y en publicaciones sin operación declarada; no aparece en alquiler. Las informales declaran precio algo más que las neutras (91.7% frente a 87.3%), pero el subgrupo es pequeño y la diferencia no es concluyente. Además, el indicador solo cubre Revolico: es una cota inferior.
8. **El apartamento es la opción más accesible.** Su media es $18,181.82 USD y su mediana $15,000.00 USD (n = 33), frente a la casa ($42,842.11 y $33,000.00 USD; n = 57). La diferencia se mantiene en P10–P90. Entre los tipos con n ≥ 10, el Inmueble sin tipo específico es el más opaco y el más caro en media, lo que sugiere que la falta de información sobre el tipo se asocia con operaciones de mayor valor.

En conjunto, el mercado digital de Diez de Octubre no es un espacio transparente de precios y ubicaciones: es un mercado segmentado por divisas, por acceso a información y por barrios. La base verificada permite afirmar esto con mayor rigor que la versión anterior, y también permite identificar qué no se puede saber: el precio del alquiler, la zona de una cuarta parte de las publicaciones y la operación de más de la mitad. Ese límite es parte del resultado.

## Limitaciones

- **Muestra no probabilística:** 122 publicaciones es una base pequeña y no necesariamente representativa del universo de viviendas del municipio. No hay serie temporal: el corte de Revolico es único (2026-10-31) y Facebook no tiene fechas homogéneas.
- **Integración de fuentes heterogéneas:** Revolico y Facebook no comparten esquema. Facebook aporta descripciones y precios, pero muchas publicaciones no tienen título ni texto crudo, lo que eleva el «sin clasificar» y reduce la medición de informalidad a Revolico. Las comparaciones entre fuentes deben leerse como descriptivas.
- **Duplicado entre fuentes:** se detectó un par Revolico–Facebook de la misma propiedad y el mismo precio. Se conserva en la base de 122 para no alterar el universo acordado; el n efectivo sería 121 si se eliminara.
- **Verificación municipal:** el polígono es una simplificación de 11 vértices y no resuelve casos catastrales a pocos metros del borde. La regla de título usa la mención textual del anuncio; cuando el título es ambiguo (por ejemplo, «Ampliación del Sevillano» o «Reparto Flores»), la publicación se conserva con confianza media y la ambigüedad se documenta. Las 8 indeterminadas se excluyen, lo que puede introducir un sesgo de selección.
- **Clasificación:** el tipo y la operación se toman de los campos normalizados; la zona se completa con el texto declarado. Puede haber errores de asignación, especialmente en títulos ambiguos o sin palabras clave.
- **Campos ausentes:** no hay datos homogéneos de metros cuadrados, estado legal, número de baños, año de construcción, vendedor o agencia. Solo 6 publicaciones de Facebook traen `area_m2`, y ninguna de Revolico: no se puede calcular precio por m² ni distinguir particulares de intermediarios.
- **Alquiler:** solo 3 publicaciones, 1 con precio y ninguno en USD. No se puede estimar un precio de alquiler ni comparar compra y alquiler.
- **Zonas:** solo 91 de 122 publicaciones (74.6%) especifican zona. Los promedios por barrio se basan en subgrupos pequeños (n = 5–25) y deben leerse como evidencia descriptiva.
- **CUP:** el único precio en CUP no se convierte a USD porque no se dispone de un tipo de cambio oficial o de mercado claramente definido para el corte. Se reporta como hallazgo, no como precio comparable.
- **Precios de oferta:** los valores son precios publicados, no precios de transacción. La diferencia entre lo que se pide y lo que se paga no es observable con estos datos.
- **Sesgo de publicación:** las viviendas que no se publican, o que se publican en canales cerrados, no aparecen en la base. La opacidad medida es la del mercado digital visible, no la del mercado total.

## Anexo: fuentes, cobertura y referencias

### A.1 Fuentes y captura

| Fuente | Uso en el análisis | Corte o captura | Confirmadas |
|---|---|---|---:|
| Revolico | Anuncios inmobiliarios: título, precio, enlace y fecha de verificación | 2026-10-31 | 83 |
| Facebook | Anuncios y descripciones: precio y texto parcial | 2026-11-04 | 39 |
| GeoJSON municipal | Polígono DPA `23.09` para la comprobación punto-en-polígono | Copia versionada | — |
| Nominatim / OpenStreetMap | Geocodificación de topónimos; caché local | `datos/geo/geocoding_lha.json` | — |
| ONEI, Anuario Estadístico de Cuba | Contexto de población, vivienda y tenencia | `fuentes/anuario_estadistico_notas.md` | — |

### A.2 Cobertura por campo

| Campo | Cobertura | n | Lectura |
|---|---:|---:|---|
| Precio declarado en USD | 86.9% | 106/122 | Base principal de los análisis de precio. |
| Precio declarado en CUP | 0.8% | 1/122 | No se convierte a USD. |
| Sin precio | 12.3% | 15/122 | Se conserva y se reporta como opacidad. |
| Zona identificada | 74.6% | 91/122 | 84 en ficha + 7 recuperadas del texto. |
| Operación declarada | 43.4% | 53/122 | 50 ventas y 3 alquileres; 69 sin clasificar. |
| Habitaciones | 0.0% | 0/122 | No hay campo homogéneo; no se estima. |
| Baños | 0.0% | 0/122 | No hay campo homogéneo; no se estima. |
| Superficie (m²) | 4.9% | 6/122 | Solo Facebook (`detalles_propiedad.area_m2`). |
| Teléfono | 23.8% | 29/122 | Contacto declarado; no se usa para inferir intermediación. |
| Enlace | 68.0% | 83/122 | Todos de Revolico. |

### A.3 Referencias

- **ONEI.** *Anuario Estadístico de Cuba*. Oficina Nacional de Estadística e Información, República de Cuba. Notas de uso en `fuentes/anuario_estadistico_notas.md`.
- **OpenStreetMap / Nominatim.** Servicio de geocodificación usado para traducir topónimos a coordenadas; resultados cacheados en `datos/geo/geocoding_lha.json`.
- **GeoJSON municipal.** `datos/geo/lha.geojson`, copia versionada del polígono de La Habana; SHA-256 `b9bbcce811d9bbfcee15f5e904d97dc24cf044cabcf17a870487ad361bb7c9e6`.
- **Revolico.** Portal de anuncios clasificados; captura del 2026-10-31. URL base: `https://www.revolico.com`.
- **Facebook.** Publicaciones de grupos y páginas de compraventa; captura del 2026-11-04. No se reproducen enlaces individuales por privacidad.

> **Nota sobre la evidencia:** los precios son precios de oferta, no de transacción. No hay datos homogéneos de metros cuadrados, habitaciones, baños, estado legal ni año de construcción. Las ausencias se reportan; no se imputan.

---

**Proyecto de Ciencia de Datos — Universidad de La Habana**

Facultad de Matemática y Computación (MATCOM)

Profesor: **Yudivian Almeida Cruz**

Repositorio: `Mercado-digital-cubano-en-10-de-octubre`

