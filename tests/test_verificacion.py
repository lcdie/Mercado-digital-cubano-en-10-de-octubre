#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pruebas de contrato del universo verificado de Diez de Octubre.

No descargan datos ni modifican archivos: comprueban las invariantes que
sostienen el informe final. Se ejecutan con:

    python3 -m unittest discover -s tests -t .
"""

import json
import sys
import unittest
from collections import Counter
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "scripts"))

from analisis_final_30_preguntas import (  # noqa: E402
    cargar_anuncios_confirmados,
    stats,
)


def cargar(ruta):
    with open(RAIZ / ruta, encoding="utf-8") as f:
        return json.load(f)


class UniversoVerificadoTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.confirmados = cargar(
            "datos/limpios/unificado_confirmados_diez_octubre.json"
        )
        cls.verificacion = cargar(
            "datos/limpios/verificacion_municipal_unificado.json"
        )
        cls.descartes = cargar(
            "datos/limpios/descartados_diez_octubre.json"
        )["registros"]
        cls.universo = {
            r["id_unico"]: r
            for r in cargar(
                "datos/limpios/datos_unificados_facebook_revolico.json"
            )
        }
        cls.anuncios, _ = cargar_anuncios_confirmados()

    def test_01_universo_confirmado_es_122(self):
        self.assertEqual(len(self.confirmados), 122)
        self.assertEqual(
            sum(1 for r in self.verificacion if r["resultado"] == "SÍ"), 122
        )

    def test_02_fuentes_83_revolico_39_facebook(self):
        fuentes = Counter(r.get("fuente") for r in self.confirmados)
        self.assertEqual(fuentes["revolico"], 83)
        self.assertEqual(fuentes["facebook"], 39)

    def test_03_descartes_55_y_composicion(self):
        self.assertEqual(len(self.descartes), 55)
        resultados = Counter(r["resultado"] for r in self.descartes)
        self.assertEqual(resultados["NO"], 47)
        self.assertEqual(resultados["INDETERMINADO"], 8)
        fuera = [r for r in self.descartes if not r["en_universo_unificado"]]
        self.assertEqual(len(fuera), 1)
        self.assertEqual(fuera[0]["id_unico"], "facebook-27")

    def test_04_descartes_conservan_registro_original_y_unificado(self):
        for registro in self.descartes:
            self.assertIsInstance(registro.get("registro_original"), dict)
            self.assertTrue(registro["registro_original"])
            self.assertTrue(registro.get("motivo_descarte"))
            if registro["en_universo_unificado"]:
                self.assertEqual(
                    registro["registro_unificado"],
                    self.universo[registro["id_unico"]],
                )

    def test_05_confirmados_y_descartados_no_se_solapan(self):
        confirmados = {r["id_unico"] for r in self.confirmados}
        descartados = {r["id_unico"] for r in self.descartes}
        self.assertEqual(confirmados & descartados, set())

    def test_06_ningun_confirmado_tiene_titulo_externo(self):
        for registro in self.verificacion:
            if registro["resultado"] == "SÍ":
                self.assertEqual(
                    registro["senales_titulo"]["fuera"],
                    [],
                    f"{registro['id_unico']} tiene un título externo",
                )
            if (
                registro["resultado"] == "NO"
                and registro["evidencia_principal"] == "título"
            ):
                self.assertTrue(
                    registro["senales_titulo"]["fuera"],
                    f"{registro['id_unico']} se descartó por título sin señal externa",
                )

    def test_07_ventas_usd_mantienen_los_estadisticos(self):
        usd = [
            a["_precio"] for a in self.anuncios
            if a["_precio"] is not None and a["_moneda"] == "USD"
        ]
        cup = [
            a["_precio"] for a in self.anuncios
            if a["_precio"] is not None and a["_moneda"] == "CUP"
        ]
        ventas = [
            a["_precio"] for a in self.anuncios
            if a["_op"] == "Venta"
            and a["_precio"] is not None
            and a["_moneda"] == "USD"
        ]
        s = stats(ventas)
        self.assertEqual(len(usd), 106)
        self.assertEqual(len(cup), 1)
        self.assertEqual(len(ventas), 43)
        self.assertAlmostEqual(s["mean"], 26023.26, places=2)
        self.assertAlmostEqual(s["median"], 20000.00, places=2)
        self.assertAlmostEqual(s["p10"], 6200.00, places=2)
        self.assertAlmostEqual(s["p90"], 60000.00, places=2)

    def test_08_duplicado_conocido_y_n_efectivo(self):
        pares = {
            frozenset([a["id_unico"]] + (a.get("posibles_duplicados") or []))
            for a in self.confirmados
            if a.get("posibles_duplicados")
        }
        self.assertEqual(len(pares), 1)
        self.assertIn(
            frozenset({"facebook-35", "revolico-58326838"}),
            pares,
        )
        self.assertEqual(len(self.confirmados) - len(pares), 121)


if __name__ == "__main__":
    unittest.main()
