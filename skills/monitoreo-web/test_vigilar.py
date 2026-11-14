#!/usr/bin/env python3
"""Pruebas de huellas y migración de referencias de monitoreo web."""
from __future__ import annotations

import hashlib
import io
import unittest

from vigilar import (
    VERSION_HUELLA,
    detectar,
    huella_de_stream,
    huellas_de_stream,
    requiere_revision_migracion,
)


def huella_legacy(cuerpo: bytes) -> str:
    texto = " ".join(cuerpo.decode("utf-8", "replace").split())
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


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

    def test_streaming_legacy_hash_matches_previous_algorithm(self) -> None:
        cuerpo = b"  texto\tcon   espacios\nUTF-8: \xc3\xa9 y byte invalido: \xff  "
        nueva, heredada = huellas_de_stream(io.BytesIO(cuerpo), tamano=2)
        self.assertEqual(nueva, hashlib.sha256(cuerpo).hexdigest())
        self.assertEqual(heredada, huella_legacy(cuerpo))


class FingerprintMigrationTests(unittest.TestCase):
    def test_unchanged_legacy_fingerprint_is_verified_before_rebase(self) -> None:
        cuerpo = b"texto   con\nespacios y \xff"
        anterior = {"estado": "200", "huella": huella_legacy(cuerpo)}
        fila = {
            "estado": "200",
            "huella": hashlib.sha256(cuerpo).hexdigest(),
            "huella_legacy": huella_legacy(cuerpo),
            "ms": "120",
        }

        cambio, fallo = detectar(anterior, fila, aviso=800, corte=2000)

        self.assertIn("referencia renovada", cambio)
        self.assertIn("verificada", cambio)
        self.assertNotIn("cambió el contenido", cambio)
        self.assertFalse(requiere_revision_migracion(anterior, cambio))
        self.assertFalse(fallo)

    def test_changed_legacy_fingerprint_alerts_and_requires_manual_review(self) -> None:
        anterior = {"estado": "200", "huella": hashlib.sha256(b"contenido aprobado").hexdigest()}
        fila = {
            "estado": "200",
            "huella": hashlib.sha256(b"contenido alterado").hexdigest(),
            "huella_legacy": huella_legacy(b"contenido alterado"),
            "ms": "120",
        }

        cambio, fallo = detectar(anterior, fila, aviso=800, corte=2000)

        self.assertIn("cambió el contenido", cambio)
        self.assertIn("huella heredada", cambio)
        self.assertTrue(requiere_revision_migracion(anterior, cambio))
        self.assertFalse(fallo)

    def test_unknown_fingerprint_version_requires_manual_review(self) -> None:
        anterior = {
            "estado": "200",
            "huella": "hash-de-version-desconocida",
            "huella_version": "sha512-future",
        }
        fila = {
            "estado": "200",
            "huella": "hash-actual",
            "huella_legacy": "hash-legacy",
            "ms": "120",
        }

        cambio, fallo = detectar(anterior, fila, aviso=800, corte=2000)

        self.assertIn("versión de huella no compatible", cambio)
        self.assertTrue(requiere_revision_migracion(anterior, cambio))
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
