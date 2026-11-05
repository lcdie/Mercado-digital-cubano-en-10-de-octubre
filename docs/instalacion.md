# Guía de instalación y reproducción

Esta guía permite clonar el repositorio, instalar las dependencias, ejecutar el pipeline completo y verificar que las cifras del informe coincidan con los datos generados.

## Requisitos previos

- Python 3.9 o superior
- Acceso a internet para instalar dependencias (una sola vez)
- El entorno de documentación `.venv-docs` es necesario solo para regenerar el PDF

## Paso 1: Clonar el repositorio

```bash
git clone https://github.com/lcdie/Mercado-digital-cubano-en-10-de-octubre.git
cd Mercado-digital-cubano-en-10-de-octubre
```

## Paso 2: Instalar dependencias de análisis

```bash
pip install -r requirements.txt
```

Dependencias incluidas: `requests`, `beautifulsoup4`, `pandas`, `matplotlib`, `seaborn`.

Versiones fijadas con `==` para reproducibilidad.

## Paso 3: Ejecutar el pipeline completo

Desde la raíz del proyecto:

```bash
bash scripts/run_all.sh
```

El pipeline ejecuta en orden:

1. **Verificación municipal** (`scripts/verificar_municipio_publicaciones.py`): aplica la regla de título primero, comprueba el polígono municipal DPA 23.09 y genera `datos/limpios/unificado_confirmados_diez_octubre.json` (122 confirmados) y `datos/limpios/descartados_diez_octubre.json` (55 descartes íntegros).
2. **Informe A-F** (`scripts/analisis_final_30_preguntas.py`): genera `analisis/informe_final.md` con las 30 preguntas organizadas en bloques A–F.
3. **Control de cifras** (`scripts/cifras_control.py`): valida 36 cifras del informe contra los datos generados. Sale con código 0 si todo cuadra.
4. **Pruebas de contrato** (`tests/test_verificacion.py`): 8 pruebas que protegen el universo (122 confirmados, fuentes 83/39, descartes 55, integridad de registros, estadísticos de ventas, duplicado conocido).
5. **Gráficos de exposición** (`graficos/generar_graficas.py`): genera 5 PNG en `graficos/`.
6. **PDF del informe** (opcional, requiere `.venv-docs`): `.venv-docs/bin/python scripts/generar_pdf_informe.py`.

O ejecutar todo en un comando:

```bash
bash scripts/run_all.sh
```

## Paso 3 alternativo: ejecutar por pasos individuales

Si prefieres ejecutar cada paso por separado:

```bash
python3 scripts/verificar_municipio_publicaciones.py
python3 scripts/analisis_final_30_preguntas.py
python3 scripts/cifras_control.py
python3 -m unittest discover -s tests -t .
python3 graficos/generar_graficas.py
```

## Archivos que produce cada etapa

| Etapa | Script | Archivos de salida |
|---|---|---|
| Verificación municipal | `verificar_municipio_publicaciones.py` | `datos/limpios/unificado_confirmados_diez_octubre.json`, `datos/limpios/descartados_diez_octubre.json`, `datos/limpios/descartados_diez_octubre.csv` |
| Informe A-F | `analisis_final_30_preguntas.py` | `analisis/informe_final.md` |
| Control de cifras | `cifras_control.py` | Salida por consola (36 cifras verificadas) |
| Pruebas de contrato | `tests/test_verificacion.py` | Resultado de unittest (8/8 pasando) |
| Gráficos | `graficos/generar_graficas.py` | `graficos/grafico_1_*.png` a `grafico_5_*.png` |
| PDF | `generar_pdf_informe.py` | `analisis/informe_final.pdf` |

## Cómo comprobar que el resultado es correcto

1. `python3 scripts/cifras_control.py` debe imprimir `RESULTADO: 36 cifras verificadas; todas coinciden.`
2. `python3 -m unittest discover -s tests -t .` debe imprimir `Ran 8 tests` y `OK`.
3. `analisis/informe_final.md` debe existir y contener 30 preguntas (A1–F5).
4. `datos/limpios/unificado_confirmados_diez_octubre.json` debe tener 122 registros.
5. `datos/limpios/descartados_diez_octubre.json` debe tener 55 registros.

## Dependencias para documentación (PDF)

Si necesitas regenerar el PDF:

```bash
pip install -r requirements-docs.txt
.venv-docs/bin/python scripts/generar_pdf_informe.py
```

## Sin red

Las pruebas de contrato y el control de cifras no requieren acceso a internet. Solo la descarga inicial de dependencias y el scraper de Revolico (`src/scrape_revolico.py`) requieren red.
