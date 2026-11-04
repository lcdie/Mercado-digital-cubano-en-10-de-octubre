# Informe Final: Mercado Inmobiliario Digital en Diez de Octubre

**Fecha de generación:** 04/11/2026 08:22
**Universo analizado:** 171 anuncios limpios de Revolico
**Anuncios con precio en USD:** 136

## Introducción

Este informe analiza el mercado inmobiliario digital del municipio Diez de Octubre, La Habana, a partir de anuncios publicados en Revolico. Se responden 30 preguntas de investigación organizadas en cinco bloques temáticos (A–E). Las preguntas cuyas respuestas no alcanzaban una base mínima de datos fueron sustituidas por preguntas alternativas respondibles con la información disponible.

## Metodología

- Se trabajó con 171 anuncios previamente limpiados: solo Diez de Octubre y precio mínimo de 1,000 USD cuando existe precio.
- Los análisis de precio usan los 136 anuncios con precio declarado en USD; se excluye 1 anuncio en CUP y 34 sin precio.
- Para reducir el efecto de valores extremos se reporta el rango P10–P90 y la mediana junto a la media.
- Cada respuesta indica su tamaño de muestra (n). Los subgrupos con n < 10 se presentan como evidencia descriptiva, no como conclusión firme.
- La clasificación de tipo, zona y características se infiere de palabras clave del título y del enlace.

## Fuente y universo de datos

- **Revolico (fuente principal):** 171 anuncios limpios del municipio Diez de Octubre. Es la única fuente usada en los cálculos de este informe.
- **Anuario Estadístico de Cuba (ONEI):** se consulta como contexto general del municipio; no se usa para calcular precios ni proporciones de la muestra digital.
- **Facebook (fuente explorada, no integrada):** se revisaron 37 publicaciones de grupos de compraventa. Se excluyeron del análisis cuantitativo porque no comparten el esquema de campos de Revolico (precio anidado, ubicación en texto libre y sin municipio normalizado) y no permiten aplicar el mismo filtro municipal y de limpieza. Incorporarlas sin normalizar habría mezclado universos distintos. Se conservan en `datos/limpios/datos_unificados_facebook_revolico.json` para una ampliación futura.

## Preguntas sustituidas

Cinco preguntas del cuestionario original no podían responderse con una base mínima de datos. Se sustituyeron por preguntas equivalentes y respondibles:

| # | Pregunta original | Motivo de la sustitución | Pregunta nueva |
|---|---|---|---|
| 2 | ¿Cuál es la mediana del precio de alquiler? | Solo 2 anuncios de alquiler declaran precio (1 USD y 1 CUP). | ¿Cuál es el precio mediano de los anuncios con precio en USD? |
| 6 | ¿Es más caro comprar que alquilar? | Solo 1 alquiler tiene precio en USD; no hay base para comparar. | ¿Qué tan dispersos son los precios respecto a la media? |
| 17 | ¿Cuál es el precio promedio por metro cuadrado? | Solo 3 anuncios mencionan metraje. | ¿Qué proporción de anuncios incluye al menos una característica física explícita? |
| 23 | ¿Qué zonas concentran más anuncios de venta y de alquiler? | Solo una zona tiene algún anuncio de alquiler. | ¿Qué proporción de los anuncios con zona identificada se concentra en las cuatro zonas principales? |
| 26 | ¿Cuál es el precio promedio en CUP? | Solo 1 anuncio declara precio en CUP. | ¿Los anuncios con lenguaje informal declaran precio con más frecuencia que los neutros? |

Además de esas cinco sustituciones, la **Q1** se reformuló de «precio promedio de venta» a «precio promedio de los anuncios con precio declarado en USD», porque solo 50 anuncios se identifican explícitamente como venta. Por la misma razón, **Q20** y **Q28** se expresan sobre anuncios con precio en USD. Cuando aporta información, se reporta por separado el subconjunto de ventas explícitas (Q1, Q2 y Q11).

## Las 30 preguntas y sus respuestas

### Bloque A: Precios del mercado

**1. ¿Cuál es el precio promedio de los anuncios con precio declarado en USD en Diez de Octubre?**

> **$32,688.24 USD** (n = 136). Si se excluyen los valores extremos y se calcula sobre el tramo P10–P90, el promedio baja a **$28,131.82 USD** (n = 110). Si se restringe a los 50 anuncios que se identifican explícitamente como venta, el promedio es **$22,880.00 USD**.

**2. ¿Cuál es el precio mediano de los anuncios con precio declarado en USD?**

> **$24,000.00 USD** (n = 136). La mediana es menor que la media porque unos pocos anuncios muy caros elevan el promedio. En el subconjunto de ventas explícitas, la mediana es **$17,000.00 USD** (n = 50).

**3. ¿Cuál es el rango de precios que cubre el 80% central de los anuncios?**

> Entre **$8,000.00 USD** (P10) y **$70,000.00 USD** (P90). Dentro de ese tramo se concentran **110 de 136 anuncios (80.9%)**.

**4. ¿Cuáles son el anuncio más caro y el más barato publicados?**

> Más caro: **$180,000.00 USD**. Más barato: **$1,000.00 USD**.

**5. ¿Qué proporción de anuncios no declara precio?**

> **34 de 171 anuncios (19.88%)** no declaran precio. Esto obliga a contactar al vendedor para conocerlo.

**6. ¿Qué tan dispersos son los precios respecto a la media?**

> La media ($32,688.24) supera a la mediana ($24,000.00) en **$8,688.24**, un 36.2% de la mediana. Además, **26 anuncios (19.1%)** quedan fuera del tramo P10–P90. La distribución está sesgada a la derecha: hay una minoría de inmuebles de lujo que infla el promedio.

### Bloque B: Tipos de inmueble

**7. ¿Cuáles son los tipos de inmueble más publicados?**

> - Casa: **81 anuncios** (47.4%)
> - Apartamento: **49 anuncios** (28.7%)
> - Inmueble: **37 anuncios** (21.6%)
> - Cuarto: **2 anuncios** (1.2%)
> - Local: **2 anuncios** (1.2%)

**8. ¿Qué porcentaje son casas independientes frente a apartamentos?**

> Casas: **81 (62.3%)**. Apartamentos: **49 (37.7%)** (n = 130 anuncios con tipo identificable entre ambos).

**9. ¿Cuál es el precio promedio por tipo de inmueble (anuncios con precio en USD)?**

> - Inmueble: **$40,500.00 USD** (n = 26)
> - Casa: **$36,626.47 USD** (n = 68)
> - Apartamento: **$19,425.00 USD** (n = 40)
> 
> Se excluyen los tipos con menos de 5 anuncios con precio: Cuarto (1), Local (1).

**10. ¿Qué tipo de inmueble concentra el precio máximo declarado?**

> **Inmueble**, la categoría que agrupa los títulos que no especifican un tipo, con el anuncio «180,000 USD Cada en la víbora 10 octubre» a **$180,000.00 USD**. Es un valor atípico: el segundo precio más alto es **$120,000.00 USD**.

**11. ¿Cuántos anuncios se identifican como venta, alquiler o sin clasificar?**

> Venta: **56 anuncios (32.7%)**. Alquiler: **22 (12.9%)**. Sin clasificar por título: **93 (54.4%)**. De los 22 alquileres, solo 1 declara precio en USD y 1 en CUP; por eso no se puede comparar estadísticamente el precio de alquiler con el de venta.

**12. ¿Qué tipo de inmueble domina en la zona con el precio promedio más alto?**

> Entre las zonas con al menos 5 anuncios con precio, **La Víbora** tiene el promedio más alto: **$52,277.78 USD** (n = 9). El tipo dominante es **Apartamento** (6 de 9 anuncios con precio).

### Bloque C: Características físicas

**13. ¿Cuál es la cantidad más común de cuartos/habitaciones?**

> **3 cuartos**, presente en **8 de 19 anuncios** que especifican el dato (42.1%).

**14. ¿Cómo varía el precio según el número de cuartos?**

> - 2 cuartos: **$22,400.00 USD** (n = 5)
> - 3 cuartos: **$37,166.67 USD** (n = 6)
> 
> Los anuncios de 2 y 3 cuartos son los únicos subgrupos con al menos 5 casos. El precio promedio sube de 2 a 3 cuartos en **$14,766.67 USD**.

**15. ¿Qué porcentaje de anuncios menciona garaje y cómo se relaciona con el precio?**

> **8 de 171 anuncios (4.7%)** mencionan garaje. Entre los que declaran precio en USD, el promedio con garaje es **$43,375.00 USD** (n = 8) frente a **$32,020.31 USD** sin garaje (n = 128): una diferencia de **$11,354.69 USD** (35.5% más). El subgrupo con garaje es pequeño (n = 8), así que la diferencia es indicativa, no concluyente.

**16. ¿Cuántos anuncios especifican 'planta baja' y cuál es su precio promedio?**

> **8 anuncios (4.7%)** mencionan planta baja o bajos; los **8** con precio en USD promedian **$33,125.00 USD**. Es un grupo pequeño (n = 8), por lo que solo describe una tendencia.

**17. ¿Qué proporción de anuncios incluye al menos una característica física explícita?**

> **24 de 171 anuncios (14.0%)** mencionan al menos una característica física (garaje, patio, azotea, terraza, balcón, baño, cuartos o habitaciones). De ellos, **20** declaran precio en USD.

**18. ¿Qué características físicas se mencionan con más frecuencia?**

> - Garaje: **8 anuncios**
> - Cuarto: **6 anuncios**
> - Baño: **3 anuncios**
> - Terraza: **2 anuncios**
> - Balcón: **1 anuncio**
> - Azotea: **1 anuncio**
> - Sala: **1 anuncio**
> - Patio: **1 anuncio**

### Bloque D: Ubicación dentro de Diez de Octubre

**19. ¿Qué zonas o barrios aparecen con más frecuencia en los anuncios?**

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
> **117 de 171 anuncios (68.4%)** no especifican zona en el título.

**20. ¿Qué zona tiene el precio promedio más alto entre los anuncios con precio en USD?**

> Entre las zonas con al menos 5 anuncios con precio, **La Víbora** tiene el promedio más alto: **$52,277.78 USD** (n = 9). Si se exige n ≥ 10, la más cara es **Santos Suárez** ($25,923.08 USD, n = 13).

**21. ¿Qué zona tiene la mayor cantidad de anuncios publicados?**

> **Santos Suárez**, con **14 anuncios** (13 de ellos con precio en USD).

**22. ¿Hay diferencia de precios entre zonas dentro del mismo municipio?**

> Sí. Entre las zonas con al menos 5 anuncios con precio, **La Víbora** promedia **$52,277.78 USD** (n = 9) y **Lawton** promedia **$23,600.00 USD** (n = 10): una diferencia de **$28,677.78 USD**. Si se comparan solo zonas con n ≥ 10, la diferencia entre Santos Suárez y Lawton es de **$2,323.08 USD**.

**23. ¿Qué proporción de los anuncios con zona identificada se concentra en las cuatro zonas principales?**

> Las cuatro zonas principales —Santos Suárez, Lawton, La Víbora, El Sevillano— reúnen **42 de 54 anuncios con zona identificada (77.8%)**. La oferta está, por tanto, muy concentrada en pocos barrios.

**24. ¿Cuántos anuncios no especifican zona dentro del municipio?**

> **117 de 171 anuncios (68.4%)** no especifican zona en el título ni en el enlace.

### Bloque E: Moneda y mercado informal

**25. ¿Qué proporción de anuncios con moneda declarada usa USD frente a CUP?**

> USD: **136 de 137 (99.3%)**. CUP: **1 de 137 (0.7%)**. Además, 34 anuncios no declaran precio ni moneda. En el total del universo, el USD aparece en **79.5%** de los anuncios.

**26. ¿Los anuncios con lenguaje informal declaran precio con más frecuencia que los anuncios con lenguaje neutro?**

> Sí. Entre los **15 anuncios** con palabras como 'oportunidad', 'ganga', 'permuta', 'intercambio' o 'cambio', **14 (93.3%)** declaran precio. Entre los **156 anuncios** con lenguaje neutro, lo hacen **123 (78.8%)**. La diferencia es de **14.5 puntos porcentuales**.

**27. ¿Qué porcentaje de anuncios incluye palabras de mercado informal?**

> **15 de 171 anuncios (8.8%)**. Distribución: oportunidad (12), permuta (2), cambio (1).

**28. ¿Qué rango de precios es más frecuente entre los anuncios con precio en USD?**

> El rango **10,000 - 20,000 USD** es el más frecuente, con **34 anuncios (25.0% de los 136 con precio en USD)**.

> Distribución completa:
>
> - 0 - 10,000: 22 anuncios (16.2%)
> - 10,000 - 20,000: 34 anuncios (25.0%)
> - 20,000 - 30,000: 22 anuncios (16.2%)
> - 30,000 - 40,000: 18 anuncios (13.2%)
> - 40,000 - 50,000: 14 anuncios (10.3%)
> - 50,000 - 60,000: 5 anuncios (3.7%)
> - 60,000 - 70,000: 5 anuncios (3.7%)
> - 70,000 - 80,000: 7 anuncios (5.1%)
> - 80,000+: 9 anuncios (6.6%)

**29. ¿Cuántos anuncios parecen de particulares frente a posibles anuncios repetidos o agencias?**

> La base no incluye un campo de vendedor que permita distinguir particulares de agencias. Como aproximación, **171 de 171 títulos son únicos** y no hay títulos duplicados. La ausencia de duplicados exactos no muestra indicios de publicación masiva, pero tampoco descarta que una misma agencia use títulos distintos.

**30. ¿Qué recomendación práctica se puede hacer a alguien que quiera comprar o alquilar en Diez de Octubre?**

> 1. **Presupuesto:** la mediana de los anuncios con precio en USD es **$24,000.00 USD** (en ventas explícitas, **$17,000.00 USD**) y el 80% central de los precios está entre **$8,000.00 y $70,000.00 USD**. El tramo más frecuente es **10,000 - 20,000 USD** (34 anuncios, 25.0%).
> 2. **Tipo de inmueble:** un apartamento promedia **$19,425.00 USD** (n = 40) y una casa **$36,626.47 USD** (n = 68); el apartamento es la opción más económica.
> 3. **Zonas:** Santos Suárez concentra la mayor oferta (14 anuncios), seguida por Lawton (11) y La Víbora (9). El promedio más alto entre zonas con al menos 5 anuncios con precio es La Víbora (**$52,277.78 USD**, n = 9), mientras que Lawton (**$23,600.00 USD**, n = 10) es la alternativa más económica de ese grupo.
> 4. **Moneda:** el mercado está dolarizado: **136 de 137 anuncios con moneda declarada (99.3%)** usan USD. Hay que contar con divisas o verificar el tipo de cambio si se paga en CUP.
> 5. **Información incompleta:** **34 anuncios (19.9%)** no declaran precio y **117 (68.4%)** no especifican zona. Verifique siempre precio, ubicación y estado legal directamente con el vendedor.
> 6. **Precaución estadística:** los promedios por zona y por características se basan en subgrupos pequeños; úselos como orientación, no como precio de referencia definitivo.

## Conclusiones

1. El mercado está dolarizado: 136 de 137 anuncios con moneda declarada (99.3%) están en USD.
2. Los precios están sesgados a la derecha: la media ($32,688.24) supera a la mediana ($24,000.00) y 26 anuncios (19.1%) quedan fuera del tramo P10–P90.
3. Las casas son el tipo más publicado (81 anuncios, 47.4%). Entre casa y apartamento, la casa es más cara en promedio ($36,626.47 USD) que el apartamento ($19,425.00 USD).
4. La oferta se concentra en pocas zonas: las cuatro principales reúnen 77.8% de los anuncios con zona identificada.
5. Existen diferencias de precio entre zonas: La Víbora promedia $52,277.78 USD y Lawton $23,600.00 USD (zonas con al menos 5 anuncios con precio).
6. La información está incompleta: 34 anuncios (19.9%) no declaran precio y 117 (68.4%) no especifican zona.

## Limitaciones

- Los datos provienen solo de Revolico; no representan todo el mercado inmobiliario de Diez de Octubre.
- Se exploró Facebook (37 publicaciones), pero se excluyó del análisis cuantitativo porque no comparte el esquema de campos de Revolico ni un municipio normalizado; integrarla exigiría una normalización y un filtro municipal adicionales.
- La muestra es de 171 anuncios y puede no ser representativa del mercado completo.
- La clasificación de tipo, zona y características depende de palabras clave y puede contener errores.
- Los precios de alquiler no se pudieron analizar: solo 1 anuncio de alquiler declara precio en USD y 1 en CUP.
- Los subgrupos por zona, garaje, planta baja y número de cuartos tienen tamaños pequeños; sus promedios son descriptivos.

---

Informe generado por el Proyecto de Ciencia de Datos — Universidad de La Habana

Facultad de Matemática y Computación (MATCOM)

Profesor: Yudivian Almeida Cruz

