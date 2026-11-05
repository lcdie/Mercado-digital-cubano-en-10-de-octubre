#!/usr/bin/env bash
# run_all.sh — Pipeline completo del proyecto Mercado digital cubano en Diez de Octubre
#
# Ejecuta los 4 pasos en orden:
#   1. Verificación municipal (título primero + polígono + geocodificación)
#   2. Informe A-F (30 preguntas sobre las 122 confirmadas)
#   3. Control de cifras (valida 36 cifras contra los datos generados)
#   4. Pruebas de contrato (8 pruebas, sin red)
#
# Opcional: regenera el PDF del informe al finalizar.

set -euo pipefail

RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$RAIZ"

echo "==> Paso 1: Verificación municipal"
python3 scripts/verificar_municipio_publicaciones.py

echo "==> Paso 2: Informe A-F (30 preguntas)"
python3 scripts/analisis_final_30_preguntas.py

echo "==> Paso 3: Control de cifras"
python3 scripts/cifras_control.py

echo "==> Paso 4: Pruebas de contrato"
python3 -m unittest discover -s tests -t .

echo "==> Paso opcional: generar gráficas de exposición"
python3 graficos/generar_graficas.py

echo "==> Paso opcional: regenerar PDF"
if [ -x .venv-docs/bin/python ]; then
  .venv-docs/bin/python scripts/generar_pdf_informe.py
else
  echo "Aviso: .venv-docs/bin/python no encontrado, se omite el PDF"
fi

echo "==> Pipeline completo finalizado"
