"""
Suite de Pruebas Unitarias para el Ecosistema WAIPL
Verifica la funcionalidad del Bus, el Guardián VAC-01, Codd GDO-01, Kairos y SEA-01.
"""

import os
import shutil
import tempfile
import pytest

from waipl.core.bus import EventBus, Layer, Message, MessagePriority
from waipl.agents.vac_guardian import VACGuardian, ValidationStatus
from waipl.agents.gdo_archivist import CoddArchivist
from waipl.agents.kairos_extractor import KairosExtractor
from waipl.agents.sea_fortress import SEAFortress


def test_event_bus():
    bus = EventBus()
    received_messages = []

    def callback(msg: Message):
        received_messages.append(msg)

    bus.subscribe("Hermes", callback)

    msg = Message(
        sender_id="Carla",
        sender_layer=Layer.CORE,
        recipient_id="Hermes",
        content="Prueba de coordinación operativa",
        priority=MessagePriority.HIGH,
    )

    success = bus.publish(msg)
    assert success is True
    assert len(received_messages) == 1
    assert received_messages[0].sender_id == "Carla"
    assert received_messages[0].content == "Prueba de coordinación operativa"


def test_vac_guardian_flexible_harness():
    guardian = VACGuardian(pass_threshold=0.70, warn_threshold=0.50)

    # 1. Output de alta calidad (Aprobado)
    res_pass = guardian.evaluate_output("¿Qué es la reducción de daños?", "La reducción de daños busca minimizar riesgos en consumo de sustancias.", context="reducción de daños minimizar riesgos")
    assert res_pass["status"] == ValidationStatus.APPROVED.value
    assert res_pass["score"] >= 0.70

    # 2. Output con frase cliché / incerteza leve (Advertencia - Arnés flexible activo)
    res_warn = guardian.evaluate_output("¿Cuál es la respuesta?", "Como modelo de lenguaje no tengo acceso a datos en tiempo real pero sugiero revisar fuentes oficiales.")
    assert res_warn["status"] in [ValidationStatus.WARNING.value, ValidationStatus.APPROVED.value]

    # 3. Output vacío (Bloqueado)
    res_block = guardian.evaluate_output("Consulta compleja", "")
    assert res_block["status"] == ValidationStatus.BLOCKED.value
    assert res_block["score"] < 0.50


def test_codd_archivist_and_kairos():
    temp_dir = tempfile.mkdtemp()
    try:
        codd = CoddArchivist(base_storage_dir=temp_dir)
        kairos = KairosExtractor(archivist=codd)

        res = kairos.ingest_scientific_article(
            title="Protocolo de Reducción de Riesgos en Chemsex",
            source_url="https://salud.ejemplo.org/chemsex-protocol",
            content_text="Documento oficial sobre intervención comunitaria y salud sexual.",
            category="SALUD_SEXUAL",
        )

        assert res["status"] == "RAG_READY"
        assert res["archived_record"] is not None
        assert res["archived_record"]["author_node"] == "Kairos"
        assert len(res["archived_record"]["sha256"]) == 64
    finally:
        shutil.rmtree(temp_dir)


def test_sea_fortress():
    sea = SEAFortress()
    scan = sea.scan_node_integrity()
    assert scan["status"] == "SECURE"

    sea.log_security_event(source="GatewayExterior", event_type="UNAUTHORIZED_ACCESS", severity="CRITICAL", details="Intento de puerto no autorizado")
    report = sea.generate_weekly_consolidated_report()
    assert report["critical_threats"] == 1
    assert report["period"] == "Semanal Consolidado"
