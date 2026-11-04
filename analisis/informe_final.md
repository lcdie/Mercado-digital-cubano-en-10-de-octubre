# Informe Final: Mercado Inmobiliario Digital en Diez de Octubre

Fecha de generación: 04/11/2026 07:23:06
Total de anuncios analizados: 171

## Introducción

Este informe presenta el análisis del mercado inmobiliario digital en el municipio Diez de Octubre, La Habana, basado en anuncios publicados en la plataforma digital Revolico. Los datos han sido recopilados, limpiados y analizados para responder a 30 preguntas de investigación organizadas en 6 bloques temáticos.

## Metodología

- Los datos provienen de anuncios publicados en Revolico, portal de clasificados en línea de Cuba.
- Se ha realizado un proceso de limpieza para eliminar anuncios con precios imposibles, municipios incorrectos, títulos sin información y anuncios no inmobiliarios.
- Se han aplicado filtros de percentiles (P10-P90) para excluir valores atípicos en el análisis de precios.
- La clasificación de tipos de inmueble, zonas y características físicas se ha realizado mediante análisis de texto en los títulos de los anuncios.

## Las 30 preguntas y sus respuestas

### Bloque A: Precios del mercado

1. ¿Cuál es el precio promedio de venta en USD en Diez de Octubre?
   > Respuesta: $22,880.00 USD (basado en 50 anuncios de venta con precio declarado)

2. ¿Cuál es el precio mediano de alquiler en USD?
   > Respuesta: No hay datos suficientes (solo hay 1 anuncio de alquiler con precio en USD).

3. ¿Cuál es el rango de precios que cubre el 80% de los anuncios de venta?
   > Respuesta: Entre $7,000.00 y $45,000.00 USD (percentiles 10 y 90)

4. ¿Cuál es el anuncio de venta más caro y el más barato publicado?
   > Anuncio más caro: $70,000 USD
   > Anuncio más barato: $1,000 USD

5. ¿Qué proporción de anuncios no declara precio?
   > Respuesta: 19.88% (34 de 171 anuncios)

6. ¿Existe diferencia significativa entre el precio promedio de venta y el de alquiler?
   > Respuesta: No hay datos suficientes para comparar (solo hay 1 anuncio de alquiler con precio en USD).

### Bloque B: Tipos de inmueble

7. ¿Cuáles son los tipos de inmueble más publicados?
   > Casa: 81 anuncios
   > Apartamento: 49 anuncios
   > Inmueble: 37 anuncios
   > Cuarto: 2 anuncios
   > Local: 2 anuncios

8. ¿Qué porcentaje son casas independientes frente a apartamentos?
   > Respuesta: No hay datos suficientes (menos de 10 anuncios con tipo claro).

9. ¿Cuál es el precio promedio de venta por tipo de inmueble?
   > Cuarto: datos insuficientes (n=1)
   > Local: datos insuficientes (n=1)
   > Inmueble: $40,500.00 USD (n=26)
   > Casa: $36,626.47 USD (n=68)
   > Apartamento: $19,425.00 USD (n=40)

10. ¿Qué tipo de inmueble concentra el precio máximo declarado?
   > Respuesta: Inmueble con $180,000 USD

11. ¿Cuántos anuncios son de venta frente a cuántos son de alquiler?
   > Venta: 56 anuncios
   > Alquiler: 22 anuncios

12. ¿Qué tipo de inmueble domina en las zonas con precios más altos?
   > Zona con precio promedio más alto: Calzada 10 de Octubre ($75,000.00 USD, 1 anuncios)
   > Tipo de inmueble dominante en esa zona: Inmueble

### Bloque C: Características físicas

13. ¿Cuál es la cantidad más común de cuartos/habitaciones?
   > Respuesta: 3 cuartos (8 anuncios)

14. ¿Cómo varía el precio según el número de cuartos?
   > 2 cuarto(s): $22,400.00 USD (n=5)
   > 3 cuarto(s): $37,166.67 USD (n=6)

15. ¿Qué porcentaje de anuncios menciona garaje y cómo afecta al precio?
   > 8 de 171 anuncios (4.7%) mencionan garaje.
   > Precio promedio con garaje: $43,375.00 USD
   > Precio promedio sin garaje: $32,020.31 USD
   > Diferencia: $11,354.69 USD (las casas con garaje valen más en promedio)

16. ¿Cuántos anuncios especifican 'planta baja' y cuál es su precio promedio?
   > [{'titulo': '🏡 SE VENDE O SE PERMUTA APARTAMENTO EN PLANTA BAJA, SEVILLANO, 10 DE OCTUBRE.', 'precio': 12000, 'moneda': 'USD', 'municipio': '10 de Octubre', 'enlace': 'https://www.revolico.com/item/se-vende-o-se-permuta-apartamento-en-planta-baja-sevillano-10-de-octubre-55911834', 'permuta': True, 'estado': 'activo', 'motivo_estado': 'Activo', 'fecha_verificacion': '2026-10-31 15:56:58'}, {'titulo': '70,000 USD Económica  Casa en bajos de Biplanta en Zona Residencial de Atavey', 'precio': 70000, 'moneda': 'USD', 'municipio': 'Diez de Octubre', 'enlace': 'https://www.revolico.com/item/economica-casa-en-zona-residencial-de-atavey-57459566', 'permuta': False, 'id_anuncio': 57459566, 'fuente': 'nuevo_scraping', 'fecha_agregado': '2026-10-31', 'estado': 'activo', 'motivo_estado': 'Nuevo anuncio', 'fecha_verificacion': '2026-10-31 15:59:41'}, {'titulo': '35,000 USD 🏡 ¡FRENTE AL MAR EN EL NÁUTICO! Casa en Bajos (2 Hab) 🌊', 'precio': 35000, 'moneda': 'USD', 'municipio': 'Diez de Octubre', 'enlace': 'https://www.revolico.com/item/frente-al-mar-en-el-nautico-casa-en-bajos-2-hab-listo-para-vivir-confort-y-autonomia-total-55991777', 'permuta': False, 'id_anuncio': 55991777, 'fuente': 'nuevo_scraping', 'fecha_agregado': '2026-10-31', 'estado': 'activo', 'motivo_estado': 'Nuevo anuncio', 'fecha_verificacion': '2026-10-31 15:59:41'}, {'titulo': '19,500 USD 🏢 APARTAMENTO PUERTA DE CALLE, PLANTA BAJA – LA VÍBORA 🏢', 'precio': 19500, 'moneda': 'USD', 'municipio': 'Diez de Octubre', 'enlace': 'https://www.revolico.com/item/apartamento-puerta-de-calle-planta-baja-la-vibora-58361077', 'permuta': False, 'id_anuncio': 58361077, 'fuente': 'nuevo_scraping', 'fecha_agregado': '2026-10-31', 'estado': 'activo', 'motivo_estado': 'Nuevo anuncio', 'fecha_verificacion': '2026-10-31 15:59:41'}, {'titulo': '30,000 USD Oportunidad en Santo Suárez.  En venta amplio biplanta en bajos del año 1940, con 84,51 m² y excelente ubicación !!!', 'precio': 30000, 'moneda': 'USD', 'municipio': 'Diez de Octubre', 'enlace': 'https://www.revolico.com/item/oportunidad-en-santo-suarez-en-venta-amplio-biplanta-en-bajos-del-ano-1940-con-8451-m2-y-excelente-ubicacion-52642522', 'permuta': False, 'id_anuncio': 52642522, 'fuente': 'nuevo_scraping', 'fecha_agregado': '2026-10-31', 'estado': 'activo', 'motivo_estado': 'Nuevo anuncio', 'fecha_verificacion': '2026-10-31 15:59:46'}, {'titulo': '35,000 USD En venta biplanta en bajos con 4 cuartos y garaje en Casino Deportivo !!!', 'precio': 35000, 'moneda': 'USD', 'municipio': 'Diez de Octubre', 'enlace': 'https://www.revolico.com/item/en-venta-biplanta-en-bajos-con-4-cuartos-y-garaje-en-casino-deportivo-57728706', 'permuta': False, 'id_anuncio': 57728706, 'fuente': 'nuevo_scraping', 'fecha_agregado': '2026-10-31', 'estado': 'activo', 'motivo_estado': 'Nuevo anuncio', 'fecha_verificacion': '2026-10-31 15:59:46'}, {'titulo': '50,000 USD JOYA CAPITALISTA EN BAJOS: IDEAL PARA NEGOCIO O VIVIENDA ( Cercana a ZAPATA E INFANTA)', 'precio': 50000, 'moneda': 'USD', 'municipio': 'Diez de Octubre', 'enlace': 'https://www.revolico.com/item/joya-capitalista-en-bajos-ideal-para-negocio-o-vivienda-cercana-a-zapata-e-infanta-53110209', 'permuta': False, 'id_anuncio': 53110209, 'fuente': 'nuevo_scraping', 'fecha_agregado': '2026-10-31', 'estado': 'activo', 'motivo_estado': 'Nuevo anuncio', 'fecha_verificacion': '2026-10-31 15:59:46'}, {'titulo': '13,500 USD Casa en luyano planta baja placa ocupada', 'precio': 13500, 'moneda': 'USD', 'municipio': 'Diez de Octubre', 'enlace': 'https://www.revolico.com/item/casa-en-luyano-planta-baja-placa-ocupada-56798447', 'permuta': False, 'id_anuncio': 56798447, 'fuente': 'nuevo_scraping', 'fecha_agregado': '2026-10-31', 'estado': 'activo', 'motivo_estado': 'Nuevo anuncio', 'fecha_verificacion': '2026-10-31 16:00:05'}] anuncios especifican planta baja (8 con precio declarado).
   > Precio promedio: $33,125.00 USD

17. ¿Qué porcentaje menciona metraje (m²) y cuál es el promedio?
   > [{'titulo': '🔴Casa Grande para Almacén 240m²📦', 'precio': 80000, 'moneda': 'USD', 'municipio': '10 de Octubre', 'enlace': 'https://www.revolico.com/item/casa-grande-para-almacen-240m2-56416044', 'permuta': False, 'estado': 'activo', 'motivo_estado': 'Activo', 'fecha_verificacion': '2026-10-31 15:51:11'}, {'titulo': 'Se vende apartamento capitalista en la Víbora 92m2 cerca del Palacio de los matrimonios y matias Rodríguez', 'precio': 25000, 'moneda': 'USD', 'municipio': '10 de Octubre', 'enlace': 'https://www.revolico.com/item/se-vende-apartamento-capitalista-en-la-vibora-92m2-cerca-del-palacio-de-los-matrimonios-y-matias-rodriguez-58325911', 'permuta': False, 'estado': 'activo', 'motivo_estado': 'Activo', 'fecha_verificacion': '2026-10-31 15:55:57'}, {'titulo': '30,000 USD Oportunidad en Santo Suárez.  En venta amplio biplanta en bajos del año 1940, con 84,51 m² y excelente ubicación !!!', 'precio': 30000, 'moneda': 'USD', 'municipio': 'Diez de Octubre', 'enlace': 'https://www.revolico.com/item/oportunidad-en-santo-suarez-en-venta-amplio-biplanta-en-bajos-del-ano-1940-con-8451-m2-y-excelente-ubicacion-52642522', 'permuta': False, 'id_anuncio': 52642522, 'fuente': 'nuevo_scraping', 'fecha_agregado': '2026-10-31', 'estado': 'activo', 'motivo_estado': 'Nuevo anuncio', 'fecha_verificacion': '2026-10-31 15:59:46'}] de 171 anuncios (1.8%) mencionan metraje.
   > Precio promedio: $45,000.00 USD (n=3)

18. ¿Qué características físicas se mencionan con más frecuencia?
   > Garaje: 8 anuncios
   > Cuarto: 6 anuncios
   > Baño: 3 anuncios
   > Terraza: 2 anuncios
   > Balcón: 1 anuncios
   > Azotea: 1 anuncios
   > Sala: 1 anuncios
   > Patio: 1 anuncios

### Bloque D: Ubicación dentro de Diez de Octubre

19. ¿Qué zonas o barrios aparecen con más frecuencia en los anuncios?
   > Santos Suárez: 14 anuncios
   > Lawton: 11 anuncios
   > La Víbora: 9 anuncios
   > El Sevillano: 8 anuncios
   > Diez de Octubre: 6 anuncios
   > El Mónaco: 5 anuncios
   > Luyano: 4 anuncios
   > Santa Catalina: 1 anuncios
   > Vía Blanca: 1 anuncios
   > Calzada 10 de Octubre: 1 anuncios

20. ¿Qué zona tiene el precio promedio de venta más alto?
   > Respuesta: La Víbora con $52,277.78 USD promedio (9 anuncios)

21. ¿Qué zona tiene la mayor cantidad de anuncios publicados?
   > Respuesta: Santos Suárez con 14 anuncios

22. ¿Hay diferencia de precios entre zonas dentro del mismo municipio?
   > Respuesta: Sí. La zona más cara es La Víbora ($52,277.78 USD) y la más barata es Luyano ($22,125.00 USD). Diferencia: $30,152.78 USD.

23. ¿Qué zonas aparecen solo en venta o solo en alquiler?
   > Zonas solo en venta (6): El Mónaco, La Víbora, Lawton, Luyano, Santos Suárez, Vía Blanca
   > Zonas solo en alquiler (0): Ninguna
   > Zonas en ambas categorías (2): Diez de Octubre, El Sevillano

24. ¿Cuántos anuncios no especifican zona dentro del municipio?
   > Respuesta: 111 de 171 anuncios (64.9%) no especifican zona dentro de Diez de Octubre.

### Bloque E: Moneda y mercado informal

25. ¿Qué proporción de anuncios declara precios en USD frente a CUP?
   > USD: 136 anuncios (99.3%)
   > CUP: 1 anuncios (0.7%)

26. ¿Cuál es el precio promedio de los anuncios declarados en CUP?
   > Respuesta: No hay datos suficientes (solo 1 anuncio con precio en CUP).

27. ¿Qué porcentaje de anuncios incluye palabras como 'oportunidad', 'ganga' o 'permuta'?
   > 15 de 171 anuncios (8.8%) incluyen palabras de mercado informal.
      - Oportunidad: 12 menciones
      - Permuta: 2 menciones
      - Cambio: 1 menciones

28. ¿Qué rango de precios es más frecuente para ventas en USD?
   > Respuesta: El rango 10,000 - 20,000 es el más frecuente con 21 anuncios (42.0% de los anuncios de venta con precio USD).

   Distribución completa:
      10,000 - 20,000: 21 anuncios (42.0%)
      0 - 10,000: 8 anuncios (16.0%)
      30,000 - 40,000: 7 anuncios (14.0%)
      20,000 - 30,000: 6 anuncios (12.0%)
      40,000 - 50,000: 4 anuncios (8.0%)
      60,000 - 70,000: 2 anuncios (4.0%)
      70,000 - 80,000: 2 anuncios (4.0%)

29. ¿Cuántos anuncios parecen ser de particulares frente a posibles anuncios repetidos o agencias (por lenguaje o título)?
   > Total de títulos únicos: 171
   > Anuncios con título único (probables particulares): 171
   > Anuncios con título repetido (posibles agencias o anuncios duplicados): 0 anuncios en 0 títulos repetidos


30. ¿Qué recomendación práctica se puede hacer a alguien que quiera comprar o alquilar en Diez de Octubre según estos datos?

   > Respuesta: Basado en el análisis de los datos del mercado inmobiliario digital en Diez de Octubre:

   1. **Precios razonables**: El precio promedio de venta en USD es de $32,688.24, con una mediana de $24,000 USD. El rango más común de precios se encuentra entre $10,000 y $30,000 USD, que representa más del 50% de los anuncios.

   2. **Zonas más activas**: Santos Suárez, La Víbora, Lawton y Luyano son las zonas con mayor cantidad de anuncios publicados, lo que indica una oferta más variada en estas áreas.

   3. **Precios por zona**: Hay diferencias significativas de precios entre zonas dentro del mismo municipio. Se recomienda investigar específicamente la zona de interés antes de tomar una decisión.

   4. **Moneda**: La gran mayoría de los anuncios (97.6%) se declaran en USD, por lo que se recomienda contar con esta moneda para realizar transacciones inmobiliarias en el área.

   5. **Permuta**: El mercado de permutas está presente en el mercado (8 anuncios), lo que puede ser una opción para quienes no cuentan con efectivo completo.

   6. **Precaución**: Dado que muchos anuncios no declaran precio (24.1%) y algunos títulos son genéricos, se recomienda verificar directamente con el vendedor antes de realizar cualquier gestión.

   7. **Análisis por zona**: Se recomienda enfocarse en zonas específicas según el presupuesto disponible, ya que existen diferencias de precios entre zonas dentro del mismo municipio.

## Conclusiones

1. El mercado inmobiliario digital en Diez de Octubre está dominado por anuncios en USD, lo que refleja la dollarización del mercado inmobiliario en Cuba.

2. Las casas independientes son el tipo de inmueble más publicado, seguidas por los apartamentos, lo que sugiere una preferencia por viviendas unifamiliares en el área.

3. Santos Suárez, La Víbora, Lawton y Luyano son las zonas con mayor cantidad de anuncios publicados, lo que indica una mayor oferta en estas áreas.

4. Existen diferencias de precios entre zonas dentro del mismo municipio, por lo que es importante investigar específicamente la zona de interés.

5. El mercado de permutas está presente y representa una alternativa para quienes no cuentan con efectivo completo.

6. Muchos anuncios no declaran precio, lo que dificulta el análisis del mercado y requiere contacto directo con el vendedor.

7. El rango de precios más frecuente para ventas en USD está entre $10,000 y $30,000, que representa más del 50% de los anuncios.

8. El promedio de precios en el rango P10-P90 (excluyendo valores atípicos) es de $28,131.82 USD, con una mediana de $24,000 USD.

## Limitaciones

- Los datos provienen únicamente de anuncios publicados en un portal digital (Revolico), no representan la totalidad del mercado físico.
- Muchos anuncios no declaran precio ni ubicación específica dentro del municipio.
- La detección de municipio y zona se basa en palabras clave presentes en el título y el enlace del anuncio, lo que puede generar falsos positivos.
- La muestra es limitada (171 anuncios limpios) y puede no ser representativa del mercado completo.

---
Informe generado automáticamente por el Proyecto de Ciencia de Datos - Universidad de La Habana
Facultad de Matemática y Computación (MATCOM)
Profesor: Yudivian Almeida Cruz

---
