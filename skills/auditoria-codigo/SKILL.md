---
name: auditoria-codigo
description: "Herramientas y flujos de auditoría de código: revisión de cambios, detección de imprecisiones, trazabilidad de estados (IMPLEMENTADO/VALIDADO/PUBLICADO) y separación de evidencia. Úsala ante auditar código, revisar commit, verificar fidelidad de implementación o contrastar repositorio vs. bundle."
type: workflow
lifecycle: active
---

# Auditoría de Código — Evidencia y trazabilidad

Skill para auditorías de código y cambios, con énfasis en separación HECHO / PROPUESTO / PENDIENTE y contraste entre repositorio, tests y artefactos publicados.

## Cuándo activar

- Revisión de commits o PRs relacionados con el Aula.
- Contraste repositorio vs. bundle público.
- Verificación de que un cambio no convierte lo implementado en demostrado.
- Auditoría de tests (Vitest, etc.).

## Flujo de auditoría

1. **Alcance**  
   Define qué archivos, commits o claims se revisan.

2. **Evidencia**  
   Lee el código o el diff real. No te bases solo en mensajes de commit.

3. **Clasificación**  
   - HECHO: presente en el código y verificado.  
   - PROPUESTO: descrito pero no implementado.  
   - PENDIENTE: no comprobado.  
   - CONTRADICTORIO: conflicto entre fuentes.

4. **Trazabilidad**  
   Distingue IMPLEMENTADO (código), VALIDADO (tests) y PUBLICADO (bundle/despliegue).

5. **Informe**  
   Entrega tabla corta con ID, afirmación, clasificación y evidencia.

## Reglas

- No afirmes que algo funciona en producción sin evidencia de ejecución.
- No eleves un mecanismo en código a comportamiento demostrado en el bundle público.
- Cita archivo y línea cuando sea posible.

## Output esperado

- Dictamen breve.
- Matriz de hallazgos.
- Puntos PENDIENTE explícitos.
- Recomendación de cierre o de nueva verificación.
