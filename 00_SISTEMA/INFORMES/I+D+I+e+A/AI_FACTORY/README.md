# I+D+i+e+A — AI FACTORY

## Línea de investigación AF-01

**Denominación:** WAIPL AI Factory — Línea de Investigación en Infraestructura Agentica, Inferencia y AI Factory  
**Código:** I+D+i+e+A / AF-01  
**Estado:** ABIERTA — ESTUDIO DE VIABILIDAD  
**Fecha de apertura:** 2026-09-11  
**Naturaleza:** Investigación aplicada / estudio de viabilidad / experimentación arquitectónica  
**Carácter:** Independiente de proveedor tecnológico

## Propósito

Investigar la viabilidad de una arquitectura de AI Factory / Agentic Infrastructure para WAIPL que desacople agentes, modelos, runtimes e infraestructura, permitiendo utilizar NVIDIA y otros proveedores como componentes intercambiables sin convertirlos en la arquitectura del ecosistema.

## Independencia respecto de otras líneas

AF-01 constituye una **tercera vía de investigación independiente** dentro del corpus I+D+i+e+A.

No forma parte de:

- G3 / ALNIRA
- Graphify / LLM / WikiSkill

Estas líneas podrán compartir aprendizajes o interfaces cuando corresponda, pero no se fusionan conceptualmente ni documentalmente.

## Hipótesis central

WAIPL podría beneficiarse de una capa propia de infraestructura de ejecución agentica en la que:

**AGENTE → SERVICIO IA → INFERENCIA → COMPUTE → INFRAESTRUCTURA**

se encuentren suficientemente desacoplados para permitir sustitución tecnológica, control operativo, observabilidad, resiliencia y gobernanza.

## Referencia tecnológica inicial

NVIDIA DSX OS y su ecosistema asociado constituyen una referencia experimental, no una decisión de adopción.

Elementos iniciales a investigar:

- DSX OS
- NIM
- Dynamo
- NVCF
- Run:ai
- Kubernetes / NKE / NKD
- AI Factory Orchestrator
- VMaaS
- NICo
- DPF
- NVCM
- RMS
- NVSentinel
- Fleet Intelligence
- Health Validation
- Maestro

## Casos reales de experimentación

La investigación podrá utilizar como casos de estudio sistemas ya existentes en WAIPL, entre ellos Vár, Emily, Watchdog, Vigil/Vigilant, William-SCY-01 y sistemas de comunicación interna, así como la progresiva migración de funciones actualmente construidas con n8n.

## Principio rector

> **No investigar NVIDIA para decidir utilizar NVIDIA. Investigar AI Factory para determinar qué infraestructura necesita WAIPL.**

NVIDIA podrá ser infraestructura, runtime, proveedor de modelos, proveedor de servicios o componente experimental, pero no será considerada la arquitectura WAIPL por defecto.

## Resultado esperado de la primera fase

Un informe de viabilidad que determine si es técnicamente, arquitectónicamente, operacionalmente, económicamente y organizativamente viable construir una capa de infraestructura agentica agnóstica para WAIPL, junto con un diseño de Proof of Concept.
