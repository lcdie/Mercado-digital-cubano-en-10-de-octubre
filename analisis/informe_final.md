# Mercado inmobiliario digital en Diez de Octubre
## Opacidad, dolarización, desigualdad territorial e informalidad

**Fecha de generación:** 04/11/2026 08:42
**Corte de los datos:** 2026-10-31
**Fuente:** Revolico (anuncios activos)
**Universo estricto:** 134 anuncios de Diez de Octubre
**Anuncios con precio en USD:** 116

## Resumen ejecutivo

La base final contiene **134 anuncios** estrictamente de Diez de Octubre. Respecto a los 171 anuncios del informe anterior, se retiraron **37** que mencionaban otros municipios. Sobre la fuente completa de 270 anuncios, el filtro descartó además 3 con precio inferior a 1,000 USD (que no formaban parte de los 171). La base corregida es la que se usa en todas las respuestas de este informe.

Los hallazgos principales son:

- **Dolarización:** 116 de 117 anuncios con moneda declarada están en USD (**99.1%**), y 116 de 134 del total (**86.6%**).
- **Precios de compra:** mediana **$16,000.00 USD**; P10–P90 **$6,500.00–$43,500.00 USD**; media **$22,597.83 USD** (n = 46 ventas con precio USD).
- **Alquiler:** 1 de 9 alquileres declaran precio y **ninguno lo hace en USD**; el precio de alquiler no es estimable con esta base.
- **Opacidad:** 17 de 134 anuncios (12.7%) no declaran precio; 80 (59.7%) no especifican zona; solo 51 (38.1%) permiten cruzar precio y zona.
- **Desigualdad territorial:** las cuatro zonas principales concentran 42 de 54 anuncios con zona identificada (77.8%). La Víbora tiene la media más alta ($52,277.78 USD, n = 9), pero su mediana es $26,000.00 USD.
- **Informalidad:** 15 de 134 anuncios (11.2%) usan lenguaje de oportunidad, permuta o cambio. No aparecen en alquiler: se concentran en venta y en anuncios sin operación declarada.
- **Tipo de inmueble:** el apartamento es la opción más accesible: media **$19,027.03 USD** y mediana **$15,000.00 USD** (n = 37), frente a la casa con media **$38,768.97 USD** y mediana **$30,000.00 USD** (n = 58).

La ausencia de datos no se trata como un simple defecto: se mide y se reporta como un rasgo del mercado. Un anuncio sin precio, sin zona o sin operación limita la capacidad de comparar y de verificar, y esa limitación es parte del problema social que el estudio documenta.

## Introducción: por qué este mercado es un problema social

El acceso a la vivienda en La Habana no depende solo de la oferta y la demanda. En un mercado digital con precios en divisas, ubicaciones incompletas y anuncios que no declaran si se vende o se alquila, la información se convierte en un recurso desigual. Quien tiene acceso a divisas, a contactos y a tiempo para verificar puede comparar; quien no lo tiene queda expuesto a la opacidad y a la intermediación informal.

Este informe estudia cuatro dimensiones de ese problema:

1. **Precios:** ¿cuánto cuesta comprar y cuánto alquilar, y con qué dispersión? La media sola engaña; por eso se reportan mediana y P10–P90.
2. **Territorio:** ¿la oferta y los precios se distribuyen de forma desigual entre los barrios del mismo municipio?
3. **Dolarización:** ¿en qué medida el mercado funciona en USD y qué implica para quien solo tiene CUP?
4. **Opacidad e informalidad:** ¿cuánta información falta y qué prácticas (lenguaje de oportunidad, permuta, anuncios sin operación) aparecen en los anuncios?

El municipio Diez de Octubre es un caso relevante porque combina una alta densidad de vivienda, barrios con identidad propia (Santos Suárez, Lawton, La Víbora, Luyano, El Sevillano) y una presencia importante de anuncios digitales. La comparación entre barrios permite observar si el mercado reproduce o atenúa las desigualdades territoriales.

## Metodología y corrección de la base

### Fuente y universo

- **Revolico:** única fuente usada en los cálculos. Se analizan los anuncios activos del municipio Diez de Octubre con corte al 2026-10-31.
- **Anuario Estadístico de Cuba (ONEI):** se consulta como contexto general del municipio; no se usa para calcular precios ni proporciones de la muestra digital.
- **Facebook (fuente explorada, no integrada):** se revisaron 37 publicaciones de grupos de compraventa. No se incorporan al análisis cuantitativo porque no comparten el esquema de campos de Revolico (precio anidado, ubicación en texto libre y sin municipio normalizado) y no permiten aplicar el mismo filtro municipal. Mezclarlas sin normalizar habría introducido un sesgo difícil de medir.

### Filtro estricto y contaminación de la base anterior

El campo `municipio` del scraper **no es fiable**: todos los anuncios aparecen como «Diez de Octubre», incluso cuando el título dice «Habana Vieja», «Boyeros», «Arroyo Naranjo» o «Santa Fe». Por eso el filtro revisa el título y el enlace, y la exclusión municipal tiene prioridad sobre el campo `municipio`.

De la fuente inicial de 270 anuncios, el filtro conserva **134** y descarta **136**: 133 por mencionar otro municipio o localidad y 3 por precio inferior a 1,000 USD. La versión anterior del informe usaba 171 anuncios; de ellos, **37 mencionaban otros municipios** y fueron retirados. La base de 134 es la base estrictamente municipal que se usa en esta versión.

Ejemplos de anuncios retirados por pertenecer a otro municipio:

| Anuncio (extracto) | Municipio o zona detectada |
|---|---|
| «Casa en cojímar» | Cojímar (Habana del Este) |
| «8,000 USD Casa 2do piso Poey Arroyo Naranjo» | Arroyo Naranjo |
| «20,000 USD Casa en Boyeros cerca del aeropuerto» | Boyeros |
| «56,000 USD CASA EN SANTA FE PRECIO 56MIL USD» | Santa Fe |
| «33,000 USD MUNICIPIO PLAZA» | Plaza de la Revolución |
| «45,000 USD Casa Independiente con patio en altahabana» | Altahabana |
| «Casa de renta en Río Cristal, Boyeros» | Boyeros |
| «CASA EN VENTA EN LA HABANA, PÁRRAGA (ARROYO NARANJO)» | Arroyo Naranjo |
| «Casa en Marianao» | Marianao |

La distinción es importante: estos 37 anuncios **no son ausencia de información**, son contaminación de la base. Una vez corregida, la ausencia se mide sobre los 134 anuncios que sí pertenecen al municipio.

### Reglas de análisis

- **Precios:** se analizan solo los 116 anuncios con precio declarado en USD. Se excluye 1 anuncio en CUP y 17 sin precio. Para reducir el efecto de valores extremos se reportan media, mediana y rango P10–P90, siempre con el tamaño de muestra (n).
- **Subgrupos pequeños:** los grupos con n < 10 se presentan como evidencia descriptiva, no como conclusión firme. Las zonas con n < 5 no se usan para comparar promedios.
- **Clasificación:** el tipo de inmueble, la zona y la operación se infieren de palabras clave del título y del enlace. Es una clasificación reproducible, pero puede contener errores de asignación.
- **Ausencia:** un anuncio sin precio, sin zona o sin operación no se elimina del universo. Se conserva y se contabiliza como indicador de opacidad, porque su ausencia también describe el mercado.

### Trazabilidad del cambio respecto a la versión anterior

La versión anterior respondía 30 preguntas sobre 171 anuncios. Esa base incluía 37 anuncios de otros municipios, por lo que sus cifras no eran estrictamente de Diez de Octubre y quedan supersedidas. Además, cinco preguntas originales no eran estimables con los datos disponibles (mediana del alquiler, comparación compra–alquiler, precio por metro cuadrado, zonas por operación y precio promedio en CUP). En esta versión esas preguntas se reemplazan por preguntas que sí pueden responderse, incluyendo varias que miden la ausencia de información.

## Las 30 preguntas y sus respuestas

Cada pregunta indica su nivel de evidencia: ✅ sólida (n ≥ 30 o censo completo del subgrupo), 🟡 descriptiva (n = 5–29) y 🔴 no estimable (la ausencia es el hallazgo).

### Bloque A: Precios de referencia

**A1. ¿Cuál es el precio promedio de compra en USD?** ✅ (n = 46)

> **$22,597.83 USD** entre las 46 ventas explícitas con precio en USD. Si se incluyen todos los anuncios con precio USD (ventas y anuncios sin operación declarada; no hay alquileres en USD), la media sube a **$34,134.48 USD** (n = 116), porque los anuncios sin operación declarada incluyen inmuebles de mayor precio. La media de compra es una referencia, no el precio típico: la mediana es bastante menor (A2).

**A2. ¿Cuál es la mediana y el rango P10–P90 del precio de compra en USD?** ✅ (n = 46)

> Mediana **$16,000.00 USD**. El 80% central de las ventas está entre **$6,500.00 USD** (P10) y **$43,500.00 USD** (P90). El mínimo es **$1,000.00 USD** y el máximo **$70,000.00 USD**. La mediana es menor que la media ($22,597.83), señal de una distribución sesgada a la derecha: unos pocos anuncios muy caros elevan el promedio.

**A3. ¿Cuál es el precio promedio o mediano del alquiler?** 🔴 (no estimable)

> **No estimable.** Hay 9 anuncios de alquiler: 1 declara precio (uno solo, en CUP: 50,000 CUP) y 8 no lo declaran (88.9%). Ningún alquiler tiene precio en USD. No se puede calcular una media ni una mediana en USD, y el único precio en CUP no es comparable sin un tipo de cambio explícito. La ausencia de precio de alquiler es el hallazgo, no una limitación menor.

**A4. ¿Qué proporción de alquileres declara precio y en qué moneda?** ✅ (censo de 9 alquileres)

> **1 de 9 (11.1%)** declaran precio. Ese único anuncio está en **CUP** (50,000 CUP); **0 de 9** lo declaran en USD. Los otros 8 alquileres no permiten conocer ni siquiera el orden de magnitud del precio.

**A5. ¿La compra declara precio más que el alquiler?** ✅ (censo de ventas y alquileres)

> Sí. **46 de 52 ventas (88.5%)** declaran precio, frente a **1 de 9 alquileres (11.1%)**. La brecha es de **77.4 puntos porcentuales**. El mercado de compra es mucho más transparente en precio que el de alquiler, que funciona casi por contacto directo.

### Bloque B: Desigualdades territoriales

**B1. ¿Qué zonas concentran la mayor oferta?** ✅ (54 anuncios con zona identificada)

> - Santos Suárez: **14 anuncios** (25.9% de los anuncios con zona)
> - Lawton: **11 anuncios** (20.4% de los anuncios con zona)
> - La Víbora: **9 anuncios** (16.7% de los anuncios con zona)
> - El Sevillano: **8 anuncios** (14.8% de los anuncios con zona)
> - El Mónaco: **5 anuncios** (9.3% de los anuncios con zona)
> - Luyano: **4 anuncios** (7.4% de los anuncios con zona)
> - Santa Catalina: **1 anuncio** (1.9% de los anuncios con zona)
> - Vía Blanca: **1 anuncio** (1.9% de los anuncios con zona)
> - Calzada 10 de Octubre: **1 anuncio** (1.9% de los anuncios con zona)
>
> **54 de 134 anuncios (40.3%)** especifican zona; **80 (59.7%)** no lo hacen. Las cuatro zonas principales —Santos Suárez, Lawton, La Víbora, El Sevillano— reúnen **42 de 54 (77.8%)** de la oferta con zona identificada: la información territorial está muy concentrada en pocos barrios.

**B2. ¿Qué zona tiene el precio promedio más alto?** 🟡 (n = 9 en La Víbora)

> **La Víbora**, con una media de **$52,277.78 USD** (n = 9). Es un resultado descriptivo: el grupo tiene menos de 10 anuncios y su media está influida por un anuncio de $180,000 USD. Si se exige n ≥ 10, la zona con media más alta es **Santos Suárez** ($25,923.08 USD, n = 13).

**B3. ¿Qué zona tiene la mediana más alta?** 🟡 (n = 9 en La Víbora)

> **La Víbora**, con una mediana de **$26,000.00 USD** (n = 9). El orden completo de las zonas con n ≥ 5 es:
>
> - La Víbora: mediana **$26,000.00 USD** (n = 9)
> - El Sevillano: mediana **$23,000.00 USD** (n = 7)
> - Lawton: mediana **$22,500.00 USD** (n = 10)
> - Santos Suárez: mediana **$20,000.00 USD** (n = 13)
> - El Mónaco: mediana **$18,000.00 USD** (n = 5)
>
> La mediana ordena las zonas de forma distinta a la media: La Víbora sigue primera, pero su ventaja se reduce mucho porque la mediana no se deja arrastrar por el anuncio de $180,000.

**B4. ¿La brecha La Víbora–Lawton se mantiene al usar medianas?** 🟡 (n = 9 y 10)

> **No se mantiene con la misma magnitud.** Por media, La Víbora ($52,277.78 USD) supera a Lawton ($23,600.00 USD) en **$28,677.78 USD**. Por mediana, la diferencia es de solo **$3,500.00 USD** ($26,000.00 frente a $22,500.00). La brecha por media es unas 8.2 veces mayor que la brecha por mediana. El anuncio de $180,000 USD en La Víbora (y su P90 de $116,000.00 USD) explica gran parte de la diferencia: la media describe el extremo alto, no el precio típico. Para comparar barrios conviene usar la mediana.

**B5. ¿La falta de zona afecta igual a compra y alquiler?** ✅ (censo de operaciones)

> No. La falta de zona es más grave en alquiler: **8 de 9 (88.9%)** alquileres no especifican zona, frente a **34 de 52 (65.4%)** ventas y **38 de 73 (52.1%)** anuncios sin operación declarada. El alquiler combina las dos opacidades: casi nunca declara precio y casi nunca declara zona.

### Bloque C: Dolarización

**C1. ¿Qué porcentaje de anuncios con moneda declarada está en USD?** ✅ (n = 117)

> **116 de 117 (99.1%)**. El único anuncio con moneda declarada que no está en USD es un alquiler en CUP (50,000 CUP). Los 17 anuncios sin precio no declaran moneda y quedan fuera de este denominador.

**C2. ¿Qué porcentaje del total está en USD?** ✅ (n = 134)

> **116 de 134 (86.6%)**. El resto se reparte entre 17 anuncios sin precio (12.7%) y 1 anuncio en CUP (0.7%). La dolarización es alta incluso cuando se cuenta a los anuncios que no declaran precio.

**C3. ¿La dolarización varía por tipo de inmueble?** ✅ (anuncios con precio)

> - Casa: **58 de 58 (100.0%)** en USD
> - Apartamento: **37 de 37 (100.0%)** en USD
> - Inmueble: **20 de 21 (95.2%)** en USD
> - Cuarto: **1 de 1 (100.0%)** en USD
>
> La dolarización es prácticamente total en todos los tipos con precio. El único anuncio en CUP es un inmueble sin tipo específico (clasificado como «Inmueble») y de alquiler. No hay un tipo de inmueble que funcione principalmente en CUP.

**C4. ¿La dolarización varía por zona?** ✅ (51 anuncios con precio y zona)

> **No se puede medir variación territorial:** los **51 anuncios** con precio y zona identificada están **todos en USD (100%)**. El único anuncio en CUP no especifica zona. La conclusión no es que todas las zonas estén dolarizadas por igual, sino que la base no permite compararlas: la ausencia de zona en el anuncio en CUP impide saber si hay barrios con precios en CUP.

**C5. ¿Cuánto podría variar la dolarización si los anuncios sin precio fueran CUP o USD?** ✅ (cota inferior y superior)

> La proporción de USD en el total está acotada entre **86.6%** y **99.3%**. El límite inferior supone que los 17 anuncios sin precio están en CUP; el superior, que están en USD. La diferencia entre ambos escenarios es de **12.7 puntos porcentuales**. La ausencia de precio y moneda impide conocer el valor exacto, pero permite afirmar que, en cualquier escenario, más de cuatro quintas partes del mercado está en USD o podría estarlo. Esa cota es un resultado, no una especulación.

### Bloque D: Opacidad de la información

**D1. ¿Qué porcentaje no declara precio?** ✅ (n = 134)

> **17 de 134 (12.7%)**. Son anuncios que no permiten comparar precios sin contactar al vendedor. La ausencia es especialmente alta en alquiler (A4).

**D2. ¿Qué porcentaje no especifica zona?** ✅ (n = 134)

> **80 de 134 (59.7%)**. Sin zona no se puede verificar la ubicación ni comparar barrios. Es la dimensión más opaca del mercado: casi tres de cada cinco anuncios omiten este dato.

**D3. ¿Cuántos anuncios carecen de precio y zona a la vez?** ✅ (n = 134)

> **14 de 134 (10.4%)**. En estos anuncios no se puede saber ni cuánto cuesta ni dónde está. Son el núcleo más opaco del mercado digital.

**D4. ¿Qué porcentaje tiene información mínima completa (precio + zona)?** ✅ (n = 134)

> **51 de 134 (38.1%)**. Solo algo más de un tercio de los anuncios permite cruzar precio y zona. Ese es el subconjunto sobre el que se pueden hacer comparaciones territoriales relativamente sólidas; el resto queda fuera por falta de un dato básico.

**D5. ¿La opacidad es mayor en alquiler que en venta?** ✅ (censo de operaciones)

> Sí, sobre todo en precio. En **alquiler**, **8 de 9 (88.9%)** no declaran precio y **8 de 9 (88.9%)** no declaran zona. En **venta**, **6 de 52 (11.5%)** no declaran precio y **34 de 52 (65.4%)** no declaran zona. El alquiler es el segmento más opaco en ambas dimensiones.

### Bloque E: Prácticas informales

**E1. ¿Qué porcentaje usa lenguaje informal («oportunidad», «ganga», «permuta», «intercambio» o «cambio»)?** ✅ (n = 134)

> **15 de 134 (11.2%)**. El lenguaje informal no es mayoritario, pero aparece en uno de cada nueve anuncios. Es una señal de prácticas de intermediación y de negociación que no se ajustan del todo al formato de una oferta inmobiliaria formal.

**E2. ¿Qué palabras informales dominan?** ✅ (n = 15)

> - «oportunidad»: **12 anuncios**
> - «permuta»: **2 anuncios**
> - «cambio»: **1 anuncio**
>
> «Oportunidad» es la palabra dominante; «permuta» y «cambio» aparecen en pocos anuncios. Las palabras «ganga» e «intercambio» no aparecen en la base. La informalidad se expresa más como reclamo comercial que como trueque explícito.

**E3. ¿Los anuncios informales declaran precio más que los neutros?** 🟡 (n = 15 informales)

> **14 de 15 (93.3%)** de los informales declaran precio, frente a **103 de 119 (86.6%)** de los neutros. La diferencia es de **6.8 puntos porcentuales**. El subgrupo informal es pequeño (n = 15), así que la diferencia es indicativa: no permite concluir que el lenguaje informal implique mayor transparencia.

**E4. ¿La informalidad se concentra en alguna operación?** ✅ (censo de 15 anuncios informales)

> - Venta: **6 de 15 (40.0%)**
> - Alquiler: **0 de 15 (0.0%)**
> - Sin clasificar: **9 de 15 (60.0%)**
>
> La informalidad aparece en **venta** y en **anuncios sin operación declarada**; **no aparece en alquiler**. Esto refuerza la lectura de que el alquiler se gestiona por otros canales (contacto directo, redes cerradas) y no necesita el reclamo de «oportunidad» en el título.

**E5. ¿Los anuncios sin clasificar son más opacos que los clasificados?** ✅ (censo de operaciones)

> **No.** Los anuncios sin operación declarada son, en esta base, más completos que las ventas explícitas: **70 de 73 (95.9%)** declaran precio y **35 de 73 (47.9%)** declaran zona. En venta, esas proporciones son **88.5%** y **34.6%**; en alquiler, **11.1%** y **11.1%**. El grupo realmente opaco es el alquiler, no el de los anuncios sin clasificar. La falta de etiqueta de operación no equivale a falta de información.

### Bloque F: Tipos de inmueble y accesibilidad

**F1. ¿Qué tipo de inmueble se publica más?** ✅ (n = 134)

> - Casa: **62 anuncios** (46.3%)
> - Apartamento: **43 anuncios** (32.1%)
> - Inmueble: **27 anuncios** (20.1%)
> - Cuarto: **2 anuncios** (1.5%)
>
> La casa es el tipo más publicado, seguida del apartamento. Entre ambos suman la mayor parte de la oferta; el «Inmueble» agrupa títulos que no especifican un tipo concreto.

**F2. ¿Qué tipo tiene el precio medio más bajo?** ✅ (n = 37 apartamentos)

> - Apartamento: media **$19,027.03 USD** (n = 37)
> - Casa: media **$38,768.97 USD** (n = 58)
> - Inmueble: media **$46,350.00 USD** (n = 20)
>
> El **apartamento** es la opción más accesible entre los tipos con n ≥ 10: su media es **$19,027.03 USD**, frente a **$38,768.97 USD** de la casa y **$46,350.00 USD** del inmueble sin tipo específico. La diferencia entre apartamento y casa es de **$19,741.94 USD**: el apartamento cuesta aproximadamente **50.9% menos** que la casa en promedio. El cuarto tiene n = 1 y no se usa para comparar.

**F3. ¿Qué tipo tiene la mediana más baja?** ✅ (n = 37 apartamentos)

> - Apartamento: mediana **$15,000.00 USD** (n = 37)
> - Casa: mediana **$30,000.00 USD** (n = 58)
> - Inmueble: mediana **$35,500.00 USD** (n = 20)
>
> El **apartamento** también tiene la mediana más baja: **$15,000.00 USD**, frente a **$30,000.00 USD** de la casa y **$35,500.00 USD** del inmueble. La mediana del apartamento es la mitad de la mediana de la casa. La conclusión se mantiene al pasar de la media a la mediana, lo que la hace más robusta frente a valores extremos.

**F4. ¿La diferencia se mantiene en el rango P10–P90?** ✅ (n = 37, 58 y 20)

> - Apartamento: P10 **$6,600.00 USD**, mediana **$15,000.00 USD**, P90 **$37,000.00 USD** (n = 37)
> - Casa: P10 **$8,850.00 USD**, mediana **$30,000.00 USD**, P90 **$76,500.00 USD** (n = 58)
> - Inmueble: P10 **$14,500.00 USD**, mediana **$35,500.00 USD**, P90 **$83,100.00 USD** (n = 20)
>
> Sí. El apartamento es más barato en los tres puntos de la distribución: su P10 ($6,600.00) es menor que el de la casa ($8,850.00) y que el del inmueble ($14,500.00); su P90 ($37,000.00) también es menor que el de la casa ($76,500.00) y el del inmueble ($83,100.00). El rango del apartamento es más estrecho y desplazado hacia abajo. El P90 del apartamento ($37,000.00) supera la mediana de la casa ($30,000.00), pero sigue muy por debajo del P90 de la casa: las distribuciones se solapan, aunque el apartamento es consistentemente más accesible.

**F5. ¿Qué tipo concentra más opacidad de precio y zona?** ✅ (censo por tipo)

> - Inmueble: **6 de 27 (22.2%)** sin precio; **19 de 27 (70.4%)** sin zona
> - Casa: **4 de 62 (6.5%)** sin precio; **38 de 62 (61.3%)** sin zona
> - Apartamento: **6 de 43 (14.0%)** sin precio; **21 de 43 (48.8%)** sin zona
> - Cuarto: **1 de 2 (50.0%)** sin precio; **2 de 2 (100.0%)** sin zona
>
> El **Inmueble** (títulos que no especifican un tipo concreto) concentra la mayor opacidad entre los tipos comparables: 22.2% sin precio y 70.4% sin zona. La casa tiene la menor proporción sin precio (6.5%), pero sigue teniendo 61.3% sin zona. El cuarto muestra 50% y 100%, pero solo son 2 anuncios: es evidencia descriptiva, no una conclusión. La opacidad de zona afecta a todos los tipos; la de precio se concentra en el Inmueble y el Apartamento.

## La ausencia como hallazgo

Los indicadores de ausencia no son un apéndice: son resultados del estudio. La tabla reúne los principales.

| Indicador | Resultado | Lectura social |
|---|---:|---|
| Anuncios sin precio | **17/134 (12.7%)** | No se puede comparar sin contactar al vendedor. |
| Anuncios sin zona | **80/134 (59.7%)** | No se puede verificar la ubicación ni comparar barrios. |
| Sin precio y sin zona | **14/134 (10.4%)** | Anuncios completamente opacos en precio y ubicación. |
| Información completa (precio + zona) | **51/134 (38.1%)** | Solo un tercio permite un análisis mínimo. |
| Alquileres sin precio | **8/9 (88.9%)** | El mercado de alquiler es casi invisible en precios. |
| Alquileres sin zona | **8/9 (88.9%)** | Tampoco se puede ubicar la oferta de alquiler. |
| Anuncios sin operación declarada | **73/134 (54.5%)** | Más de la mitad no dice si se vende o se alquila. |
| Sin característica física explícita | **114/134 (85.1%)** | La descripción del inmueble es mínima. |
| Totalmente opacos (sin precio, zona ni característica) | **11/134 (8.2%)** | No hay ningún dato útil para comparar. |
| Sin moneda declarada | **17/134 (12.7%)** | No se sabe si el precio, cuando exista, será en USD o CUP. |

La lectura social es directa: la opacidad no afecta a todos por igual. Quien puede llamar, visitar y verificar accede a la información que falta; quien depende del anuncio para comparar queda en desventaja. El alquiler, además, es el segmento con mayor ausencia de precio y zona, lo que sugiere que una parte importante de ese mercado opera por canales informales o de confianza previa.

## Conclusiones

1. **La base corregida es de 134 anuncios.** La versión anterior (171) incluía 37 anuncios de otros municipios; sus cifras no eran estrictamente de Diez de Octubre y quedan supersedidas. El filtro estricto también descartó 3 anuncios con precio inferior a 1,000 USD.
2. **El mercado está dolarizado.** 116 de 117 anuncios con moneda declarada (99.1%) están en USD; en el total, la proporción es 86.6% y la cota superior posible es 99.3%. Quien no tiene divisas enfrenta una barrera de acceso estructural.
3. **El precio de compra típico es mucho menor que el promedio.** La mediana de las ventas con precio USD es $16,000.00 USD, mientras que la media es $22,597.83 USD. El 80% central está entre $6,500.00 y $43,500.00 USD (n = 46). La media sola sobreestima el precio al que se concentra la oferta.
4. **El alquiler no tiene precio estimable.** Solo 1 de 9 alquileres declara precio, y ninguno en USD. No se puede responder cuánto cuesta alquilar con esta base; esa ausencia es un hallazgo sobre el funcionamiento del segmento.
5. **La desigualdad territorial existe, pero hay que medirla con medianas.** Las cuatro zonas principales concentran 77.8% de los anuncios con zona. La Víbora tiene la media más alta ($52,277.78 USD, n = 9), pero su mediana es $26,000.00 USD; frente a Lawton, la brecha por media es $28,677.78 USD y por mediana solo $3,500.00 USD. El anuncio de $180,000 USD infla la media.
6. **La opacidad es masiva en zona y grave en precio.** 59.7% no especifica zona, 12.7% no declara precio y solo 38.1% permite cruzar ambos datos. El 10.4% no tiene ninguno de los dos. La ausencia de información es un mecanismo de desigualdad: quien no puede verificar queda expuesto a la intermediación.
7. **La informalidad es visible pero no domina.** 11.2% usa lenguaje de oportunidad, permuta o cambio. Se concentra en venta y en anuncios sin operación declarada; no aparece en alquiler. Los informales declaran precio algo más que los neutros (93.3% frente a 86.6%), pero el subgrupo es pequeño y la diferencia no es concluyente.
8. **El apartamento es la opción más accesible.** Su media es $19,027.03 USD y su mediana $15,000.00 USD (n = 37), frente a la casa ($38,768.97 y $30,000.00 USD; n = 58). La diferencia se mantiene en P10–P90. Entre los tipos con n ≥ 10, el Inmueble sin tipo específico es el más opaco y el más caro en media, lo que sugiere que la falta de información sobre el tipo se asocia con operaciones de mayor valor.

En conjunto, el mercado digital de Diez de Octubre no es un espacio transparente de precios y ubicaciones: es un mercado segmentado por divisas, por acceso a información y por barrios. La base corregida permite afirmar esto con mayor rigor que la versión anterior, y también permite identificar qué no se puede saber: el precio del alquiler, la zona de la mayoría de los anuncios y la operación de más de la mitad. Ese límite es parte del resultado.

## Limitaciones

- **Fuente única:** los datos provienen solo de Revolico; no representan todo el mercado inmobiliario de Diez de Octubre. Facebook se exploró (37 publicaciones), pero no se integró por incompatibilidad de esquema y de normalización municipal.
- **Muestra:** 134 anuncios es una base pequeña y no necesariamente representativa del universo de viviendas del municipio. No hay serie temporal: el corte es único (2026-10-31).
- **Clasificación por palabras clave:** el tipo, la zona y la operación se infieren del título y del enlace. Puede haber errores de asignación, especialmente en títulos ambiguos o sin palabras clave.
- **Campos ausentes:** no hay datos de metros cuadrados, estado legal, número de baños, año de construcción, vendedor o agencia. No se puede calcular precio por m² ni distinguir particulares de intermediarios.
- **Alquiler:** solo 9 anuncios, 1 con precio y ninguno en USD. No se puede estimar un precio de alquiler ni comparar compra y alquiler.
- **Zonas:** solo 54 de 134 anuncios (40.3%) especifican zona. Los promedios por barrio se basan en subgrupos pequeños (n = 5–14) y deben leerse como evidencia descriptiva.
- **CUP:** el único precio en CUP no se convierte a USD porque no se dispone de un tipo de cambio oficial o de mercado claramente definido para el corte. Se reporta como hallazgo, no como precio comparable.
- **Sesgo de publicación:** los anuncios que no se publican, o que se publican en canales cerrados, no aparecen en la base. La opacidad medida es la del mercado digital visible, no la del mercado total.

---

**Proyecto de Ciencia de Datos — Universidad de La Habana**

Facultad de Matemática y Computación (MATCOM)

Profesor: **Yudivian Almeida Cruz**

Repositorio: `Mercado-digital-cubano-en-10-de-octubre`

