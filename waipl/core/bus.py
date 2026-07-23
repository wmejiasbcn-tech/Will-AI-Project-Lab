"""
WAIPL Core Bus — Bus de Eventos e Interconexión Multicapa
Permite el intercambio de mensajes entre:
- Capa 1: Núcleo Central (Carla, Hermes, Codd, Sylvia Bloom, Ada, Aether, Altheia...)
- Capa 2: Servicios (VAC-01 Guardián, GDO-01, Kairos, SEA-01)
- Capa 3: Cinturón de Kuiper / Vórtice (Z, Kimi K3, Genspark, Neo)
- Capa 4: Gateway Exterior (Antigravity, Cursor, Linear, Notex AI, Make.com y Entidades Externas)
"""

import asyncio
import json
import logging
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("WAIPL-Bus")


class Layer(Enum):
    SOVEREIGN = 0
    CORE = 1
    SERVICES = 2
    KUPER_VORTEX = 3
    EXTERNAL = 4


class MessagePriority(Enum):
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


class Message:
    def __init__(
        self,
        sender_id: str,
        sender_layer: Layer,
        recipient_id: str,
        content: Any,
        priority: MessagePriority = MessagePriority.NORMAL,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        self.id = f"MSG-{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}"
        self.timestamp = datetime.utcnow().isoformat()
        self.sender_id = sender_id
        self.sender_layer = sender_layer
        self.recipient_id = recipient_id
        self.content = content
        self.priority = priority
        self.metadata = metadata or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "sender_id": self.sender_id,
            "sender_layer": self.sender_layer.name,
            "recipient_id": self.recipient_id,
            "content": self.content,
            "priority": self.priority.name,
            "metadata": self.metadata,
        }


class EventBus:
    def __init__(self):
        self._subscribers: Dict[str, List[Callable[[Message], None]]] = {}
        self._history: List[Message] = []
        self._external_firewall_enabled: bool = True

    def subscribe(self, node_id: str, callback: Callable[[Message], None]):
        """Registra una función callback para escuchar mensajes dirigidos a un nodo."""
        if node_id not in self._subscribers:
            self._subscribers[node_id] = []
        self._subscribers[node_id].append(callback)
        logger.info(f"Nodo '{node_id}' suscrito al bus de comunicaciones WAIPL.")

    def publish(self, message: Message) -> bool:
        """Publica y enruta un mensaje en el bus con validación de seguridad."""
        # Validación de Firewall para capa exterior no verificada
        if message.sender_layer == Layer.EXTERNAL and self._external_firewall_enabled:
            logger.info(f"[Firewall SEA-01] Inspeccionando mensaje de capa exterior ({message.sender_id})...")
            # Los mensajes externos deben ser revisados antes de llegar al Núcleo
            if "untrusted" in message.metadata and message.metadata["untrusted"]:
                logger.warning(f"[Firewall SEA-01] Mensaje bloqueado de fuente no confiable: {message.sender_id}")
                return False

        self._history.append(message)
        logger.info(f"[Bus] {message.sender_id} -> {message.recipient_id} | Prioridad: {message.priority.name}")

        listeners = self._subscribers.get(message.recipient_id, [])
        # Soporte para broadcast
        if message.recipient_id == "*":
            listeners = [cb for subs in self._subscribers.values() for cb in subs]

        for listener in listeners:
            try:
                listener(message)
            except Exception as e:
                logger.error(f"Error procesando mensaje en nodo {message.recipient_id}: {e}")

        return True

    def get_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        return [msg.to_dict() for msg in self._history[-limit:]]
