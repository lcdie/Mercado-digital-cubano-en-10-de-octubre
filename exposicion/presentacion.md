# Mercado Inmobiliario Digital en Diez de Octubre
**Ciencia de Datos — MATCOM, Universidad de La Habana**  
Profesor: Yudivian Almeida Cruz  
Fecha: Noviembre de 2026

---

## 1. Problema social
¿Cuánto cuesta realmente vivir en Diez de Octubre?

- Opacidad de la información
- Dolarización de los precios
- Desigualdad entre barrios
- Prácticas informales

---

## 2. Fuente y base de datos
- **Revolico:** 83 publicaciones confirmadas (corte 2026-10-31)
- **Facebook:** 39 publicaciones confirmadas (captura 2026-11-04)
- **Total verificado:** 122 publicaciones dentro del municipio
- **Descartados:** 55 registros conservados íntegros con motivo

---

## 3. Verificación municipal
- Regla de título primero: el título decide; ficha y texto son respaldo
- Polígono municipal DPA 23.09 + geocodificación Nominatim
- 46 anuncios de otro municipio excluidos
- 8 indeterminadas excluidas
- 0 contradictorios

---

## 4. Precios de compra (ventas en USD)
![Gráfica 1](graficos/grafico_1_precios_venta_usd.png)

- **Mediana:** $20.000 USD
- **Media:** $26.023 USD
- **P10–P90:** $6.200 – $60.000 USD
- La media sobreestima el precio típico por valores extremos

---

## 5. Desigualdad territorial
![Gráfica 2](graficos/grafico_2_oferta_por_zona.png)

- Top-4 zonas concentran 75,8% de la oferta con zona identificada
- Santos Suárez y Lawton lideran en cantidad de anuncios

---

## 6. Media vs Mediana por zona
![Gráfica 3](graficos/grafico_3_media_mediana_zona.png)

- La Víbora: media más alta (n = 11) — valores extremos inflan el promedio
- El Sevillano: mediana más alta (n = 10)
- Usar mediana para comparar barrios

---

## 7. Dolarización
![Gráfica 4](graficos/grafico_4_moneda.png)

- 86,9% del universo declara USD
- 1 precio en CUP (alquiler, no convertido)
- 15 publicaciones (12,3%) sin precio

---

## 8. Opacidad de la información
![Gráfica 5](graficos/grafico_5_opacidad.png)

- 67,2% tiene precio y zona
- 25,4% sin zona
- 12,3% sin precio
- 4,9% sin ninguno de los dos
- La ausencia de información es un hallazgo, no un defecto

---

## 9. Tipos de inmueble
- Casa: 57 anuncios, mediana $33.000 USD
- Apartamento: 33 anuncios, mediana $15.000 USD
- El apartamento es la opción más accesible

---

## 10. Limitaciones
- Muestra no probabilística (122 publicaciones)
- Precios de oferta, no de transacción
- Sin serie temporal (corte único)
- No hay datos homogéneos de m², habitaciones, baños
- Alquiler no estimable (3 publicaciones, ninguna en USD)

---

## 11. Conclusiones
1. Mercado altamente dolarizado: barrera de acceso estructural
2. Precio mediano ($20.000) muy inferior a la media ($26.023)
3. Alquiler no estimable con esta base
4. Desigualdad territorial real: usar mediana, no media
5. Opacidad importante: 1 de cada 4 anuncios no declara zona

---

## 12. Preguntas
Espacio para Q&A
