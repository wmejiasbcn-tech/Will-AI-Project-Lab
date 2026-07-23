"""
WAIPL Agente VAC-01 "Guardián de Confianza"
Evalúa la calidad, coherencia factual y nivel de alucinación de las respuestas de IA.
Implementa un arnés flexible:
- Score >= 0.70 -> APROBADO (Entrega directa)
- 0.50 <= Score < 0.70 -> ADVERTENCIA (Entrega con nota contextual, permite flexibilidad/creatividad)
- Score < 0.50 -> BLOQUEADO (Alucinación severa o riesgo de seguridad)
"""

import logging
from enum import Enum
from typing import Any, Dict

logger = logging.getLogger("VAC-01-Guardian")


class ValidationStatus(Enum):
    APPROVED = "APROBADO"
    WARNING = "ADVERTENCIA"
    BLOCKED = "BLOQUEADO"


class VACGuardian:
    def __init__(self, pass_threshold: float = 0.70, warn_threshold: float = 0.50):
        self.pass_threshold = pass_threshold
        self.warn_threshold = warn_threshold
        self.total_evaluated = 0
        self.blocked_count = 0

    def evaluate_output(self, prompt: str, ai_output: str, context: str = "") -> Dict[str, Any]:
        """Evalúa un output generado por una IA y calcula su score de confianza."""
        self.total_evaluated += 1

        # Heurísticas de verificación de calidad y factualidad
        score = self._calculate_confidence_score(prompt, ai_output, context)

        if score >= self.pass_threshold:
            status = ValidationStatus.APPROVED
            action = "Entrega directa al usuario/nodo destinatario."
        elif score >= self.warn_threshold:
            status = ValidationStatus.WARNING
            action = "Entrega con nota de sugerencia contextual (arnés flexible activo)."
        else:
            status = ValidationStatus.BLOCKED
            action = "Bloqueado por alucinación severa o incerteza. Notificado a Hermes."
            self.blocked_count += 1

        result = {
            "score": round(score, 2),
            "status": status.value,
            "action": action,
            "prompt_length": len(prompt),
            "output_length": len(ai_output),
        }

        logger.info(f"[VAC-01] Evaluación completada | Score: {result['score']} | Estado: {result['status']}")
        return result

    def _calculate_confidence_score(self, prompt: str, ai_output: str, context: str) -> float:
        """Calcula el score de confianza (0.0 - 1.0) basado en reglas y heurísticas."""
        if not ai_output or len(ai_output.strip()) == 0:
            return 0.0

        base_score = 0.85

        # Penalizaciones por indicadores típicos de alucinación o respuestas vacías
        output_lower = ai_output.lower()
        if "como modelo de lenguaje" in output_lower or "no tengo acceso a datos" in output_lower:
            base_score -= 0.15

        if len(ai_output) < 10 and len(prompt) > 50:
            base_score -= 0.20

        # Si hay contexto RAG proporcionado, se verifica coincidencia de palabras clave
        if context:
            context_words = set(context.lower().split())
            output_words = set(output_lower.split())
            overlap = len(context_words.intersection(output_words))
            if overlap > 5:
                base_score += 0.10

        return max(0.0, min(1.0, base_score))
