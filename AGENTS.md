# AGENTS.md — Invariantes del pipeline (Mercado inmobiliario digital en Diez de Octubre)

**Proyecto:** Ciencia de Datos, Universidad de La Habana (MATCOM)  
**Tema:** opacidad, dolarización, desigualdad territorial e informalidad del mercado inmobiliario digital de Diez de Octubre  
**Universo canónico:** 122 publicaciones confirmadas (83 Revolico + 39 Facebook)

---

## Reglas invariantes (no modificar sin revisar el informe)

1. **El título manda.** Si el título nombra un lugar externo a Diez de Octubre, el registro se descarta (`NO`). Si nombra Diez de Octubre o un reparto interno, se confirma (`SÍ`). Solo si el título no aporta señal se usa la ficha, el enlace, el grupo, la ubicación o la zona.
2. **No se elimina información.** Los 55 registros no incluidos se conservan íntegros en `datos/limpios/descartados_diez_octubre.json` y `.csv`, con motivo, evidencia, `registro_original` y `registro_unificado` exacto.
3. **El universo es 122.** 134 es la base histórica etiquetada (no verificada) y se conserva solo como referencia histórica. No son comparables.
4. **No se imputan valores ausentes.** Precio, zona, operación, habitaciones, baños y superficie ausentes se reportan como opacidad, nunca se rellenan.
5. **Orden de ejecución:** verificación municipal → informe A-F → PDF. El informe lee `datos/limpios/unificado_confirmados_diez_octubre.json` y se queda solo con `resultado == "SÍ"`.
6. **No añadir fuentes ajenas.** No se incorporan Cubisima, HogarEnCuba, entrevistas ni tasas de cambio. Ese es el alcance del repositorio de referencia, no el tema propio.
7. **No cambiar el universo a última hora.** Mantener 122 confirmados y 55 descartes sin alterar registros.

---

## Pipeline (4 pasos)

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

Para regenerar el PDF:

```bash
.venv-docs/bin/python scripts/generar_pdf_informe.py
```

---

## Archivos clave

| Ruta | Propósito |
|---|---|
| `datos/limpios/unificado_confirmados_diez_octubre.json` | Base final de 122 confirmados |
| `datos/limpios/descartados_diez_octubre.json` / `.csv` | 55 descartes íntegros con motivo |
| `scripts/verificar_municipio_publicaciones.py` | Verificación título-primero y generación de bases |
| `scripts/analisis_final_30_preguntas.py` | Generador del informe A-F |
| `scripts/cifras_control.py` | 36 cifras de control (solo lectura) |
| `tests/test_verificacion.py` | 8 pruebas de contrato |
| `data_dictionary.md` | Diccionario de datos y convenciones de nulos |
| `bitacora_cambios.md` | Historia 134 → 122 y decisiones manuales |
| `analisis/informe_final.md` / `.pdf` | Informe final A-F |
| `requeriments.txt` | Dependencias (versiones fijadas donde sea posible) |

---

## Pendientes operativos

- **Push a origin:** pendiente. Credenciales de GitHub no configuradas, `gh` no instalado, token expuesto anteriormente no reutilizable. Resolver con SSH o PAT nuevo antes de publicar.
- **Versiones fijadas:** `requirements.txt` usa `==` para los paquetes instalados; `seaborn` y los de documentación quedan con `>=` porque no se pudo congelar su versión exacta en este entorno.
