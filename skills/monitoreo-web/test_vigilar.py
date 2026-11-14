#!/usr/bin/env python3
"""Pruebas de huellas y migración de referencias de monitoreo web."""
from __future__ import annotations

import hashlib
import io
import unittest

from vigilar import VERSION_HUELLA, detectar, huella_de_stream


class HuellaStreamTests(unittest.TestCase):
    def test_hashes_original_bytes_in_chunks(self) -> None:
        cuerpo = b"cabecera\x00\xff\xc3\xa9  valor\n"
        resultado = huella_de_stream(io.BytesIO(cuerpo), tamano=3)
        self.assertEqual(resultado, hashlib.sha256(cuerpo).hexdigest())

    def test_empty_body_has_standard_sha256(self) -> None:
        self.assertEqual(
            huella_de_stream(io.BytesIO(b"")),
            hashlib.sha256(b"").hexdigest(),
        )


class FingerprintMigrationTests(unittest.TestCase):
    def test_legacy_fingerprint_is_rebased_without_false_content_alert(self) -> None:
        anterior = {"estado": "200", "huella": "hash-normalizado-antiguo"}
        fila = {"estado": "200", "huella": "hash-bytes-nuevo", "ms": "120"}

        cambio, fallo = detectar(anterior, fila, aviso=800, corte=2000)

        self.assertIn("referencia renovada", cambio)
        self.assertNotIn("cambió el contenido", cambio)
        self.assertFalse(fallo)

    def test_current_version_detects_real_content_change(self) -> None:
        anterior = {
            "estado": "200",
            "huella": "hash-anterior",
            "huella_version": VERSION_HUELLA,
        }
        fila = {"estado": "200", "huella": "hash-actual", "ms": "120"}

        cambio, fallo = detectar(anterior, fila, aviso=800, corte=2000)

        self.assertIn("cambió el contenido", cambio)
        self.assertFalse(fallo)

    def test_current_version_keeps_unchanged_content_as_equal(self) -> None:
        anterior = {
            "estado": "200",
            "huella": "hash-igual",
            "huella_version": VERSION_HUELLA,
        }
        fila = {"estado": "200", "huella": "hash-igual", "ms": "120"}

        cambio, fallo = detectar(anterior, fila, aviso=800, corte=2000)

        self.assertEqual(cambio, "igual")
        self.assertFalse(fallo)


if __name__ == "__main__":
    unittest.main()
