# Mercado inmobiliario digital en Diez de Octubre
## Versión revisada: 30 preguntas originales con 10 reemplazos

**Fecha de generación:** 04/11/2026 09:59
**Corte de los datos:** 2026-10-31
**Fuente:** Revolico (anuncios activos)
**Universo estricto:** 134 anuncios de Diez de Octubre
**Anuncios con precio en USD:** 116

## Qué cambia en esta versión

Este informe parte del cuestionario original de 30 preguntas. Se **conservan 20 preguntas** y se **reemplazan 10** que no alcanzaban un respaldo suficiente: dependían de uno o pocos anuncios, de un campo que no existe en la base o de una comparación entre subgrupos demasiado pequeños. Los reemplazos no inventan datos: convierten esa debilidad en preguntas respondibles y, en varios casos, en mediciones explícitas de la ausencia de información.

La base usada es la corregida de **134 anuncios estrictamente de Diez de Octubre**. La fuente completa tiene 270 anuncios; el filtro descartó 136: 133 por mencionar otro municipio o localidad y 3 por precio inferior a 1,000 USD. Las cifras de la versión anterior sobre 171 anuncios no se reutilizan porque incluían anuncios de otros municipios.

## Resumen ejecutivo

- **Dolarización:** 116 de 117 anuncios con moneda declarada están en USD (**99.1%**), y 116 de 134 del total (**86.6%**).
- **Precios:** media **$34,134.48 USD** y mediana **$25,000.00 USD** (n = 116). El 80% central está entre **$7,750.00** y **$75,000.00 USD**.
- **Precios de compra:** en las 46 ventas explícitas con precio USD, media **$22,597.83 USD**, mediana **$16,000.00 USD** y P10–P90 **$6,500.00–$43,500.00 USD**.
- **Alquiler:** 1 de 9 alquileres declara precio y **ninguno lo hace en USD**; el precio de alquiler no es estimable con esta base.
- **Opacidad:** 17 de 134 anuncios (12.7%) no declaran precio; 80 (59.7%) no especifican zona; solo 51 (38.1%) permiten cruzar precio y zona.
- **Desigualdad territorial:** las cuatro zonas principales concentran 42 de 54 anuncios con zona identificada (77.8%). La Víbora tiene la media más alta ($52,277.78 USD, n = 9), pero su mediana es $26,000.00 USD.
- **Informalidad:** 15 de 134 anuncios (11.2%) usan lenguaje de oportunidad, permuta o cambio. Se concentran en venta y en anuncios sin operación declarada; no aparecen en alquiler.
- **Tipo de inmueble:** el apartamento es la opción más accesible: mediana **$15,000.00 USD** (n = 37) frente a la casa, con mediana **$30,000.00 USD** (n = 58).

La ausencia de datos se mide como un rasgo del mercado. Un anuncio sin precio, sin zona o sin operación limita la capacidad de comparar y de verificar; esa limitación es parte del problema social que el estudio documenta.

## Metodología

- **Fuente:** Revolico, única fuente usada en los cálculos. Se analizan los anuncios activos de Diez de Octubre con corte al 2026-10-31.
- **Universo:** 134 anuncios estrictos. El filtro revisa título y enlace porque el campo `municipio` del scraper no es fiable: todos los anuncios aparecen como «Diez de Octubre» aunque el título diga otro municipio.
- **Precios:** se analizan los 116 anuncios con precio en USD. Se excluye 1 anuncio en CUP y 17 sin precio. Se reportan media, mediana, P10–P90 y media recortada para reducir el efecto de los valores extremos.
- **Clasificación:** tipo, zona y operación se infieren de palabras clave del título y del enlace. Es reproducible, pero puede contener errores de asignación.
- **Ausencia:** un anuncio sin precio, zona u operación no se elimina. Se conserva y se contabiliza como indicador de opacidad.

### Niveles de evidencia

- ✅ **Sólida:** n ≥ 30 o censo completo del subgrupo.
- 🟡 **Descriptiva:** n = 5–29; el resultado orienta, pero no se generaliza.
- 🔴 **No estimable:** la ausencia de datos es el hallazgo.

## Las 10 preguntas reemplazadas

La siguiente tabla documenta qué pregunta se retiró, por qué no tenía respaldo suficiente y qué pregunta la sustituye. Las 20 restantes se conservan con su redacción original.

| # | Pregunta original | Por qué no alcanza | Pregunta de reemplazo |
|---|---|---|---|
| 10 | ¿Qué tipo de inmueble concentra el precio máximo declarado? | La respuesta depende de un solo anuncio (el máximo de $180,000). No describe un tipo de inmueble: describe un caso. | ¿Cuál es la mediana del precio en USD por tipo de inmueble? |
| 12 | ¿Qué tipo de inmueble domina en la zona con el precio promedio más alto? | La zona con la media más alta (La Víbora) solo tiene 9 anuncios con precio; 6 son apartamentos. n = 9. | ¿La declaración de precio depende de que el anuncio identifique zona? |
| 13 | ¿Cuál es la cantidad más común de cuartos/habitaciones? | Solo 14 anuncios permiten extraer un número explícito de cuartos. n = 14. | ¿Qué proporción de anuncios es totalmente opaca (sin precio, zona ni característica)? |
| 14 | ¿Cómo varía el precio según el número de cuartos? | Solo 12 anuncios combinan número de cuartos y precio en USD. n = 12. | ¿Qué proporción de anuncios ofrece información completa (precio y zona)? |
| 15 | ¿Qué porcentaje de anuncios menciona garaje y cómo se relaciona con el precio? | Solo 7 anuncios mencionan garaje. n = 7. | ¿La opacidad de precio y zona es mayor en alquiler o en venta? |
| 16 | ¿Cuántos anuncios especifican 'planta baja' y cuál es su precio promedio? | Solo 8 anuncios mencionan planta baja o bajos. n = 8. | ¿Qué tipo de inmueble presenta mayor opacidad de precio y zona? |
| 20 | ¿Qué zona tiene el precio promedio más alto entre los anuncios con precio en USD? | La zona con la media más alta (La Víbora) solo tiene 9 anuncios con precio y su media está inflada por un valor extremo de $180,000. n = 9. | ¿Qué porcentaje de anuncios con precio USD queda dentro del tramo P10–P90? |
| 22 | ¿Hay diferencia de precios entre zonas dentro del mismo municipio? | La diferencia se apoya en los mismos grupos pequeños (n = 9 y n = 10) y en una media sensible a valores extremos. | ¿Cuánto cambia el precio promedio al recortar 10% de cada cola? |
| 26 | ¿Los anuncios con lenguaje informal declaran precio con más frecuencia que los neutros? | Solo 15 anuncios usan lenguaje informal; la comparación es descriptiva. n = 15. | ¿Cómo se distribuye la informalidad según el tipo de operación? |
| 29 | ¿Cuántos anuncios parecen de particulares frente a posibles anuncios repetidos o agencias? | La base no tiene campo de vendedor ni de agencia; los títulos únicos no permiten distinguir unos de otros. | ¿Qué proporción de anuncios no declara operación y cómo se distribuye por tipo de inmueble? |

Las 20 preguntas conservadas son: Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9, Q11, Q17, Q18, Q19, Q21, Q23, Q24, Q25, Q27, Q28, Q30. Las 10 reemplazadas son: Q10, Q12, Q13, Q14, Q15, Q16, Q20, Q22, Q26, Q29.

## Las 30 preguntas y sus respuestas

### Bloque A: Precios del mercado

**1. ¿Cuál es el precio promedio de los anuncios con precio declarado en USD en Diez de Octubre?** ✅ (n = 116)

> **$34,134.48 USD** entre los 116 anuncios con precio en USD. Si se restringe a las 46 ventas explícitas con precio en USD, la media baja a **$22,597.83 USD**: los anuncios sin operación declarada incluyen inmuebles de mayor precio y elevan el promedio general.
>
> La media no es el precio típico. La mediana (Q2) y la media recortada (Q22) son referencias más estables.

**2. ¿Cuál es el precio mediano de los anuncios con precio declarado en USD?** ✅ (n = 116)

> **$25,000.00 USD** (n = 116). En las 46 ventas explícitas con precio USD, la mediana es **$16,000.00 USD**.
>
> La mediana es menor que la media general porque unos pocos anuncios muy caros elevan el promedio. Para una persona que busca comprar, la mediana de ventas es la referencia más realista.

**3. ¿Cuál es el rango de precios que cubre el 80% central de los anuncios?** ✅ (n = 116)

> Entre **$7,750.00 USD** (P10) y **$75,000.00 USD** (P90). Dentro de ese tramo quedan **94 de 116 anuncios (81.0%)**.
>
> El mínimo es **$1,000.00 USD** y el máximo **$180,000.00 USD**. El rango central es amplio: la diferencia entre P10 y P90 es de **$67,250.00 USD**.

**4. ¿Cuáles son el anuncio más caro y el más barato publicados?** ✅ (n = 116)

> - Más caro: **$180,000.00 USD**, clasificado como Inmueble («180,000 USD Cada en la víbora 10 octubre»).
> - Más barato: **$1,000.00 USD**.
>
> El segundo precio más alto es **$120,000.00 USD**. El máximo de $180,000 es un valor atípico que conviene tratar por separado: eleva la media y no representa al conjunto.

**5. ¿Qué proporción de anuncios no declara precio?** ✅ (n = 134)

> **17 de 134 anuncios (12.7%)** no declaran precio. Los otros 117 sí lo hacen: 116 en USD y 1 en CUP.
>
> No declarar precio obliga a contactar al vendedor y reduce la posibilidad de comparar. Es un indicador de opacidad, no un dato perdido.

**6. ¿Qué tan dispersos son los precios respecto a la media?** ✅ (n = 116)

> La media ($34,134.48) supera a la mediana ($25,000.00) en **$9,134.48**, un **36.5%** de la mediana.
>
> Además, **22 de 116 anuncios (19.0%)** quedan fuera del tramo P10–P90: 12 por debajo de P10 y 10 por encima de P90. La distribución está sesgada a la derecha: una minoría de inmuebles muy caros infla el promedio.

### Bloque B: Tipos de inmueble

**7. ¿Cuáles son los tipos de inmueble más publicados?** ✅ (n = 134)

> - Casa: **62 anuncios (46.3%)**
> - Apartamento: **43 anuncios (32.1%)**
> - Inmueble: **27 anuncios (20.1%)**
> - Cuarto: **2 anuncios (1.5%)**
>
> «Inmueble» agrupa los títulos que no especifican un tipo. No es una categoría física homogénea, sino un residual de clasificación.

**8. ¿Qué porcentaje son casas independientes frente a apartamentos?** ✅ (n = 105)

> - Casas: **62 de 105 (59.0%)**
> - Apartamentos: **43 de 105 (41.0%)**
>
> Entre los anuncios con tipo identificable como casa o apartamento, la casa es mayoría. El resto de los anuncios queda en «Inmueble» o «Cuarto» y no entra en esta comparación.

**9. ¿Cuál es el precio promedio por tipo de inmueble (anuncios con precio en USD)?** ✅ (n = 116)

> - Casa: **$38,768.97 USD** (n = 58)
> - Apartamento: **$19,027.03 USD** (n = 37)
> - Inmueble: **$46,350.00 USD** (n = 20)
> - Cuarto: **$80,000.00 USD** (n = 1)
>
> El apartamento tiene el promedio más bajo. El Cuarto solo tiene un anuncio con precio: su promedio no se usa para comparar. La media de Inmueble está afectada por el máximo de $180,000; por eso la Q10 reporta medianas.

**10. ¿Cuál es la mediana del precio en USD por tipo de inmueble?** ✅ (n = 116)

> - Apartamento: **$15,000.00 USD** (n = 37)
> - Casa: **$30,000.00 USD** (n = 58)
> - Inmueble: **$35,500.00 USD** (n = 20)
> - Cuarto: **$80,000.00 USD** (n = 1)
>
> La mediana confirma el orden de accesibilidad: el apartamento es la opción más barata (mediana $15,000) y la casa cuesta el doble en términos medianos ($30,000). El Inmueble tiene la mediana más alta ($35,500), pero es una categoría residual y su media está inflada por un valor extremo. El Cuarto no se compara: n = 1.
>
> Esta pregunta sustituye a la original sobre el tipo que concentra el precio máximo, que dependía de un solo anuncio.

**11. ¿Cuántos anuncios se identifican como venta, alquiler o sin clasificar?** ✅ (n = 134)

> - Venta: **52 anuncios (38.8%)**
> - Alquiler: **9 anuncios (6.7%)**
> - Sin clasificar: **73 anuncios (54.5%)**
>
> De las 52 ventas, 46 (88.5%) declaran precio. De los 9 alquileres, solo 1 (11.1%) lo hace, y en CUP; ningún alquiler declara precio en USD. La operación no declarada es la categoría más frecuente.

**12. ¿La declaración de precio depende de que el anuncio identifique zona?** ✅ (n = 134)

> - Con zona identificada: **51 de 54 (94.4%)** declaran precio.
> - Sin zona identificada: **66 de 80 (82.5%)** declaran precio.
>
> La diferencia es de **11.9 puntos porcentuales** a favor de los anuncios con zona. No implica causalidad: ambos grupos declaran precio en una proporción alta. Lo que muestra es que la falta de zona no impide conocer el precio, pero sí reduce algo la transparencia.
>
> Esta pregunta sustituye a la original sobre el tipo dominante en la zona más cara, que se apoyaba en 9 anuncios.

### Bloque C: Características físicas y opacidad

**13. ¿Qué proporción de anuncios es totalmente opaca (sin precio, zona ni característica)?** ✅ (n = 134)

> **11 de 134 anuncios (8.2%)** no declaran precio, no especifican zona y no mencionan ninguna característica física (garaje, patio, azotea, terraza, balcón, baño, cuarto o habitación).
>
> Otros 14 anuncios (10.4%) carecen de precio y zona, pero 3 de ellos mencionan al menos una característica. La opacidad total es minoritaria, pero existe: son anuncios que solo ofrecen un título y un contacto.
>
> Esta pregunta sustituye a la original sobre la cantidad más común de cuartos, que solo podía calcularse en 14 anuncios.

**14. ¿Qué proporción de anuncios ofrece información completa (precio y zona)?** ✅ (n = 134)

> **51 de 134 anuncios (38.1%)** declaran precio y especifican zona. Es decir, menos de 4 de cada 10 anuncios permiten cruzar precio y ubicación.
>
> De los 117 anuncios con precio, 51 (43.6%) también identifican zona. De los 54 con zona, 51 (94.4%) también declaran precio.
>
> Esta pregunta sustituye a la original sobre la variación del precio según el número de cuartos, que solo tenía 12 casos con precio.

**15. ¿La opacidad de precio y zona es mayor en alquiler o en venta?** 🟡 (censo de 9 alquileres y 52 ventas)

> - Venta (n = 52): 6 sin precio (11.5%); 34 sin zona (65.4%).
> - Alquiler (n = 9): 8 sin precio (88.9%); 8 sin zona (88.9%).
> - Sin clasificar (n = 73): 3 sin precio (4.1%); 38 sin zona (52.1%).
>
> El alquiler es mucho más opaco: **8 de 9 alquileres (88.9%)** no declaran precio y **8 de 9 (88.9%)** no especifican zona. En venta, la falta de precio es menor (**6 de 52, 11.5%**), aunque la falta de zona sigue siendo alta (**34 de 52, 65.4%**).
>
> La diferencia es consistente, pero el grupo de alquiler es pequeño (n = 9). Se reporta como evidencia descriptiva. Además, **7 de 9 alquileres** carecen de precio y zona a la vez, frente a **5 de 52 ventas**.
>
> Esta pregunta sustituye a la original sobre garaje, que solo tenía 7 anuncios.

**16. ¿Qué tipo de inmueble presenta mayor opacidad de precio y zona?** 🟡 (subgrupos de 2 a 62 anuncios)

> - Casa (n = 62): 4 sin precio (6.5%); 38 sin zona (61.3%).
> - Apartamento (n = 43): 6 sin precio (14.0%); 21 sin zona (48.8%).
> - Inmueble (n = 27): 6 sin precio (22.2%); 19 sin zona (70.4%).
> - Cuarto (n = 2): 1 sin precio (50.0%); 2 sin zona (100.0%).
>
> Entre los grupos con un tamaño mínimamente interpretable, **Inmueble** es el más opaco: **6 de 27 (22.2%)** no declaran precio y **19 de 27 (70.4%)** no especifican zona. Casa registra **4 de 62 (6.5%)** sin precio y **38 de 62 (61.3%)** sin zona; Apartamento, **6 de 43 (14.0%)** y **21 de 43 (48.8%)**, respectivamente.
>
> Cuarto muestra 50.0% sin precio y 100% sin zona, pero solo tiene 2 anuncios: no se usa para concluir. La categoría Inmueble, al ser un residual de títulos que no especifican tipo, concentra la mayor ambigüedad.
>
> Esta pregunta sustituye a la original sobre planta baja, que solo tenía 8 anuncios.

**17. ¿Qué proporción de anuncios incluye al menos una característica física explícita?** ✅ (n = 134)

> **20 de 134 anuncios (14.9%)** mencionan al menos una característica física: garaje, patio, azotea, terraza, balcón, baño, cuartos o habitaciones. Los otros 114 (85.1%) no describen ninguna.
>
> La cobertura es baja: la mayoría de los anuncios se limita a precio, tipo y, a veces, zona. Cualquier análisis de características físicas queda limitado a una minoría de la muestra.

**18. ¿Qué características físicas se mencionan con más frecuencia?** ✅ (n = 134)

> - Habitación/cuarto: **14 anuncios** (10.4%)
> - Garaje: **7 anuncios** (5.2%)
> - Baño: **3 anuncios** (2.2%)
> - Balcón: **2 anuncios** (1.5%)
> - Terraza: **1 anuncio** (0.7%)
> - Azotea: **1 anuncio** (0.7%)
> - Patio: **0 anuncios**
>
> Los conteos son menciones y pueden solaparse: un mismo anuncio puede incluir varias características. Solo 20 anuncios contienen al menos una, por lo que estos números describen una minoría muy específica de la oferta.

### Bloque D: Ubicación dentro de Diez de Octubre

**19. ¿Qué zonas o barrios aparecen con más frecuencia en los anuncios?** ✅ (n = 134)

> - Santos Suárez: **14 anuncios**
> - Lawton: **11 anuncios**
> - La Víbora: **9 anuncios**
> - El Sevillano: **8 anuncios**
> - El Mónaco: **5 anuncios**
> - Luyano: **4 anuncios**
> - Santa Catalina: **1 anuncio**
> - Vía Blanca: **1 anuncio**
> - Calzada 10 de Octubre: **1 anuncio**
>
> **54 de 134 anuncios (40.3%)** especifican zona; **80 (59.7%)** no lo hacen.

**20. ¿Qué porcentaje de anuncios con precio USD queda dentro del tramo P10–P90?** ✅ (n = 116)

> **94 de 116 anuncios (81.0%)** quedan dentro del tramo **$7,750.00–$75,000.00 USD**.
> Quedan fuera **22 (19.0%)**: 12 por debajo de P10 (10.3%) y 10 por encima de P90 (8.6%).
>
> La pregunta complementa la Q3: allí se delimita el rango; aquí se cuantifica cuánta masa de anuncios queda dentro y cuánta en las colas. Que casi una quinta parte quede fuera confirma que la distribución tiene extremos relevantes.
>
> Esta pregunta sustituye a la original sobre la zona con el precio promedio más alto, que dependía de 9–10 anuncios.

**21. ¿Qué zona tiene la mayor cantidad de anuncios publicados?** ✅ (n = 54 con zona)

> **Santos Suárez**, con **14 anuncios** (25.9% de los que tienen zona). De ellos, 13 declaran precio en USD.
>
> Le siguen Lawton (11), La Víbora (9) y El Sevillano (8). La oferta con zona identificada se concentra en pocos barrios.

**22. ¿Cuánto cambia el precio promedio al recortar 10% de cada cola?** ✅ (n = 94 tras el recorte)

> - Media original: **$34,134.48 USD** (n = 116)
> - Media recortada al 10%: **$29,494.68 USD** (n = 94)
> - Mediana: **$25,000.00 USD** (n = 116)
>
> El recorte elimina 11 precios por cada cola (22 en total) y deja un rango de **$7,000.00–$75,000.00 USD**. La media recortada es **$4,639.80 USD menor** que la media original (13.6% menos), lo que confirma que los valores extremos inflan el promedio.
>
> Aun así, la media recortada sigue por encima de la mediana: la asimetría no desaparece del todo. La mediana sigue siendo la referencia más conservadora.
>
> Esta pregunta sustituye a la original sobre diferencias de precio entre zonas, que se apoyaba en grupos de 9 y 10 anuncios.

**23. ¿Qué proporción de los anuncios con zona identificada se concentra en las cuatro zonas principales?** ✅ (censo de 54 anuncios con zona)

> Las cuatro zonas principales —Santos Suárez, Lawton, La Víbora, El Sevillano— reúnen **42 de 54 anuncios con zona identificada (77.8%)**.
>
> Los 12 anuncios restantes se reparten entre 5 zonas con pocos casos. La oferta está muy concentrada, pero esa concentración convive con una mayoría de anuncios que ni siquiera declaran zona.

**24. ¿Cuántos anuncios no especifican zona dentro del municipio?** ✅ (n = 134)

> **80 de 134 anuncios (59.7%)** no especifican zona en el título ni en el enlace. Solo **54 (40.3%)** permiten ubicar el inmueble dentro de un barrio.
>
> La ubicación es el dato más ausente: 80 de 134 anuncios (59.7%). Sin zona no se puede comparar el precio por barrio ni verificar si el anuncio corresponde realmente a Diez de Octubre.

### Bloque E: Moneda y mercado informal

**25. ¿Qué proporción de anuncios con moneda declarada usa USD frente a CUP?** ✅ (n = 117)

> - USD: **116 de 117 (99.1%)**
> - CUP: **1 de 117 (0.9%)**
>
> En el total del universo, el USD aparece en **116 de 134 anuncios (86.6%)**. Los otros 17 no declaran precio ni moneda.
>
> El mercado está prácticamente dolarizado. Quien solo dispone de CUP necesita un tipo de cambio y enfrenta una barrera adicional.

**26. ¿Cómo se distribuye la informalidad según el tipo de operación?** 🟡 (n = 15 anuncios informales)

> - Venta: **6 de 15 (40.0%)**
> - Sin clasificar: **9 de 15 (60.0%)**
> - Alquiler: **0 de 15 (0.0%)**
>
> Dentro de cada operación, la proporción es:
>
> - Venta: **6 de 52 (11.5%)**
> - Alquiler: **0 de 9 (0.0%)**
> - Sin clasificar: **9 de 73 (12.3%)**
>
> La informalidad se reparte entre venta y anuncios sin operación declarada; no aparece en alquiler. El grupo es pequeño (15 anuncios), así que la conclusión es descriptiva.
>
> Esta pregunta sustituye a la original sobre si los anuncios informales declaran precio más que los neutros, comparación que descansaba en 15 casos.

**27. ¿Qué porcentaje de anuncios incluye palabras de mercado informal?** ✅ (n = 134)

> **15 de 134 anuncios (11.2%)** incluyen palabras como «oportunidad», «ganga», «permuta», «intercambio» o «cambio».
>
> Distribución de las menciones:
>
> - Oportunidad: **12 anuncios**
> - Permuta: **2 anuncios**
> - Cambio: **1 anuncio**
>
> Los otros **119 anuncios (88.8%)** usan un lenguaje neutro.

**28. ¿Qué rango de precios es más frecuente entre los anuncios con precio en USD?** ✅ (n = 116)

> El rango **10,000 – 20,000 USD** es el más frecuente, con **32 anuncios (27.6% de los 116 con precio en USD)**.
>
> Distribución completa:
>
> - 0 – 10,000: 17 anuncios (14.7%)
> - 10,000 – 20,000: 32 anuncios (27.6%)
> - 20,000 – 30,000: 17 anuncios (14.7%)
> - 30,000 – 40,000: 13 anuncios (11.2%)
> - 40,000 – 50,000: 12 anuncios (10.3%)
> - 50,000 – 60,000: 4 anuncios (3.4%)
> - 60,000 – 70,000: 5 anuncios (4.3%)
> - 70,000 – 80,000: 7 anuncios (6.0%)
> - 80,000 y más: 9 anuncios (7.8%)
>
> El **56.9%** de los anuncios se concentra por debajo de 30,000 USD, y el **78.4%** por debajo de 50,000 USD.

**29. ¿Qué proporción de anuncios no declara operación y cómo se distribuye por tipo de inmueble?** ✅ (n = 134)

> **73 de 134 anuncios (54.5%)** no declaran si se venden o se alquilan. Es el segundo dato más ausente, después de la zona (59.7%).
>
> Distribución por tipo:
>
> - Casa: **32 de 62 (51.6%)**
> - Apartamento: **22 de 43 (51.2%)**
> - Inmueble: **18 de 27 (66.7%)**
> - Cuarto: **1 de 2 (50.0%)**
>
> La falta de operación afecta a todos los tipos, pero es más frecuente en Inmueble (66.7%). No equivale a falta de precio: **70 de 73 anuncios sin operación (95.9%)** sí declaran precio.
>
> Esta pregunta sustituye a la original sobre particulares frente a agencias, que no podía responderse porque la base no tiene campo de vendedor.

**30. ¿Qué recomendación práctica se puede hacer a alguien que quiera comprar o alquilar en Diez de Octubre?** ✅ (síntesis de Q1–Q29)

> 1. **Presupuesto:** la mediana general es **$25,000.00 USD** y la de ventas explícitas **$16,000.00 USD**. El 80% central está entre **$7,750.00 y $75,000.00 USD**; el tramo más frecuente es **10,000 – 20,000 USD** (32 anuncios, 27.6%).
> 2. **Tipo de inmueble:** el apartamento tiene mediana **$15,000.00 USD** (n = 37); la casa, **$30,000.00 USD** (n = 58). El apartamento es la opción más accesible.
> 3. **Zonas:** Santos Suárez concentra la mayor oferta (14 anuncios), seguida por Lawton (11) y La Víbora (9). La Víbora tiene la media más alta, pero su mediana es **$26,000.00 USD**; Lawton **$22,500.00 USD** y Santos Suárez **$20,000.00 USD**. Para comparar, use medianas: La Víbora sigue siendo más cara, pero la brecha es menor que con la media.
> 4. **Moneda:** **116 de 117 anuncios con moneda declarada (99.1%)** están en USD. Hay que contar con divisas o verificar el tipo de cambio si se paga en CUP.
> 5. **Información incompleta:** **17 anuncios (12.7%)** no declaran precio, **80 (59.7%)** no especifican zona y **11 (8.2%)** son totalmente opacos. Solo **51 (38.1%)** permiten cruzar precio y zona. Verifique siempre precio, ubicación y situación legal directamente con el vendedor.
> 6. **Precaución estadística:** los subgrupos por zona y tipo son pequeños. Use las medianas y los rangos, no solo los promedios, y no generalice los resultados de un barrio al municipio completo.

## Conclusiones

1. **Dolarización casi total:** 116 de 117 anuncios con moneda declarada (99.1%) están en USD. El mercado digital de Diez de Octubre funciona en divisas.
2. **Precios sesgados a la derecha:** la media ($34,134.48) supera a la mediana ($25,000.00) en $9,134.48. La media recortada al 10% ($29,494.68) reduce la influencia de los extremos, pero sigue por encima de la mediana.
3. **El apartamento es la opción más accesible:** mediana $15,000.00 USD frente a $30,000.00 USD de la casa. La diferencia de mediana es de $15,000.00 USD.
4. **Concentración territorial:** las cuatro zonas principales reúnen 42 de 54 anuncios con zona (77.8%). La Víbora tiene la media más alta ($52,277.78), pero su mediana ($26,000.00) es mucho menor: el promedio está inflado por valores extremos.
5. **La opacidad es un rasgo estructural:** solo 51 de 134 anuncios (38.1%) permiten cruzar precio y zona; 80 (59.7%) no especifican zona; 73 (54.5%) no declaran operación; y 11 (8.2%) son totalmente opacos.
6. **El alquiler es el segmento más opaco:** 8 de 9 alquileres no declaran precio y 8 de 9 no especifican zona. Además, ningún alquiler declara precio en USD, por lo que no se puede estimar una referencia de alquiler con esta base.
7. **La informalidad se concentra en venta y en anuncios sin operación:** 15 anuncios (11.2%) usan lenguaje de oportunidad, permuta o cambio; 6 son ventas y 9 no declaran operación. No hay ninguno en alquiler.
8. **Los 10 reemplazos mejoran la calidad de la evidencia:** en lugar de forzar estimaciones con 1, 7, 8, 9, 10, 12, 14 o 15 casos, el informe mide la opacidad, compara medianas y usa estimadores robustos. La ausencia de datos deja de ser una limitación oculta y se convierte en un resultado.

## Limitaciones

- Los datos provienen solo de Revolico; no representan todo el mercado inmobiliario de Diez de Octubre.
- Se exploró Facebook (37 publicaciones), pero se excluyó del análisis cuantitativo porque no comparte el esquema de campos de Revolico ni un municipio normalizado.
- La muestra es de 134 anuncios y puede no ser representativa del mercado completo.
- La clasificación de tipo, zona y operación depende de palabras clave y puede contener errores.
- Los subgrupos por zona (n = 5–14), alquiler (n = 9) y Cuarto (n = 2) son pequeños; sus resultados son descriptivos.
- No existe un campo de vendedor o agencia que permita distinguir particulares de intermediarios. Tampoco hay fecha de publicación: el ID del enlace es solo un proxy de recencia.
- El anuncio de $180,000 está clasificado como «Inmueble» porque su título no especifica «Casa»; no se reclasifica sin evidencia textual. Ese valor atípico infla la media y la media de La Víbora.
- No se imputan precios, zonas ni operaciones. La ausencia se reporta como hallazgo, no se rellena con supuestos.

---

Informe generado por el Proyecto de Ciencia de Datos — Universidad de La Habana

Facultad de Matemática y Computación (MATCOM)

Profesor: **Yudivian Almeida Cruz**

Repositorio: `Mercado-digital-cubano-en-10-de-octubre`

