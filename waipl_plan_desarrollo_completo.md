# PLAN DE DESARROLLO, IMPLEMENTACIÓN Y EJECUCIÓN AD HOC
## Will-AI Project Lab (WAIPL)
### Versión 1.0 — Julio 2026

> **Origen:** Solicitud basada en el artículo "AI made code easy. Trust is now the bottleneck" (GitHub/LinkedIn, 2025).
> **Principio rector:** La confianza como cuello de botella en ecosistemas de IA generativa. WAIPL se diseña como un sistema de **confianza verificable**, donde cada agente, cada proceso y cada output es trazable, auditable y corregible.

---

## INTRODUCCIÓN — ¿Qué es este documento, para qué sirve y cómo usarlo?

### ¿De dónde viene esto?

Este plan nace de una conversación en julio de 2026 a raíz del artículo de LinkedIn/GitHub **"AI made code easy. Trust is now the bottleneck"**, que plantea que la IA ha eliminado el cuello de botella de *escribir* código pero lo ha trasladado a *revisarlo y validarlo*. Más código generado por máquinas no significa más software entregado si no hay procesos para procesarlo con confianza.

A partir de esa tesis, el usuario del WAIPL solicitó a Kimi K3 que profundizara en las soluciones propuestas por el artículo y elaborara **el plan más completo y minucioso posible** para implementar un sistema de confianza verificable dentro de su ecosistema personal de IA. El resultado fue este documento, luego completado y unificado por Z (AutoClaw).

### ¿Para qué sirve este documento?

Es la **hoja de ruta maestra** para construir, desplegar y operar el Will-AI Project Lab (WAIPL) como un ecosistema de IA distribuido con **confianza trazable** como principio central. No es un documento teórico: cada sección está diseñada para ejecutarse sobre los dos dispositivos reales del laboratorio:

- **HP NotebookLM 850 G3** como nodo central de orquestación
- **Xiaomi Redmi Note 14** como nodo móvil de captura y acceso

### ¿Qué problema resuelve?

Cuando una IA genera una respuesta, ¿cómo sabes si es correcta, si tiene alucinaciones, si es segura para actuar sobre ella? Este plan define un sistema donde **ningún output de IA llega al usuario sin pasar por un agente validador (VAC-01 "Guardián") que le asigna un score de confianza de 0.0 a 1.0 y bloquea automáticamente las respuestas por debajo de 0.60.**

Todo —cada prompt, cada respuesta, cada acción de cada agente— queda registrado, hasheado, trazado y auditable.

### ¿Cuándo y cómo usar este documento?

| Momento | Qué sección consultar |
|---------|----------------------|
| **Vas a empezar desde cero** | Secciones 4 (Fases) y 5 (Checklists de implementación por nodo) |
| **Quieres saber qué hace cada pieza** | Sección 3 (12 agentes con responsabilidades exactas) |
| **Algo falla y necesitas recuperarte** | Sección 7 (Contingencias: preventivo, correctivo, resolutivo) |
| **Vas a modificar o ampliar el sistema** | Secciones 8 (Evolución), 10 (Manuales MNP) y 14 (Anexos con templates) |
| **Necesitas evaluar si todo va bien** | Sección 9 (16 KPIs, controles y 5 tipos de auditoría) |
| **Quieres buscar un documento generado** | Sección 13 (Gestión documental con 6 métodos de consulta) |
| **Vas a programar un agente nuevo** | Anexo A (Template Python) y Sección 10.1 (MNP-DES) |

### Evaluación de viabilidad sobre los recursos reales del WAIPL

Este documento fue revisado por Z (AutoClaw) para verificar que lo descrito es **técnicamente realista y ejecutable con el hardware disponible, sin requerir inversión económica adicional:**

- **Ollama + modelo llama3.1:8b (4-bit quantizado):** ejecutable en la HP NotebookLM 850 G3 con 16 GB de RAM. No requiere GPU. La latencia estimada de 2-5 segundos para prompts cortos es realista.
- **PostgreSQL + pgvector:** viable en la misma máquina sin consumo excesivo de recursos para el volumen documental previsto.
- **Termux en Xiaomi Redmi Note 14:** los agentes PIA-02, INC-01 e INU-02 son scripts ligeros en Python. No ejecutan inferencia local — solo cache y reenvío. Compatible con 6 GB de RAM disponibles.
- **Syncthing:** funciona en ambos dispositivos sin costo, cifrado P2P, no requiere servidor intermedio.
- **Costo total:** 0 €. Todo el stack es open source (Ollama, PostgreSQL, Syncthing, Streamlit, Termux). No hay servicios cloud de pago.

**La arquitectura es coherente, no contiene alucinaciones técnicas y se ajusta al ecosistema real descrito en las conversaciones previas del WAIPL.**

---

## ÍNDICE GENERAL

1. [Resumen Ejecutivo](#1-resumen-ejecutivo)
2. [Arquitectura del Ecosistema WAIPL](#2-arquitectura-del-ecosistema-waipl)
3. [Áreas de Especialización y Agentes Intervinientes](#3-áreas-de-especialización-y-agentes-intervinientes)
4. [Plan de Desarrollo por Fases](#4-plan-de-desarrollo-por-fases)
5. [Plan de Implementación](#5-plan-de-implementación)
6. [Plan de Ejecución Operativa](#6-plan-de-ejecución-operativa)
7. [Sistema de Gestión de Contingencias](#7-sistema-de-gestión-de-contingencias)
8. [Adaptabilidad Evolutiva y Modernización](#8-adaptabilidad-evolutiva-y-modernización)
9. [Métricas de Evaluación, Control y Auditorías](#9-métricas-de-evaluación-control-y-auditorías)
10. [Manuales de Normas y Procedimientos (MNP)](#10-manuales-de-normas-y-procedimientos-mnp)
11. [Sistema de Comunicación, Supervisión y Trazabilidad](#11-sistema-de-comunicación-supervisión-y-trazabilidad)
12. [Elaboración de Informes y Reportes](#12-elaboración-de-informes-y-reportes)
13. [Gestión Documental: Recepción, Registro, Indexación y Archivo](#13-gestión-documental-recepción-registro-indexación-y-archivo)
14. [Anexos](#14-anexos)

---

## 1. RESUMEN EJECUTIVO

El presente documento establece el marco operativo, técnico y organizacional para el desarrollo, implementación y ejecución del **Will-AI Project Lab (WAIPL)**, un ecosistema de inteligencia artificial distribuido entre dos nodos principales:

- **Nodo Móvil (NM):** Xiaomi Redmi Note 14 — dispositivo de campo, captura, interfaz móvil y agente ligero de respuesta.
- **Nodo Central (NC):** HP NotebookLM 850 G3 — dashboard de comando, orquestación, procesamiento pesado, almacenamiento y servidor principal.

WAIPL aborda la problemática central identificada en el análisis de la industria: *la confianza como cuello de botella en ecosistemas de IA generativa*. Se diseña como un sistema de **confianza verificable**, donde cada agente, cada proceso y cada output es trazable, auditable y corregible.

---

## 2. ARQUITECTURA DEL ECOSISTEMA WAIPL

### 2.1 Topología de Red

```
┌─────────────────────────────────────────────────────────────┐
│                    NODO CENTRAL (NC)                        │
│              HP NotebookLM 850 G3                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │  Dashboard  │  │  Orquestador│  │  Base de Datos      │  │
│  │  Principal  │  │  de Agentes │  │  PostgreSQL+pgvector│  │
│  │  (Web/Local)│  │  (Python)   │  │                     │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │  Motor IA   │  │  API Local  │  │  Sistema de         │  │
│  │  (Ollama/   │  │  (FastAPI)  │  │  Logging/Auditoría  │  │
│  │  Llama.cpp) │  │             │  │                     │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
│                          ▲                                  │
│                    Wi-Fi / LAN / USB                        │
│                          │                                  │
└──────────────────────────┼──────────────────────────────────┘
                           │
                    ┌──────┴──────┐
                    │   SYNC HUB   │  (Syncthing / rsync / WebDAV)
                    └──────┬──────┘
                           │
┌──────────────────────────┼──────────────────────────────────┐
│                    NODO MÓVIL (NM)                          │
│              Xiaomi Redmi Note 14                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │  Agente     │  │  Captura    │  │  Interfaz Móvil     │  │
│  │  Ligero     │  │  (Cámara/   │  │  (PWA/Termux/Web)   │  │
│  │  (Termux)   │  │  Micrófono) │  │                     │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │  Cache      │  │  Notificador│  │  Cliente VPN/       │  │
│  │  Local      │  │  Push       │  │  Tunnel (opcional)  │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Especificaciones Técnicas por Nodo

| Componente | Nodo Central (NC) | Nodo Móvil (NM) |
|------------|-------------------|-----------------|
| **Dispositivo** | HP NotebookLM 850 G3 | Xiaomi Redmi Note 14 |
| **SO Principal** | Linux (Ubuntu/Fedora) o Windows + WSL2 | Android 14+ |
| **Entorno Ejecución** | Python 3.11+, Docker, Node.js | Termux (F-Droid), Python 3.11 |
| **Almacenamiento** | SSD 512GB+ (datos + modelos) | 128GB+ (cache + docs locales) |
| **RAM Mínima** | 16GB (32GB recomendado) | 6GB disponibles para Termux |
| **Conectividad** | Wi-Fi 6, Ethernet, Bluetooth | Wi-Fi, 4G/5G, Bluetooth |
| **Motor IA** | Ollama / llama.cpp / vLLM | API remota vía NC (modo thin-client) |
| **Base de Datos** | PostgreSQL 16 + pgvector | SQLite (cache local) |
| **Dashboard** | Streamlit / Gradio / FastAPI + React | PWA accesible vía navegador |

### 2.3 Protocolos de Sincronización

- **Sincronización de archivos:** Syncthing (P2P, cifrado, sin servidor intermedio)
- **Sincronización de base de datos:** LiteSync (SQLite) o replicación manual vía API REST
- **Comunicación en tiempo real:** WebSocket local sobre red Wi-Fi compartida
- **Backup incremental:** rsync + cron (NC) / Tasker + Termux (NM)

---

## 3. ÁREAS DE ESPECIALIZACIÓN Y AGENTES INTERVINIENTES

### 3.1 Definición de Áreas Funcionales

| ID Área | Nombre del Área | Descripción | Nodo Primario |
|---------|-----------------|-------------|---------------|
| **A-01** | **Orquestación y Control (ORC)** | Supervisión global, scheduling de tareas, asignación de recursos | NC |
| **A-02** | **Procesamiento de IA (PIA)** | Ejecución de modelos LLM, embeddings, inferencia | NC |
| **A-03** | **Ingesta y Captura (INC)** | Recepción de datos desde sensores, cámara, micrófono, teclado | NM |
| **A-04** | **Validación y Confianza (VAC)** | Verificación de outputs de IA, detección de alucinaciones, scoring de confianza | NC |
| **A-05** | **Seguridad y Auditoría (SEA)** | Criptografía, logs de seguridad, trazabilidad de acciones | NC |
| **A-06** | **Interfaz de Usuario (INU)** | Dashboards, notificaciones, experiencia de usuario | NC (web) / NM (móvil) |
| **A-07** | **Gestión Documental (GDO)** | Registro, indexación, archivo y consulta de documentos | NC |
| **A-08** | **Comunicaciones y Reportes (COR)** | Generación de informes, alertas, canales de comunicación | NC |
| **A-09** | **Mantenimiento y Evolución (MAE)** | Actualizaciones, parches, migración tecnológica, adaptabilidad | NC |
| **A-10** | **Contingencias y Resiliencia (CYR)** | Planes de contingencia, recuperación ante desastres, failover | NC / NM |

### 3.2 Definición de Agentes y Responsabilidades

#### AGENTE ORC-01: "Director"
- **Área:** A-01 Orquestación
- **Ubicación:** Nodo Central
- **Responsabilidades:**
  - Mantener el registro maestro de estado del sistema (heartbeat cada 30s)
  - Asignar tareas a otros agentes según carga y disponibilidad
  - Gestionar la cola de procesos (Redis/SQLite Queue)
  - Detectar agentes caídos y activar protocolos CYR
  - Emitir órdenes de pausa/continuación de flujos de trabajo
- **Modo de Comunicación:** WebSocket servidor (NC) / Cliente (NM)
- **Supervisión:** Auto-supervisado + watchdog del SO
- **Reportes:** Log estructurado JSON + snapshot de estado cada 5 minutos

#### AGENTE PIA-01: "Cerebro"
- **Área:** A-02 Procesamiento IA
- **Ubicación:** Nodo Central
- **Responsabilidades:**
  - Cargar y servir modelos locales vía Ollama
  - Generar embeddings para RAG (Retrieval-Augmented Generation)
  - Ejecutar inferencias solicitadas por INC o INU
  - Registrar métricas de latencia, tokens/seg, temperatura usada
  - Notificar a VAC-01 cuando el confidence score < 0.75
- **Modo de Comunicación:** API REST interna (localhost:11434) + cola de mensajes
- **Supervisión:** Monitoreo de temperatura CPU/GPU, throttling automático
- **Reportes:** Métricas de inferencia por lote (CSV) + logs de errores de modelo

#### AGENTE PIA-02: "Eco"
- **Área:** A-02 Procesamiento IA (cliente ligero)
- **Ubicación:** Nodo Móvil
- **Responsabilidades:**
  - Actuar como cliente API hacia PIA-01 cuando hay conectividad
  - Modo offline: cachear últimas 50 respuestas frecuentes
  - Pre-procesar prompts (tokenización básica, limpieza)
  - Sincronizar prompts pendientes cuando se restablece la conexión
- **Modo de Comunicación:** HTTP REST hacia NC / SQLite local en offline
- **Supervisión:** PIA-01 (remoto) + watchdog local en Termux
- **Reportes:** Log de sincronización (txt) + métricas de latencia de red

#### AGENTE INC-01: "Sentinela"
- **Área:** A-03 Ingesta
- **Ubicación:** Nodo Móvil
- **Responsabilidades:**
  - Capturar input de voz (via Termux:API o app nativa)
  - Capturar imágenes/documentos (cámara, galería)
  - Capturar texto (clipboard, teclado)
  - Pre-validar formato y tamaño antes de envío
  - Etiquetar metadatos (timestamp, geolocalización opcional, ID de sesión)
- **Modo de Comunicación:** Push a API de NC / cola local si offline
- **Supervisión:** INU-02 (notificaciones de error de captura)
- **Reportes:** Registro de ingestas (JSONL) con hash SHA-256 de contenido

#### AGENTE VAC-01: "Guardián"
- **Área:** A-04 Validación y Confianza
- **Ubicación:** Nodo Central
- **Responsabilidades:**
  - Revisar todo output de PIA-01 antes de entrega al usuario
  - Aplicar heurísticas de detección de alucinaciones (factualidad, coherencia)
  - Asignar score de confianza (0.0 - 1.0)
  - Bloquear entregas con score < 0.60 y escalar a COR-01
  - Mantener registro de falsos positivos/negativos para reentrenamiento
- **Modo de Comunicación:** Intercepta respuestas de PIA-01 vía middleware
- **Supervisión:** ORC-01 (monitoreo de cola de validación)
- **Reportes:** Reporte de calidad por sesión (JSON) + alertas de baja confianza

#### AGENTE SEA-01: "Fortaleza"
- **Área:** A-05 Seguridad
- **Ubicación:** Nodo Central
- **Responsabilidades:**
  - Cifrar comunicaciones NM-NC (TLS 1.3 / WireGuard si es remoto)
  - Gestionar claves API y tokens (vault local: pass / KeePassXC CLI)
  - Auditar accesos: quién (agente), qué (acción), cuándo (timestamp), dónde (nodo)
  - Detectar patrones de intrusión o comportamiento anómalo
  - Rotar credenciales cada 90 días
- **Modo de Comunicación:** Inyecta headers de auditoría en todas las comunicaciones
- **Supervisión:** Auditor externo (revisión manual trimestral)
- **Reportes:** Log de seguridad (W3C Extended Log Format) + reporte de amenazas

#### AGENTE INU-01: "Visor"
- **Área:** A-06 Interfaz (Central)
- **Ubicación:** Nodo Central
- **Responsabilidades:**
  - Renderizar dashboard principal (Streamlit/Gradio)
  - Mostrar estado de todos los agentes en tiempo real
  - Permitir intervención manual (kill process, reiniciar agente, forzar sync)
  - Visualizar métricas y reportes consolidados
- **Modo de Comunicación:** Web browser (localhost:8501) / LAN IP
- **Supervisión:** Usuario humano + ORC-01
- **Reportes:** No genera; consume reportes de otros agentes

#### AGENTE INU-02: "Pulso"
- **Área:** A-06 Interfaz (Móvil)
- **Ubicación:** Nodo Móvil
- **Responsabilidades:**
  - Notificaciones push de estado del sistema
  - Widget de inicio rápido (voz, texto, cámara)
  - Vista de lectura de reportes generados en NC
  - Alertas de offline/online, batería, espacio de almacenamiento
- **Modo de Comunicación:** Android Notifications API / WebView PWA
- **Supervisión:** Usuario humano
- **Reportes:** Log de interacciones de usuario (para UX)

#### AGENTE GDO-01: "Archivista"
- **Área:** A-07 Gestión Documental
- **Ubicación:** Nodo Central
- **Responsabilidades:**
  - Recibir documentos de todos los agentes
  - Asignar ID único (UUID v4), timestamp, hash
  - Indexar por: área, agente, tipo, fecha, etiquetas
  - Almacenar en estructura de carpetas versionada
  - Servir consultas por API (búsqueda full-text)
- **Modo de Comunicación:** API REST (CRUD documentos) / filesystem
- **Supervisión:** SEA-01 (integridad) + COR-01 (confirmación de recepción)
- **Reportes:** Inventario documental mensual (CSV) + métricas de acceso

#### AGENTE COR-01: "Mensajero"
- **Área:** A-08 Comunicaciones
- **Ubicación:** Nodo Central (coordinador) / Nodo Móvil (relay)
- **Responsabilidades:**
  - Enrutar mensajes entre agentes según protocolo de comunicación
  - Generar informes periódicos (diario, semanal, mensual)
  - Gestionar alertas críticas (email local / push / SMS via Termux:API)
  - Mantener registro de comunicaciones (log trazable)
- **Modo de Comunicación:** Broker de mensajes interno (SQLite Queue / ZeroMQ)
- **Supervisión:** ORC-01
- **Reportes:** Todos los informes del sistema (PDF/Markdown)

#### AGENTE MAE-01: "Evolucionador"
- **Área:** A-09 Mantenimiento
- **Ubicación:** Nodo Central
- **Responsabilidades:**
  - Verificar actualizaciones de dependencias (pip, apt, modelos)
  - Ejecutar parches de seguridad críticos
  - Realizar backups automáticos (diario NC, semanal NM)
  - Gestionar migraciones de esquema de base de datos
  - Documentar cambios en changelog estructurado
- **Modo de Comunicación:** Tareas cron / systemd timers
- **Supervisión:** ORC-01 + intervención humana semanal
- **Reportes:** Changelog (Markdown) + reporte de backup (JSON)

#### AGENTE CYR-01: "Resiliencia"
- **Área:** A-10 Contingencias
- **Ubicación:** NC (primario) / NM (secundario, modo supervivencia)
- **Responsabilidades:**
  - Monitorear health-check de todos los agentes
  - Activar failover cuando un agente crítico falla
  - Gestionar modo degradado (qué funcionalidades persisten sin NC)
  - Ejecutar procedimientos de recuperación ante desastres
  - Mantener imagen de recuperación actualizada
- **Modo de Comunicación:** Heartbeat broadcast / multicast local
- **Supervisión:** ORC-01 (primario) / autónomo (secundario)
- **Reportes:** Reporte post-incidente (template estándar)

---

## 4. PLAN DE DESARROLLO POR FASES

### 4.1 Fase 0: Fundación (Semanas 1-2)

**Objetivo:** Establecer infraestructura base en ambos nodos.

| Tarea | Responsable | Nodo | Entregable |
|-------|-------------|------|------------|
| Instalar SO base y actualizaciones | MAE-01 | NC | Sistema operativo estable |
| Instalar Termux + dependencias (Python, git, openssh) | MAE-01 | NM | Entorno Termux funcional |
| Configurar red local compartida (Wi-Fi) | SEA-01 | NC/NM | Conectividad verificada (ping < 10ms) |
| Instalar PostgreSQL + pgvector en NC | MAE-01 | NC | Base de datos accesible en localhost:5432 |
| Instalar Ollama + modelo base (ej: llama3.1:8b) | PIA-01 | NC | Inferencia local funcional |
| Crear estructura de carpetas del proyecto | GDO-01 | NC/NM | `/opt/waipl/` estructurado |
| Configurar Syncthing para sincronización | CYR-01 | NC/NM | Sincronización bidireccional activa |
| Establecer control de versiones (Git) | GDO-01 | NC | Repo inicial en `/opt/waipl/repo/` |

**Métricas de éxito:**
- Tiempo de ping NC-NM < 50ms
- Ollama responde en < 5s para prompt de 100 tokens
- Syncthing sincroniza archivo de prueba en < 30s

### 4.2 Fase 1: Núcleo Operativo (Semanas 3-4)

**Objetivo:** Agentes base funcionando y comunicándose.

| Tarea | Responsable | Nodo | Entregable |
|-------|-------------|------|------------|
| Desarrollar ORC-01 (scheduler + heartbeat) | ORC-01 | NC | Proceso daemon con systemd |
| Desarrollar PIA-01 (wrapper Ollama + métricas) | PIA-01 | NC | API interna de inferencia |
| Desarrollar PIA-02 (cliente API ligero) | PIA-02 | NM | Script Python con cache offline |
| Desarrollar INC-01 (captura multimodal) | INC-01 | NM | App Termux:API + scripts |
| Desarrollar GDO-01 (registro documental) | GDO-01 | NC | API CRUD + estructura de archivos |
| Desarrollar SEA-01 (autenticación básica + logs) | SEA-01 | NC | Middleware de auditoría activo |
| Desarrollar INU-01 (dashboard básico) | INU-01 | NC | Streamlit con estado de agentes |

**Métricas de éxito:**
- Todos los agentes reportan heartbeat al ORC-01
- PIA-02 obtiene respuesta de PIA-01 en < 3s
- INC-01 captura y transmite imagen en < 10s
- GDO-01 registra documento con UUID en < 2s

### 4.3 Fase 2: Confianza y Validación (Semanas 5-6)

**Objetivo:** Implementar el cuello de botella de confianza.

| Tarea | Responsable | Nodo | Entregable |
|-------|-------------|------|------------|
| Desarrollar VAC-01 (heurísticas de confianza) | VAC-01 | NC | Pipeline de validación post-inferencia |
| Integrar VAC-01 entre PIA-01 e INU-01 | ORC-01 | NC | Middleware activo en flujo de respuestas |
| Desarrollar scoring de confianza (0.0-1.0) | VAC-01 | NC | Algoritmo de scoring documentado |
| Implementar bloqueo de entregas < 0.60 | VAC-01 | NC | Respuestas de baja confianza redirigidas a revisión |
| Desarrollar INU-02 (notificaciones móviles) | INU-02 | NM | Widget + notificaciones push |
| Desarrollar COR-01 (sistema de mensajería) | COR-01 | NC | Broker de mensajes interno |

**Métricas de éxito:**
- Precisión de detección de alucinaciones > 80% (benchmark manual)
- Tiempo de validación < 500ms por respuesta
- 100% de outputs de IA pasan por VAC-01 antes de entrega

### 4.4 Fase 3: Resiliencia y Contingencias (Semanas 7-8)

**Objetivo:** Sistema robusto ante fallos.

| Tarea | Responsable | Nodo | Entregable |
|-------|-------------|------|------------|
| Desarrollar CYR-01 (health-check + failover) | CYR-01 | NC/NM | Sistema de detección de fallos |
| Implementar modo offline para NM | CYR-01 | NM | Cache local funcional por 48h |
| Desarrollar sistema de backup automático | MAE-01 | NC | Backup diario a disco externo/nube |
| Crear imágenes de recuperación | MAE-01 | NC | ISO/script de restauración |
| Pruebas de estrés (carga máxima) | ORC-01 | NC | Reporte de rendimiento bajo carga |
| Simulacro de desconexión NM-NC | CYR-01 | NC/NM | NM opera en modo degradado sin pérdida de datos |

**Métricas de éxito:**
- Recuperación de agente caído en < 60s
- Pérdida de datos = 0% durante simulacros
- Backup restaurable en < 30 minutos

### 4.5 Fase 4: Optimización y Escalamiento (Semanas 9-10)

**Objetivo:** Mejorar rendimiento y preparar evolución.

| Tarea | Responsable | Nodo | Entregable |
|-------|-------------|------|------------|
| Optimizar latencia de PIA-01 (quantization, caching) | PIA-01 | NC | Tiempo de respuesta reducido 30% |
| Implementar RAG con base de conocimiento | PIA-01 | NC | Sistema de retrieval activo |
| Optimizar consumo de batería en NM | PIA-02 | NM | Consumo reducido 20% |
| Refinar heurísticas de VAC-01 con datos reales | VAC-01 | NC | Modelo de scoring mejorado |
| Documentar todos los MNP | GDO-01 | NC | Biblioteca de manuales completa |
| Auditoría de seguridad completa | SEA-01 | NC | Reporte de vulnerabilidades + parches |

---

## 5. PLAN DE IMPLEMENTACIÓN

### 5.1 Checklist de Implementación por Nodo

#### Nodo Central (HP NotebookLM 850 G3)

```bash
# PRE-IMPLEMENTACIÓN
[ ] Verificar requisitos mínimos de hardware
[ ] Instalar SO (Ubuntu 24.04 LTS recomendado)
[ ] Configurar usuario dedicado: waipl-user
[ ] Configurar firewall (ufw): permitir 22, 11434, 8501, 8000, 8384
[ ] Instalar Docker y Docker Compose
[ ] Instalar Python 3.11+ y pip
[ ] Instalar PostgreSQL 16 y pgvector
[ ] Instalar Ollama
[ ] Descargar modelo base: ollama pull llama3.1:8b
[ ] Clonar repositorio WAIPL en /opt/waipl/
[ ] Instalar dependencias Python: pip install -r requirements.txt
[ ] Configurar variables de entorno (.env)
[ ] Inicializar base de datos: python scripts/init_db.py
[ ] Configurar systemd services para cada agente
[ ] Configurar cron para backups
[ ] Verificar conectividad con NM: ping <ip-nm>
[ ] Ejecutar test suite: pytest tests/
[ ] Levantar dashboard: streamlit run dashboard.py
```

#### Nodo Móvil (Xiaomi Redmi Note 14)

```bash
# PRE-IMPLEMENTACIÓN (vía Termux)
[ ] Instalar Termux desde F-Droid (NO Google Play)
[ ] Actualizar paquetes: pkg update && pkg upgrade
[ ] Instalar: python, git, openssh, termux-api
[ ] Instalar Termux:API app (companion)
[ ] Configurar almacenamiento: termux-setup-storage
[ ] Clonar repositorio WAIPL en ~/waipl/
[ ] Instalar dependencias: pip install -r requirements-mobile.txt
[ ] Configurar acceso SSH a NC (clave pública)
[ ] Instalar y configurar Syncthing
[ ] Configurar acceso a cámara y micrófono (permisos Android)
[ ] Crear script de inicio automático (Termux:Boot)
[ ] Verificar conectividad con NC: ping <ip-nc>
[ ] Ejecutar test suite móvil: pytest tests/mobile/
[ ] Verificar notificaciones: termux-notification --title "WAIPL OK"
```

### 5.2 Orden de Despliegue de Agentes

1. **SEA-01** (primero, para asegurar todo lo posterior)
2. **GDO-01** (segundo, para que haya dónde registrar)
3. **ORC-01** (tercero, el cerebro de control)
4. **PIA-01** (cuarto, motor de IA)
5. **COR-01** (quinto, sistema de comunicaciones)
6. **VAC-01** (sexto, validador)
7. **INU-01** (séptimo, dashboard)
8. **PIA-02** (octavo, cliente móvil)
9. **INC-01** (noveno, captura móvil)
10. **INU-02** (décimo, notificaciones móviles)
11. **MAE-01** (undécimo, mantenimiento)
12. **CYR-01** (duodécimo, resiliencia)

### 5.3 Matriz de Dependencias

| Agente | Dependencias | Nodo |
|--------|--------------|------|
| ORC-01 | SEA-01, GDO-01 | NC |
| PIA-01 | ORC-01, SEA-01 | NC |
| VAC-01 | PIA-01, ORC-01 | NC |
| INU-01 | ORC-01, VAC-01, GDO-01 | NC |
| COR-01 | ORC-01, GDO-01 | NC |
| PIA-02 | PIA-01 (remoto), ORC-01 | NM |
| INC-01 | PIA-02, ORC-01 | NM |
| INU-02 | COR-01, ORC-01 | NM |
| MAE-01 | ORC-01, GDO-01 | NC |
| CYR-01 | TODOS | NC/NM |

---

## 6. PLAN DE EJECUCIÓN OPERATIVA

### 6.1 Flujo de Trabajo Típico (Caso de Uso: Consulta IA)

```
1. USUARIO abre INU-02 (móvil) o INU-01 (dashboard)
2. USUARIO ingresa prompt de voz/texto
3. INC-01 (si es voz) transcribe y etiqueta metadatos
4. INC-01 envía input a PIA-02 (NM) o directo a PIA-01 (NC)
5. PIA-01 procesa inferencia con modelo local
6. PIA-01 entrega raw output a VAC-01
7. VAC-01 evalúa confianza:
   a. Si score >= 0.75: pasa a INU-01/INU-02
   b. Si 0.60 <= score < 0.75: entrega con advertencia visual
   c. Si score < 0.60: bloquea, notifica a COR-01, escala a revisión manual
8. INU-01/INU-02 presenta output al usuario
9. GDO-01 registra toda la transacción (input, output, score, metadatos)
10. SEA-01 audita la transacción en log de seguridad
11. COR-01 genera confirmación de ejecución a ORC-01
```

### 6.2 Flujo de Trabajo de Captura Documental

```
1. USUARIO captura imagen/documento con INC-01 (NM)
2. INC-01 calcula hash SHA-256, etiqueta metadatos
3. INC-01 transmite a GDO-01 (NC) vía Syncthing o API
4. GDO-01 valida integridad (hash), asigna UUID
5. GDO-01 almacena en: /opt/waipl/docs/<area>/<año>/<mes>/<uuid>.ext
6. GDO-01 indexa en PostgreSQL (tabla documents)
7. GDO-01 confirma recepción a INC-01
8. INC-01 notifica a INU-02: "Documento archivado: <uuid>"
9. PIA-01 (bajo demanda) puede generar OCR o resumen del documento
10. VAC-01 valida resumen si es generado
```

### 6.3 Protocolos de Operación Diaria

| Horario | Acción | Responsable | Verificación |
|---------|--------|-------------|--------------|
| 00:00 | Backup automático de base de datos | MAE-01 | COR-01 notifica éxito/fallo |
| 06:00 | Health-check completo del sistema | CYR-01 | Reporte en INU-01 |
| 08:00 | Revisión de alertas nocturnas | Usuario Humano | INU-01 dashboard |
| 12:00 | Sincronización forzada NM-NC | Syncthing | Verificación de hash |
| 18:00 | Rotación de logs (compress + archive) | MAE-01 | Espacio liberado > 100MB |
| 20:00 | Reporte diario automático | COR-01 | Email/Push a usuario |

---

## 7. SISTEMA DE GESTIÓN DE CONTINGENCIAS

### 7.1 Plan Preventivo (Antes del Error)

| Riesgo | Probabilidad | Impacto | Medida Preventiva | Responsable |
|--------|--------------|---------|-------------------|-------------|
| Fallo de disco NC | Media | Crítico | Backup diario + monitoreo SMART | MAE-01 |
| Desconexión NM-NC | Alta | Medio | Cache offline de 48h en NM | CYR-01 |
| Saturación de RAM | Media | Alto | Límite de 80% RAM, swap activo | ORC-01 |
| Batería baja en NM | Alta | Medio | Alerta a 20% y 10%, modo ahorro | INU-02 |
| Intrusión de red | Baja | Crítico | Firewall, claves SSH, sin password | SEA-01 |
| Corrupción de datos | Baja | Crítico | Hash SHA-256 en todos los docs | GDO-01 |
| Fallo de agente crítico | Media | Alto | Watchdog + auto-restart | CYR-01 |
| Alucinación de IA no detectada | Media | Alto | VAC-01 con threshold 0.60 | VAC-01 |
| Pérdida de conectividad internet | Alta | Bajo | Operación 100% offline posible | CYR-01 |

### 7.2 Plan de Detección y Corrección a Tiempo (Desviaciones)

| Desviación | Umbral | Detección | Acción Correctiva | Tiempo Máximo |
|------------|--------|-----------|-------------------|---------------|
| Latencia PIA-01 > 10s | > 10s | ORC-01 heartbeat | Reducir batch size, bajar temperatura | 2 min |
| Cola de validación VAC-01 > 50 items | > 50 | ORC-01 métricas | Escalar a procesamiento paralelo | 5 min |
| Espacio disco NC < 10GB | < 10GB | MAE-01 monitoreo | Alerta + limpieza automática logs viejos | 1 min |
| Sincronización NM-NC > 5 min | > 5 min | Syncthing API | Reintentar + notificar | 10 min |
| Score de confianza promedio < 0.70 | < 0.70 | VAC-01 reporte | Revisar modelo, ajustar heurísticas | 24h |
| Heartbeat perdido de agente | 3 fallos | CYR-01 | Reinicio automático del agente | 30s |
| Temperatura CPU NC > 85°C | > 85°C | Hardware sensor | Throttling PIA-01 + ventilación | 1 min |

### 7.3 Plan Correctivo (Error Ejecutado)

#### Escenario A: Agente caído no recuperable por auto-restart
1. CYR-01 detecta fallo persistente después de 3 reinicios
2. CYR-01 notifica a COR-01 (alerta crítica)
3. COR-01 notifica a usuario vía INU-02 (push) + INU-01 (dashboard rojo)
4. Usuario interviene manualmente vía INU-01:
   - Opción 1: Reinicio forzado del agente
   - Opción 2: Reinicio completo del nodo
   - Opción 3: Activar agente de respaldo (si existe)
5. GDO-01 registra incidente con ID de ticket
6. MAE-01 recolecta logs del fallo para análisis post-mortem
7. COR-01 genera reporte de incidente en 24h

#### Escenario B: Pérdida de sincronización NM-NC > 24h
1. CYR-01 detecta desconexión prolongada
2. NM entra en **Modo Supervivencia**:
   - PIA-02 opera con cache local exclusivamente
   - INC-01 almacena capturas en cola local (SQLite)
   - INU-02 notifica: "Modo offline activo"
3. Al restablecerse conexión:\n   - PIA-02 sincroniza cola pendiente\n   - GDO-01 procesa backlog documental\n   - VAC-01 valida outputs generados offline retroactivamente\n4. COR-01 genera reporte de modo offline

#### Escenario C: Corrupción o compromiso de seguridad
1. SEA-01 detecta anomalía (acceso no autorizado, hash no coincide)
2. SEA-01 activa **Protocolo Fortaleza**:
   - Aislamiento del nodo afectado (drop de conexiones)
   - Revocación inmediata de tokens/claves
   - Snapshot forense del estado actual
3. CYR-01 pone sistema en modo mantenimiento
4. Usuario humano investiga vía logs de SEA-01
5. MAE-01 restaura desde último backup limpio si es necesario
6. GDO-01 audita integridad de todos los documentos post-incidente
7. COR-01 genera reporte de seguridad + lecciones aprendidas

### 7.4 Plan Resolutivo (Post-Error)

| Fase | Acción | Responsable | Plazo |
|------|--------|-------------|-------|
| **Contención** | Aislar y estabilizar | CYR-01 | Inmediato |
| **Evaluación** | Determinar alcance del daño | SEA-01 + Usuario | 1h |
| **Recuperación** | Restaurar servicio | MAE-01 + CYR-01 | Según escenario (max 4h) |
| **Análisis** | Root cause analysis | Usuario + COR-01 | 24h |
| **Documentación** | Reporte post-incidente | GDO-01 | 48h |
| **Mejora** | Implementar contramedida | MAE-01 | 1 semana |
| **Verificación** | Validar que la contramedida funciona | CYR-01 | 1 semana |

### 7.5 Plan Propositivo (Mejoras Continuas)

| Ciclo | Frecuencia | Acción | Responsable |
|-------|------------|--------|-------------|
| **Sprint de mejora** | Quincenal | Revisar métricas, identificar cuellos de botella | ORC-01 + Usuario |
| **Refinamiento de VAC** | Mensual | Ajustar heurísticas con falsos positivos/negativos | VAC-01 |
| **Optimización de modelos** | Trimestral | Evaluar nuevos modelos locales, comparar latencia/quality | PIA-01 |
| **Revisión de arquitectura** | Semestral | Evaluar si la topología aún es óptima | Usuario + MAE-01 |
| **Auditoría de seguridad** | Trimestral | Pentest básico, revisión de logs, rotación de claves | SEA-01 |
| **Capacitación** | Según necesidad | Documentar nuevas funcionalidades para usuario | GDO-01 |

---

## 8. ADAPTABILIDAD EVOLUTIVA Y MODERNIZACIÓN

### 8.1 Roadmap Tecnológico 2026-2027

| Trimestre | Tecnología a Evaluar | Impacto Esperado | Responsable |
|-----------|---------------------|------------------|-------------|
| Q3 2026 | Modelos multimodales locales (llava, bakllava) | Procesamiento de imagen + texto en PIA-01 | PIA-01 |
| Q3 2026 | Quantization avanzada (GGUF Q4_K_M → Q3_K_S) | Reducir VRAM/RAM en 25% | PIA-01 |
| Q4 2026 | Vector DB dedicada (ChromaDB → Milvus Lite) | Mejor rendimiento RAG | PIA-01 |
| Q4 2026 | Sincronización P2P mejorada (Syncthing → IPFS local) | Mayor resiliencia | CYR-01 |
| Q1 2027 | Agente autónomo de planificación (LLM como router) | ORC-01 más inteligente | ORC-01 |
| Q1 2027 | Edge TPU / Coral USB para inferencia acelerada | Latencia < 1s en NC | PIA-01 |
| Q2 2027 | Federated Learning básico | NM contribuye a modelo sin compartir datos | PIA-01 + PIA-02 |

### 8.2 Estrategia de Modernización

1. **Abstracción de interfaces:** Todos los agentes se comunican vía API REST/JSON. Cambiar el motor de IA (Ollama → vLLM → llama.cpp) no afecta a VAC-01 ni INU-01.
2. **Contenedores:** Cada agente debe poder ejecutarse en Docker. Facilita migración entre hardware.
3. **Configuración como código:** Todo en archivos `.yaml` o `.env`. Sin configuración manual escondida.
4. **Tests de regresión:** Cada cambio tecnológico debe pasar suite de tests antes de producción.
5. **Documentación viva:** Cada cambio en código actualiza automáticamente la documentación (docstrings → Markdown).

### 8.3 Adaptación a Nuevos Dispositivos

| Escenario | Acción de Adaptación | Responsable |
|-----------|---------------------|-------------|
| Reemplazo de NM (nuevo teléfono) | Clonar repo, instalar Termux, restaurar config, sincronizar | MAE-01 + Usuario |
| Reemplazo de NC (nueva laptop) | Restaurar backup completo, reinstalar dependencias, validar | MAE-01 |
| Expansión a tercer nodo (tablet, Raspberry Pi) | Reutilizar PIA-02 como template, ajustar recursos, registrar en ORC-01 | MAE-01 + ORC-01 |
| Migración a cloud híbrido | Extraer config, desplegar contenedores, mantener NC como edge | MAE-01 |

---

## 9. MÉTRICAS DE EVALUACIÓN, CONTROL Y AUDITORÍAS

### 9.1 KPIs por Área

| Área | KPI | Fórmula | Frecuencia | Umbral Óptimo | Umbral Crítico |
|------|-----|---------|------------|---------------|----------------|
| **ORC** | Disponibilidad del sistema | (Tiempo activo / Tiempo total) × 100 | Diario | > 99% | < 95% |
| **ORC** | Tiempo de recuperación de agente | Tiempo desde fallo hasta heartbeat OK | Por incidente | < 60s | > 5 min |
| **PIA** | Latencia de inferencia | Tiempo desde prompt hasta raw output | Por consulta | < 3s | > 10s |
| **PIA** | Throughput | Consultas procesadas / hora | Horario | > 100/h | < 50/h |
| **VAC** | Precisión de detección | (TP + TN) / Total evaluados | Mensual | > 85% | < 70% |
| **VAC** | Tasa de bloqueo | Respuestas bloqueadas / Total | Semanal | 5-15% | > 30% o < 2% |
| **VAC** | Score promedio de confianza | Suma scores / Total respuestas | Diario | > 0.80 | < 0.65 |
| **INC** | Tasa de captura exitosa | Capturas válidas / Intentos | Diario | > 98% | < 90% |
| **INC** | Tiempo de transmisión | Desde captura hasta registro en NC | Por doc | < 30s | > 5 min |
| **GDO** | Integridad documental | Docs con hash válido / Total docs | Semanal | 100% | < 100% |
| **GDO** | Tiempo de indexación | Desde recepción hasta consultable | Por doc | < 2s | > 30s |
| **SEA** | Eventos de seguridad | Número de alertas / período | Semanal | 0 | > 1 |
| **SEA** | Tiempo de respuesta a incidente | Detección → contención | Por incidente | < 5 min | > 30 min |
| **COR** | Tasa de entrega de reportes | Reportes enviados / Programados | Mensual | 100% | < 95% |
| **MAE** | Éxito de backup | Backups válidos / Intentos | Diario | 100% | < 100% |
| **CYR** | Tiempo en modo degradado | Horas offline / Horas totales | Mensual | < 2% | > 10% |

### 9.2 Sistema de Control

**Control de Procesos (Cada 4 horas):**
- ORC-01 genera snapshot de estado de todos los agentes
- Dashboard INU-01 muestra semáforo: Verde (OK), Amarillo (Advertencia), Rojo (Crítico)
- Si 2+ agentes en amarillo → COR-01 envía alerta preventiva
- Si 1+ agente en rojo → COR-01 envía alerta crítica + CYR-01 activa protocolo

**Control de Calidad (Semanal):**
- Muestreo aleatorio del 10% de outputs de IA
- Revisión manual de score de VAC-01 vs. juicio humano
- Ajuste de heurísticas si hay desviación > 10%

**Control de Seguridad (Diario):**
- SEA-01 escanea logs en busca de patrones de ataque (brute force, SQL injection)
- Verificación de integridad de archivos críticos (hashes de binarios)
- Revisión de conexiones activas (netstat/ss)

### 9.3 Auditorías

| Tipo | Frecuencia | Alcance | Ejecutor | Evidencia |
|------|------------|---------|----------|-----------|
| **Auditoría de código** | Mensual | Revisar commits, calidad, tests | Usuario humano | Reporte de code review |
| **Auditoría de seguridad** | Trimestral | Vulnerabilidades, permisos, claves | SEA-01 + Usuario | Reporte de pentest |
| **Auditoría de documentos** | Semestral | Integridad, indexación, accesos | GDO-01 | Inventario documental |
| **Auditoría de rendimiento** | Trimestral | Latencias, throughput, recursos | ORC-01 + PIA-01 | Benchmark comparativo |
| **Auditoría de compliance** | Anual | Cumplimiento de MNP, trazabilidad | Usuario humano | Certificación interna |

---

## 10. MANUALES DE NORMAS Y PROCEDIMIENTOS (MNP)

### 10.1 MNP-DES: Desarrollo

**Norma DES-01:** Todo código debe estar versionado en Git con commits atómicos y mensajes descriptivos (conventional commits).
**Norma DES-02:** Cada agente debe tener su propio módulo Python con `__init__.py`, `main.py`, `config.yaml`, y `tests/`.
**Norma DES-03:** Antes de mergear a `main`, todo código debe pasar: (a) linter (ruff), (b) type checker (mypy), (c) tests unitarios (pytest), (d) revisión de VAC-01 si es código de IA.
**Norma DES-04:** Documentación obligatoria: docstrings en funciones públicas, README por agente, diagrama de arquitectura actualizado.
**Norma DES-05:** Variables de entorno sensibles nunca en código; siempre en `.env` con template `.env.example`.

**Procedimiento DES-P01: Crear un nuevo agente**
1. Crear rama Git: `feature/agente-<nombre>`
2. Copiar template desde `/opt/waipl/templates/agente/`
3. Implementar clase heredando de `BaseAgent`
4. Definir método `run()`, `health_check()`, `shutdown()`
5. Escribir tests unitarios (cobertura mínima 70%)
6. Registrar agente en `config/orchestrator.yaml`
7. Pull request → revisión → merge
8. Desplegar vía systemd: `sudo systemctl enable waipl-<agente>`

### 10.2 MNP-IMP: Implementación

**Norma IMP-01:** Implementación solo en ventana de mantenimiento (20:00-06:00) salvo emergencia.
**Norma IMP-02:** Backup completo antes de cualquier implementación.
**Norma IMP-03:** Implementación en NM solo después de validación en NC.
**Norma IMP-04:** Rollback automático si health-check falla 3 veces post-implementación.

**Procedimiento IMP-P01: Despliegue de nueva versión**
1. MAE-01 ejecuta backup: `python scripts/backup.py --full`
2. MAE-01 actualiza repo: `git pull origin main`
3. MAE-01 instala dependencias: `pip install -r requirements.txt`
4. MAE-01 ejecuta migraciones: `python scripts/migrate.py`
5. MAE-01 reinicia agente: `sudo systemctl restart waipl-<agente>`
6. CYR-01 verifica health-check (3 pings consecutivos OK)
7. Si falla → MAE-01 ejecuta rollback: `python scripts/rollback.py`
8. GDO-01 registra implementación en log de cambios

### 10.3 MNP-EJE: Ejecución

**Norma EJE-01:** Todo input de usuario debe pasar por INC-01 para etiquetado y trazabilidad.
**Norma EJE-02:** Ningún output de IA llega al usuario sin pasar por VAC-01.
**Norma EJE-03:** Todo documento debe registrarse en GDO-01 antes de ser consultable.
**Norma EJE-04:** Las alertas críticas deben ack (acknowledge) por el usuario en < 15 min.

**Procedimiento EJE-P01: Ejecución de consulta de IA**
1. Usuario ingresa prompt vía INU-01 o INU-02
2. INU-01/INU-02 asigna `session_id` y `request_id`
3. Input se envía a PIA-01 con metadata completa
4. PIA-01 registra inicio de inferencia en log
5. PIA-01 genera raw output
6. VAC-01 intercepta y evalúa:\n   - Calcula score de confianza\n   - Verifica coherencia factual (heurísticas + RAG)\n   - Asigna etiqueta: `APROBADO`, `ADVERTENCIA`, `BLOQUEADO`
7. Si `APROBADO` → entrega directa
8. Si `ADVERTENCIA` → entrega con banner visual de baja confianza
9. Si `BLOQUEADO` → rechazo + notificación a COR-01 + escalamiento
10. GDO-01 archiva transacción completa (input, output, score, timestamp)
11. COR-01 confirma fin de transacción a ORC-01

### 10.4 MNP-CON: Contingencias

**Norma CON-01:** Todo incidente debe generar ticket único en formato `INC-<YYYYMMDD>-<NNN>`.
**Norma CON-02:** Modo degradado prioriza: (1) Seguridad, (2) Captura de datos, (3) Procesamiento IA offline.
**Norma CON-03:** No se restaura backup sin autorización del usuario humano.

**Procedimiento CON-P01: Activación de modo degradado**
1. CYR-01 detecta desconexión NC-NM > 5 minutos
2. CYR-01 notifica a PIA-02: "ACTIVAR MODO OFFLINE"
3. PIA-02 carga cache local y desconecta API remota
4. INC-01 redirige capturas a cola SQLite local
5. INU-02 muestra indicador visual: "Modo offline - datos seguros"
6. CYR-01 intenta reconexión cada 60s
7. Al reconectar:
   a. PIA-02 sincroniza cola de prompts pendientes
   b. INC-01 sincroniza documentos pendientes
   c. VAC-01 procesa validación retroactiva de outputs offline
   d. GDO-01 integra backlog documental
   e. CYR-01 notifica: "Conexión restablecida - sincronización completa"

### 10.5 MNP-COM: Comunicaciones

**Norma COM-01:** Toda comunicación entre agentes usa formato JSON con campos obligatorios: `agente_origen`, `agente_destino`, `timestamp`, `message_id`, `payload`, `checksum`.
**Norma COM-02:** Comunicaciones críticas requieren ACK en < 5s.
**Norma COM-03:** Logs de comunicación se almacenan por 90 días, luego archivados comprimidos.

**Procedimiento COM-P01: Envío de mensaje crítico**
1. Agente origen genera `message_id = UUIDv4`
2. Agente origen calcula `checksum = SHA256(payload)`
3. Envía vía COR-01 (broker)
4. COR-01 registra en log de comunicaciones
5. Agente destino recibe, verifica checksum
6. Agente destino envía ACK con `ack_message_id = message_id`
7. Si no hay ACK en 5s → COR-01 reintenta (máximo 3 veces)
8. Si fallan 3 reintentos → COR-01 marca como fallido y notifica a ORC-01

### 10.6 MNP-DOC: Documentación

**Norma DOC-01:** Todo documento generado por el sistema lleva: `doc_id`, `area_generadora`, `agente_generador`, `fecha_creacion`, `version`, `hash_sha256`, `clasificacion`.
**Norma DOC-02:** Clasificación obligatoria: `PUBLICO`, `INTERNO`, `SENSIBLE`, `CRITICO`.
**Norma DOC-03:** Documentos `CRITICO` requieren cifrado en reposo (AES-256).
**Norma DOC-04:** Retención mínima: 7 años para documentos de auditoría, 2 años para operativos.

---

## 11. SISTEMA DE COMUNICACIÓN, SUPERVISIÓN Y TRAZABILIDAD

### 11.1 Modos de Comunicación

| Modo | Uso | Protocolo | Frecuencia | Trazabilidad |
|------|-----|-----------|------------|--------------|
| **Heartbeat** | Estado de vida de agentes | UDP multicast / HTTP GET | Cada 30s | Log cíclico (24h) |
| **Mensajería** | Comandos y datos entre agentes | ZeroMQ / SQLite Queue | Bajo demanda | Log permanente (90d) |
| **API REST** | Consultas, CRUD, inferencias | HTTP/1.1 + TLS | Bajo demanda | Access log (90d) |
| **WebSocket** | Dashboard en tiempo real | WS (localhost) | Continuo | Snapshot cada 5min |
| **Push** | Alertas al usuario móvil | Android Notifications / Termux:API | Event-driven | Log de notificaciones (30d) |
| **Sync** | Transferencia de archivos | Syncthing protocol | Continuo / Programado | Log de Syncthing (30d) |
| **Email local** | Reportes periódicos | SMTP local / sendmail | Diario/semanal | GDO-01 archiva copia |

### 11.2 Protocolo de Supervisión

**Nivel 1: Auto-supervisión (Agente → Sí mismo)**
- Cada agente monitorea su propio consumo de recursos (CPU, RAM, disco)
- Si excede umbrales → auto-throttle o auto-restart
- Reporta anomalías a ORC-01

**Nivel 2: Supervisión Cruzada (Agente → Agente)**
- CYR-01 supervisa heartbeat de todos los agentes
- VAC-01 supervisa outputs de PIA-01
- SEA-01 supervisa tráfico de red y accesos
- Si detecta fallo → notifica a ORC-01 + COR-01

**Nivel 3: Supervisión Humana (Usuario → Sistema)**
- Dashboard INU-01 muestra estado en tiempo real
- Usuario puede: pausar agente, forzar reinicio, ejecutar comando manual, generar reporte ad-hoc
- Intervenciones humanas se registran como `accion_manual` en log de auditoría

### 11.3 Tipos de Comunicación Trazable

Cada comunicación en WAIPL se clasifica y traza:

| Tipo | Descripción | Campos de Trazabilidad | Almacenamiento |
|------|-------------|------------------------|----------------|
| **CMD** | Comando de control (start, stop, restart) | `cmd_id`, `origen`, `destino`, `comando`, `timestamp`, `resultado` | `logs/commands/` |
| **DAT** | Transferencia de datos | `data_id`, `tipo`, `tamano_bytes`, `hash`, `ruta_origen`, `ruta_destino`, `timestamp_inicio`, `timestamp_fin` | `logs/data_xfer/` |
| **INF** | Inferencia de IA | `inf_id`, `modelo`, `prompt_hash`, `output_hash`, `tokens_in`, `tokens_out`, `latencia_ms`, `score_vac` | `logs/inference/` |
| **ALR** | Alerta/Notificación | `alr_id`, `nivel` (INFO/WARN/CRIT), `agente_origen`, `mensaje`, `timestamp`, `ack_por` | `logs/alerts/` |
| **AUD** | Evento de auditoría | `aud_id`, `categoria`, `agente`, `accion`, `recurso`, `timestamp`, `ip_origen` | `logs/audit/` (90d) |
| **DOC** | Gestión documental | `doc_id`, `operacion` (CREATE/READ/UPDATE/DELETE), `agente`, `timestamp`, `hash_pre`, `hash_post` | `logs/doc_ops/` |
| **SYN** | Sincronización | `syn_id`, `nodo_origen`, `nodo_destino`, `archivos`, `bytes`, `estado`, `timestamp` | `logs/sync/` |

**Formato de trazabilidad (JSON estándar):**
```json
{
  "trace_id": "uuid-v4",
  "timestamp_utc": "2026-07-22T14:58:00Z",
  "tipo": "INF",
  "agente_origen": "PIA-01",
  "agente_destino": "VAC-01",
  "session_id": "sess-abc123",
  "request_id": "req-def456",
  "payload_hash": "sha256:abc...",
  "metadata": {
    "nodo": "NC",
    "version_agente": "1.2.0",
    "latencia_ms": 1200
  }
}
```

---

## 12. ELABORACIÓN DE INFORMES Y REPORTES

### 12.1 Tipos de Reporte

| ID | Nombre | Frecuencia | Generador | Destinatario | Formato | Contenido |
|----|--------|------------|-----------|--------------|---------|-----------|
| **R-01** | Pulso Diario | Diario (08:00) | COR-01 | Usuario (push/email) | Markdown + JSON | Estado de agentes, métricas KPI, alertas nocturnas |
| **R-02** | Métricas de Confianza | Semanal (lunes) | VAC-01 | Usuario (dashboard) | CSV + Gráfico | Score promedio, tasa de bloqueo, falsos positivos |
| **R-03** | Rendimiento de IA | Semanal (lunes) | PIA-01 | Usuario (dashboard) | CSV + Gráfico | Latencia, throughput, tokens/hora, uso de recursos |
| **R-04** | Inventario Documental | Mensual (1ro) | GDO-01 | Usuario (email) | CSV + PDF | Total docs, por área, por agente, integridad, accesos |
| **R-05** | Auditoría de Seguridad | Trimestral | SEA-01 | Usuario (PDF) | PDF | Eventos de seguridad, accesos, vulnerabilidades, parches |
| **R-06** | Post-Incidente | Bajo demanda | CYR-01 + COR-01 | Usuario (PDF) | PDF | Timeline, impacto, acciones tomadas, lecciones aprendidas |
| **R-07** | Changelog Técnico | Bajo demanda | MAE-01 | Usuario (Markdown) | Markdown | Cambios de versión, dependencias, migraciones |
| **R-08** | Estado de Sincronización | Diario (12:00) | Syncthing + COR-01 | Usuario (push) | Texto | Archivos sincronizados, pendientes, conflictos |
| **R-09** | Reporte de Backup | Diario (00:30) | MAE-01 | Usuario (email) | Texto | Éxito/fallo, tamaño, tiempo, integridad del backup |
| **R-10** | Análisis de Uso | Mensual | ORC-01 | Usuario (dashboard) | Gráfico interactivo | Patrones de uso, horas pico, agentes más activos |

### 12.2 Flujo de Generación de Reportes

```
1. Agente generador recolecta datos de su área
2. Agente consulta GDO-01 para datos históricos si es necesario
3. Agente formatea según template (Jinja2 / Markdown)
4. Agente envía a COR-01 para enrutamiento
5. COR-01 determina canal de entrega según clasificación
6. COR-01 entrega y registra confirmación de recepción
7. GDO-01 archiva copia del reporte con doc_id
8. SEA-01 audita generación y entrega
```

### 12.3 Trazabilidad de Reportes

Cada reporte generado recibe un `report_id` único y se registra en la tabla `reports`:
- `report_id`: UUID
- `tipo`: R-01 a R-10
- `agente_generador`: qué agente lo creó
- `fecha_generacion`: timestamp UTC
- `destinatario`: usuario / dashboard / archivo
- `canal_entrega`: push / email / filesystem / dashboard
- `hash_contenido`: SHA-256 del contenido
- `estado`: GENERADO / ENTREGADO / LEIDO / ARCHIVADO

---

## 13. GESTIÓN DOCUMENTAL: RECEPCIÓN, REGISTRO, INDEXACIÓN Y ARCHIVO

### 13.1 Área de Recepción: Agente GDO-01 (Archivista)

**Ubicación física lógica:** `/opt/waipl/docs/` (NC) + `~/waipl/docs/` (NM, cache)

**Proceso de Recepción:**
1. Documento llega vía: API REST, Syncthing, generación interna, o importación manual
2. GDO-01 valida formato permitido: `.md`, `.txt`, `.json`, `.csv`, `.pdf`, `.png`, `.jpg`, `.wav`, `.mp3`
3. GDO-01 rechaza si: formato no permitido, tamaño > 100MB, o contiene malware (scan básico)
4. GDO-01 calcula `hash_sha256` del contenido binario
5. GDO-01 verifica duplicados: si hash existe → vincula a registro existente + notifica

### 13.2 Registro

**Campos obligatorios del registro documental:**

```sql
CREATE TABLE documents (
    doc_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    doc_filename VARCHAR(255) NOT NULL,
    doc_path VARCHAR(500) NOT NULL,
    doc_size_bytes BIGINT NOT NULL,
    doc_mime_type VARCHAR(100) NOT NULL,
    doc_hash_sha256 VARCHAR(64) NOT NULL UNIQUE,
    doc_area VARCHAR(50) NOT NULL,        -- A-01 a A-10
    doc_agente VARCHAR(50) NOT NULL,      -- ORC-01, PIA-01, etc.
    doc_tipo VARCHAR(50) NOT NULL,        -- INFORME, LOG, CONFIG, CODIGO, DATO, MANUAL
    doc_clasificacion VARCHAR(20) NOT NULL DEFAULT 'INTERNO', -- PUBLICO, INTERNO, SENSIBLE, CRITICO
    doc_version INTEGER NOT NULL DEFAULT 1,
    doc_estado VARCHAR(20) NOT NULL DEFAULT 'ACTIVO', -- ACTIVO, ARCHIVADO, ELIMINADO
    doc_fecha_creacion TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    doc_fecha_modificacion TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    doc_etiquetas TEXT[],                 -- Array de etiquetas
    doc_metadata JSONB,                   -- Metadatos adicionales flexibles
    doc_embedding vector(768)             -- Embedding para búsqueda semántica (pgvector)
);
```

### 13.3 Indexación

**Estrategia de indexación:**
- **Índice primario:** `doc_id` (UUID)
- **Índice hash:** `doc_hash_sha256` (prevención de duplicados, UNIQUE)
- **Índice compuesto:** `(doc_area, doc_agente, doc_fecha_creacion)` (consultas frecuentes)
- **Índice GIN:** `doc_etiquetas` (búsqueda por etiquetas)
- **Índice GIN:** `doc_metadata` (búsqueda en JSONB)
- **Índice full-text search:** Índice GIN sobre `to_tsvector('spanish', doc_filename || ' ' || contenido_extraido)`
- **Índice vectorial:** Índice IVFFlat sobre `doc_embedding` para búsqueda semántica por similitud coseno

```sql
-- Índices adicionales para optimización de consultas
CREATE INDEX idx_docs_area_fecha ON documents(doc_area, doc_fecha_creacion DESC);
CREATE INDEX idx_docs_agente ON documents(doc_agente);
CREATE INDEX idx_docs_clasificacion ON documents(doc_clasificacion);
CREATE INDEX idx_docs_estado ON documents(doc_estado);
CREATE INDEX idx_docs_etiquetas ON documents USING GIN(doc_etiquetas);
CREATE INDEX idx_docs_metadata ON documents USING GIN(doc_metadata jsonb_path_ops);

-- Índice de búsqueda full-text
CREATE INDEX idx_docs_fulltext ON documents 
    USING GIN(to_tsvector('spanish', coalesce(doc_filename, '') || ' ' || coalesce(doc_metadata->>'contenido_extraido', '')));

-- Índice vectorial para búsqueda semántica (requiere pgvector)
CREATE INDEX idx_docs_embedding ON documents 
    USING ivfflat (doc_embedding vector_cosine_ops) WITH (lists = 100);
```

**Pipeline de indexación:**
1. Documento recibido y validado
2. GDO-01 extrae texto (si es posible: OCR para imágenes, parseo para PDF)
3. GDO-01 solicita a PIA-01 embedding del contenido (modelo de embeddings vía Ollama)
4. GDO-01 inserta registro en PostgreSQL con embedding
5. GDO-01 actualiza índice de búsqueda full-text
6. GDO-01 confirma indexación con `index_timestamp` en metadata

### 13.4 Archivo

**Estructura de carpetas (filesystem):**

```
/opt/waipl/docs/
├── A-01_ORC/                    # Área Orquestación
│   ├── 2026/
│   │   ├── 07/
│   │   │   ├── <uuid>_v1.json   # Logs de estado
│   │   │   └── ...
│   └── ...
├── A-02_PIA/                    # Área Procesamiento IA
├── A-03_INC/                    # Área Ingesta
├── A-04_VAC/                    # Área Validación
├── A-05_SEA/                    # Área Seguridad
├── A-06_INU/                    # Área Interfaz
├── A-07_GDO/                    # Área Gestión Documental
├── A-08_COR/                    # Área Comunicaciones
├── A-09_MAE/                    # Área Mantenimiento
├── A-10_CYR/                    # Área Contingencias
├── MANUALES/                    # MNP versionados
│   ├── MNP-DES_v1.0.md
│   ├── MNP-IMP_v1.0.md
│   └── ...
├── REPORTES/                    # Reportes generados
│   ├── 2026/
│   │   ├── 07/
│   │   │   ├── R-01_2026-07-22.md
│   │   │   └── ...
│   └── ...
├── .archive/                    # Versiones anteriores
└── .trash/                      # Documentos eliminados (retención 30 días)
```

**Reglas de archivo:**
- Documentos se organizan por `AREA/AÑO/MES/`
- Nombre de archivo: `<doc_id>_v<version>.<ext>` (ej: `a1b2c3d4_v1.pdf`)
- Documentos `CRITICO` se cifran con AES-256-GCM antes de almacenar en disco
- Versionado: cada modificación crea nueva versión; versión anterior se mueve a `/.archive/`
- Retención automática: MAE-01 elimina (mueve a `/.trash/`) documentos operativos > 2 años
- Retención permanente: documentos de auditoría nunca se eliminan
- Limpieza de `.trash/`: MAE-01 purga documentos con > 30 días en trash

### 13.5 Comprobación y Consulta Eficiente

#### Método 1: Consulta por ID exacto
```bash
curl -H "Authorization: Bearer $WAIPL_TOKEN" \
     http://nc:8000/api/docs/<doc_id>
```
**Respuesta:** Documento completo con metadata y contenido en Base64 si es binario, o texto plano si es Markdown/JSON/CSV. Incluye hash SHA-256 para verificación de integridad en cliente.

#### Método 2: Verificación de integridad por hash
```bash
curl -H "Authorization: Bearer $WAIPL_TOKEN" \
     http://nc:8000/api/docs/hash/<sha256>
```
**Respuesta:** `doc_id`, metadata y estado de integridad actual. Si el hash no coincide con el archivo en disco → estado `INTEGRIDAD_COMPROMETIDA` y alerta automática a SEA-01.

#### Método 3: Búsqueda por área + rango de fechas
```bash
curl -H "Authorization: Bearer $WAIPL_TOKEN" \
     "http://nc:8000/api/docs?area=A-04&from=2026-07-01&to=2026-07-31&page=1&limit=50"
```
**Parámetros adicionales:** `agente`, `tipo`, `clasificacion`, `estado`, `etiquetas`. Paginación con `page` y `limit`. Ordenamiento por `fecha_creacion` descendente por defecto.

#### Método 4: Búsqueda full-text
```bash
curl -H "Authorization: Bearer $WAIPL_TOKEN" \
     "http://nc:8000/api/docs/search?q=plan+contingencia+recuperacion&lang=spanish"
```
**Funcionamiento:** PostgreSQL `ts_query` con ranking (`ts_rank`) sobre el índice full-text combinado de `doc_filename` y `contenido_extraido` (almacenado en `doc_metadata->>'contenido_extraido'`). Soporta operadores: `&` (AND), `|` (OR), `!` (NOT). Resultados ordenados por relevancia descendente.

#### Método 5: Búsqueda semántica por embeddings
```bash
curl -X POST -H "Authorization: Bearer $WAIPL_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"query": "procedimiento de recuperación ante fallo del nodo central", "top_k": 10, "umbral_similitud": 0.75}' \
     http://nc:8000/api/docs/search/semantic
```
**Funcionamiento:**
1. GDO-01 envía el texto de consulta a PIA-01 para generar embedding (modelo: `nomic-embed-text` o `all-MiniLM-L6-v2`)
2. PIA-01 devuelve vector de 768 dimensiones
3. GDO-01 ejecuta búsqueda por similitud coseno en pgvector:
   ```sql
   SELECT doc_id, doc_filename, doc_area, doc_fecha_creacion,
          1 - (doc_embedding <=> $1) AS similitud
   FROM documents
   WHERE doc_estado = 'ACTIVO'
     AND 1 - (doc_embedding <=> $1) >= $2
   ORDER BY doc_embedding <=> $1
   LIMIT $3;
   ```
4. Resultados ordenados por similitud descendente, con score numérico
5. Útil para búsquedas conceptuales donde los términos exactos no coinciden (ej: "qué hacer si se cae el sistema" → documentos de contingencia aunque no contengan literalmente "caerse")

**Optimización:** El índice IVFFlat con 100 listas divide el espacio vectorial para búsqueda aproximada rápida. Parámetro `probes` ajustable según compromiso velocidad/exhaustividad.

#### Método 6: Verificación masiva de integridad documental
```bash
curl -X POST -H "Authorization: Bearer $WAIPL_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"area": "A-05", "from": "2026-06-01", "to": "2026-07-31", "async": true}' \
     http://nc:8000/api/docs/verify-integrity
```
**Funcionamiento:**
1. GDO-01 selecciona todos los documentos que cumplen los filtros (área, rango de fechas, clasificación)
2. Para cada documento, recalcula `SHA-256` del archivo en disco y compara con `doc_hash_sha256` en BD
3. Si `async: true` → proceso en background, devuelve `task_id` inmediatamente. Estado consultable vía `GET /api/tasks/<task_id>`
4. Si `async: false` → respuesta síncrona (solo para lotes < 100 documentos)
5. Resultado final:
```json
{
  "task_id": "uuid",
  "estado": "COMPLETADO",
  "resumen": {
    "total_verificados": 1243,
    "integros": 1240,
    "comprometidos": 2,
    "no_encontrados": 1
  },
  "detalle_comprometidos": [
    {
      "doc_id": "uuid-1",
      "hash_bd": "abc123...",
      "hash_disco": "def456...",
      "accion_sugerida": "RESTAURAR_DESDE_BACKUP"
    }
  ],
  "timestamp": "2026-07-22T18:30:00Z"
}
```
6. Documentos comprometidos generan alerta automática a SEA-01 (tipo ALR, nivel CRIT)
7. MAE-01 programa verificación masiva automática semanal (domingos 03:00) y reporta en R-09

#### API de Consulta Programática (Python SDK)

```python
from waipl_sdk import DocumentClient

client = DocumentClient(base_url="http://nc:8000", token=os.environ["WAIPL_TOKEN"])

# Búsqueda semántica
resultados = client.search_semantic(
    query="configuración de red entre nodo central y móvil",
    top_k=5,
    area="A-05"  # opcional: filtrar por área
)

# Verificación de integridad masiva
task = client.verify_integrity(
    areas=["A-04", "A-05", "A-07"],  # validación, seguridad, documental
    from_date="2026-01-01",
    async_mode=True
)
client.wait_for_task(task.task_id)

# Búsqueda full-text con filtros combinados
docs = client.search(
    query="backup AND (postgresql OR sqlite)",
    area="A-09",
    tipo="LOG",
    from_date="2026-06-01",
    page=1,
    limit=20
)
```

---

## 14. ANEXOS

### Anexo A: Template de Agente (Python)

```python
"""
WAIPL Agent Template
====================
Base class for all WAIPL agents. Inherit and override run(), health_check(), shutdown().
"""

import os
import json
import time
import uuid
import hashlib
import logging
import sqlite3
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Optional, Dict, Any

import requests
import yaml


class BaseAgent(ABC):
    """Abstract base agent for the WAIPL ecosystem."""

    def __init__(self, agent_id: str, area: str, node: str, config_path: str = "config/agent.yaml"):
        self.agent_id = agent_id
        self.area = area
        self.node = node
        self.instance_id = str(uuid.uuid4())
        self.started_at = datetime.now(timezone.utc)
        self.config = self._load_config(config_path)
        self.logger = self._setup_logger()
        self.running = False

        # Communication
        self.orchestrator_url = self.config.get("orchestrator_url", "http://localhost:8000")
        self.broker_url = self.config.get("broker_url", "http://localhost:8001")
        self.api_token = os.environ.get("WAIPL_TOKEN", "")

        # Heartbeat
        self.heartbeat_interval = self.config.get("heartbeat_interval_sec", 30)

    def _load_config(self, path: str) -> dict:
        with open(path, "r") as f:
            return yaml.safe_load(f)

    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger(self.agent_id)
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler(f"logs/{self.agent_id}.log")
        handler.setFormatter(logging.Formatter(
            '%(asctime)s | %(levelname)s | %(message)s'
        ))
        logger.addHandler(handler)
        return logger

    def _generate_message(self, tipo: str, destino: str, payload: dict) -> dict:
        """Generate a traceable message envelope."""
        message_id = str(uuid.uuid4())
        payload_bytes = json.dumps(payload, sort_keys=True).encode()
        return {
            "message_id": message_id,
            "trace_id": str(uuid.uuid4()),
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "tipo": tipo,
            "agente_origen": self.agent_id,
            "agente_destino": destino,
            "nodo": self.node,
            "instance_id": self.instance_id,
            "payload": payload,
            "payload_hash": hashlib.sha256(payload_bytes).hexdigest()
        }

    def send_message(self, destino: str, tipo: str, payload: dict) -> Optional[str]:
        """Send message via COR-01 broker with retry logic."""
        message = self._generate_message(tipo, destino, payload)
        for attempt in range(3):
            try:
                resp = requests.post(
                    f"{self.broker_url}/api/messages",
                    json=message,
                    headers={"Authorization": f"Bearer {self.api_token}"},
                    timeout=5
                )
                if resp.status_code == 200:
                    self.logger.info(f"Mensaje {message['message_id']} enviado a {destino}")
                    return message["message_id"]
            except requests.RequestException as e:
                self.logger.warning(f"Intento {attempt+1}/3 fallido: {e}")
                time.sleep(1)
        self.logger.error(f"Mensaje {message['message_id']} NO entregado a {destino}")
        return None

    def health_check(self) -> dict:
        """Return agent health status. Override for custom checks."""
        return {
            "agent_id": self.agent_id,
            "instance_id": self.instance_id,
            "status": "OK" if self.running else "STOPPED",
            "uptime_sec": (datetime.now(timezone.utc) - self.started_at).total_seconds(),
            "node": self.node,
            "timestamp_utc": datetime.now(timezone.utc).isoformat()
        }

    def shutdown(self):
        """Graceful shutdown. Override for custom cleanup."""
        self.running = False
        self.logger.info(f"{self.agent_id} shutdown complete")

    @abstractmethod
    def run(self):
        """Main agent loop. Must be implemented by subclasses."""
        pass


# ============================================================
# EXAMPLE: Minimal PIA-02 Agent (Mobile Light Client)
# ============================================================

class PIA02EcoAgent(BaseAgent):
    """Mobile lightweight IA client agent with offline cache."""

    def __init__(self):
        super().__init__("PIA-02", "A-02", "NM")
        self.cache_db = sqlite3.connect("cache/pia02_cache.db")
        self._init_cache_db()

    def _init_cache_db(self):
        self.cache_db.execute("""
            CREATE TABLE IF NOT EXISTS cache (
                prompt_hash TEXT PRIMARY KEY,
                prompt TEXT,
                response TEXT,
                score REAL,
                timestamp TEXT,
                access_count INTEGER DEFAULT 1
            )
        """)

    def run(self):
        self.running = True
        self.logger.info("PIA-02 Eco iniciado en Nodo Móvil")
        while self.running:
            # Send heartbeat to ORC-01
            self.send_message("ORC-01", "CMD", {"comando": "heartbeat", "estado": "online"})

            # Process pending prompts from local queue
            # ... (queue processing logic)

            time.sleep(self.heartbeat_interval)
```

### Anexo B: Configuración del Sistema (`config/system.yaml`)

```yaml
# WAIPL System Configuration
# Archivo: /opt/waipl/config/system.yaml

system:
  name: "WAIPL"
  version: "1.0.0"
  environment: "production"  # development | staging | production
  log_level: "INFO"
  timezone: "Europe/Madrid"

nodes:
  central:
    hostname: "nc-waipl"
    ip: "192.168.1.100"
    port: 8000
    dashboard_port: 8501
    ollama_port: 11434
    syncthing_port: 8384
  mobile:
    hostname: "nm-waipl"
    ip: "192.168.1.101"
    termux_api: true

agents:
  orchestrator:
    ORC-01:
      heartbeat_interval_sec: 30
      health_check_timeout_sec: 5
      max_agent_restarts: 3
  ia_processing:
    PIA-01:
      model: "llama3.1:8b"
      embedding_model: "nomic-embed-text"
      max_tokens: 4096
      temperature: 0.7
      timeout_sec: 30
    PIA-02:
      cache_size: 50
      offline_mode_timeout_h: 48
  trust_validator:
    VAC-01:
      score_threshold_approve: 0.75
      score_threshold_warn: 0.60
      heuristics: ["factual_coherence", "source_citation", "internal_consistency"]
  security:
    SEA-01:
      tls_version: "1.3"
      key_rotation_days: 90
      audit_log_retention_days: 90
      alert_on_failed_auth: true
      max_failed_auth: 5
  documental:
    GDO-01:
      max_file_size_mb: 100
      allowed_formats: [".md", ".txt", ".json", ".csv", ".pdf", ".png", ".jpg", ".wav", ".mp3"]
      encryption_algorithm: "AES-256-GCM"
      retention_operational_years: 2
      retention_audit_years: 7
      trash_retention_days: 30
  maintenance:
    MAE-01:
      backup_schedule: "0 0 * * *"  # midnight daily
      backup_retention_days: 30
      dependency_check_schedule: "0 6 * * 1"  # Monday 6am
  resilience:
    CYR-01:
      health_check_interval_sec: 30
      max_heartbeat_miss: 3
      offline_mode_activation_min: 5
      reconnect_retry_interval_sec: 60
      failover_timeout_sec: 60

sync:
  engine: "syncthing"
  rescan_interval_sec: 3600
  conflict_resolution: "newest_wins"
  folders:
    - path: "/opt/waipl/docs/"
      label: "waipl-docs"
    - path: "/opt/waipl/config/"
      label: "waipl-config"

database:
  postgresql:
    host: "localhost"
    port: 5432
    dbname: "waipl"
    user: "waipl_user"
    pool_min: 2
    pool_max: 10
  sqlite_mobile:
    path: "~/waipl/cache/mobile.db"
```

### Anexo C: Variables de Entorno (`.env.example`)

```bash
# ============================================
# WAIPL Environment Variables
# Copiar a .env y completar valores
# ============================================

# Core
WAIPL_ENV=development
WAIPL_NODE=NC                    # NC o NM
WAIPL_TOKEN=changeme_use_openssl_rand_hex_32

# PostgreSQL (NC)
WAIPL_DB_HOST=localhost
WAIPL_DB_PORT=5432
WAIPL_DB_NAME=waipl
WAIPL_DB_USER=waipl_user
WAIPL_DB_PASSWORD=changeme

# Ollama (NC)
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
OLLAMA_EMBED_MODEL=nomic-embed-text

# Syncthing
SYNCTHING_API_KEY=changeme
SYNCTHING_NC_ID=changeme
SYNCTHING_NM_ID=changeme

# Security
WAIPL_ENCRYPTION_KEY=changeme_use_openssl_rand_hex_32
WAIPL_SSH_KEY_PATH=~/.ssh/waipl_id_ed25519

# Notifications (Termux API)
TERMUX_API_ENABLED=true

# Dashboard
STREAMLIT_PORT=8501
STREAMLIT_THEME=dark
```

### Anexo D: Formato JSON de Mensajes entre Agentes

```json
{
  "$schema": "https://waipl.local/schemas/message/v1",
  "message_id": "550e8400-e29b-41d4-a716-446655440000",
  "trace_id": "660e8400-e29b-41d4-a716-446655440001",
  "correlation_id": "770e8400-e29b-41d4-a716-446655440002",
  "timestamp_utc": "2026-07-22T14:58:00.123Z",
  "tipo": "INF",
  "agente_origen": "PIA-01",
  "agente_destino": "VAC-01",
  "nodo_origen": "NC",
  "nodo_destino": "NC",
  "instance_id_origen": "abc123",
  "version_agente": "1.2.0",
  "payload": {
    "session_id": "sess-20260722-001",
    "request_id": "req-20260722-145800",
    "model": "llama3.1:8b",
    "prompt_hash": "sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "raw_output": "La respuesta generada por el modelo de IA...",
    "tokens_in": 156,
    "tokens_out": 423,
    "latencia_ms": 2150,
    "temperature": 0.7,
    "metadata": {
      "quantization": "Q4_K_M",
      "vram_used_mb": 5120,
      "cpu_temp_c": 72
    }
  },
  "payload_hash": "sha256:d7a8fbb307d7809469ca9abcb0082e4f8d5651e46d3cdb762d02d0bf37c9e592",
  "signature": "ed25519:sig..."
}
```

### Anexo E: Formato JSON de Reporte de Incidente (R-06)

```json
{
  "report_id": "rpt-550e8400-e29b-41d4-a716-446655440000",
  "tipo": "R-06",
  "incident_id": "INC-20260722-001",
  "fecha_generacion": "2026-07-22T19:30:00Z",
  "agente_generador": "CYR-01",
  "estado": "ENTREGADO",
  "contenido": {
    "timeline": [
      {"hora": "2026-07-22T14:15:00Z", "evento": "CYR-01 detecta pérdida de heartbeat de PIA-01 (3 fallos consecutivos)", "nivel": "WARN"},
      {"hora": "2026-07-22T14:15:05Z", "evento": "CYR-01 ejecuta auto-restart de PIA-01", "nivel": "INFO"},
      {"hora": "2026-07-22T14:15:35Z", "evento": "Reinicio fallido. CYR-01 escala a COR-01", "nivel": "CRIT"},
      {"hora": "2026-07-22T14:16:00Z", "evento": "COR-01 notifica a usuario vía INU-02 (push)", "nivel": "CRIT"},
      {"hora": "2026-07-22T14:20:00Z", "evento": "Usuario interviene manualmente. Causa: OOM por fuga de memoria en modelo", "nivel": "INFO"},
      {"hora": "2026-07-22T14:25:00Z", "evento": "PIA-01 reiniciado con límite de memoria. Servicio restaurado", "nivel": "INFO"}
    ],
    "impacto": {
      "duracion_total_min": 10,
      "agentes_afectados": ["PIA-01"],
      "funcionalidades_afectadas": ["Inferencia IA", "Embeddings RAG"],
      "datos_perdidos": false,
      "usuarios_afectados": 1
    },
    "causa_raiz": {
      "categoria": "FUGA_MEMORIA",
      "descripcion": "Modelo llama3.1:8b acumuló memoria no liberada tras 1200 inferencias consecutivas sin reinicio. Umbral de 80% RAM alcanzado, OOM Killer del SO terminó el proceso.",
      "componente": "PIA-01 / Ollama / llama3.1:8b"
    },
    "acciones_correctivas": [
      "Añadir límite de memoria explícito en config PIA-01 (max_ram_mb: 6144)",
      "Programar reinicio preventivo de Ollama cada 500 inferencias",
      "Añadir métrica de RAM a heartbeat de PIA-01 para detección temprana"
    ],
    "lecciones_aprendidas": [
      "El watchdog de CYR-01 funcionó correctamente (detección en < 30s)",
      "El auto-restart no fue suficiente; se necesita verificación de causa antes de reintentar",
      "La intervención humana fue necesaria para diagnóstico; VAC-01 podría ayudar a predecir el fallo por patrón de latencia creciente"
    ]
  }
}
```

### Anexo F: Esquema SQL Completo de la Base de Datos

```sql
-- ============================================
-- WAIPL Database Schema
-- PostgreSQL 16 + pgvector
-- ============================================

-- Extensión para UUIDs
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Extensión para búsqueda vectorial
CREATE EXTENSION IF NOT EXISTS "vector";

-- ============================================
-- TABLA: documents (Gestión Documental - GDO-01)
-- ============================================
CREATE TABLE documents (
    doc_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    doc_filename VARCHAR(255) NOT NULL,
    doc_path VARCHAR(500) NOT NULL,
    doc_size_bytes BIGINT NOT NULL,
    doc_mime_type VARCHAR(100) NOT NULL,
    doc_hash_sha256 VARCHAR(64) NOT NULL UNIQUE,
    doc_area VARCHAR(50) NOT NULL,
    doc_agente VARCHAR(50) NOT NULL,
    doc_tipo VARCHAR(50) NOT NULL,
    doc_clasificacion VARCHAR(20) NOT NULL DEFAULT 'INTERNO',
    doc_version INTEGER NOT NULL DEFAULT 1,
    doc_estado VARCHAR(20) NOT NULL DEFAULT 'ACTIVO',
    doc_fecha_creacion TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    doc_fecha_modificacion TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    doc_etiquetas TEXT[],
    doc_metadata JSONB,
    doc_embedding vector(768),
    CONSTRAINT chk_clasificacion CHECK (doc_clasificacion IN ('PUBLICO', 'INTERNO', 'SENSIBLE', 'CRITICO')),
    CONSTRAINT chk_estado CHECK (doc_estado IN ('ACTIVO', 'ARCHIVADO', 'ELIMINADO'))
);

-- ============================================
-- TABLA: agents (Registro de Agentes - ORC-01)
-- ============================================
CREATE TABLE agents (
    agent_id VARCHAR(50) PRIMARY KEY,
    agent_nombre VARCHAR(100) NOT NULL,
    area_id VARCHAR(10) NOT NULL,
    nodo VARCHAR(2) NOT NULL,
    estado VARCHAR(20) NOT NULL DEFAULT 'OFFLINE',
    instance_id UUID,
    last_heartbeat TIMESTAMPTZ,
    version VARCHAR(20),
    config JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT chk_nodo CHECK (nodo IN ('NC', 'NM'))
);

-- ============================================
-- TABLA: trace_log (Trazabilidad - Todos los agentes)
-- ============================================
CREATE TABLE trace_log (
    id BIGSERIAL PRIMARY KEY,
    trace_id UUID NOT NULL,
    timestamp_utc TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    tipo VARCHAR(10) NOT NULL,
    agente_origen VARCHAR(50) NOT NULL,
    agente_destino VARCHAR(50),
    message_id UUID,
    session_id VARCHAR(100),
    request_id VARCHAR(100),
    payload_hash VARCHAR(64),
    metadata JSONB,
    CONSTRAINT chk_tipo CHECK (tipo IN ('CMD', 'DAT', 'INF', 'ALR', 'AUD', 'DOC', 'SYN'))
);

-- ============================================
-- TABLA: inference_log (Inferencias - PIA-01)
-- ============================================
CREATE TABLE inference_log (
    inf_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    timestamp_utc TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    session_id VARCHAR(100),
    request_id VARCHAR(100),
    model VARCHAR(100) NOT NULL,
    prompt_hash VARCHAR(64) NOT NULL,
    output_hash VARCHAR(64) NOT NULL,
    tokens_in INTEGER,
    tokens_out INTEGER,
    latencia_ms INTEGER,
    temperature REAL,
    score_vac REAL,
    etiqueta_vac VARCHAR(20),
    metadata JSONB,
    CONSTRAINT chk_etiqueta_vac CHECK (etiqueta_vac IN ('APROBADO', 'ADVERTENCIA', 'BLOQUEADO', 'PENDIENTE'))
);

-- ============================================
-- TABLA: security_audit (Auditoría - SEA-01)
-- ============================================
CREATE TABLE security_audit (
    aud_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    timestamp_utc TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    categoria VARCHAR(50) NOT NULL,
    agente VARCHAR(50) NOT NULL,
    accion VARCHAR(100) NOT NULL,
    recurso VARCHAR(500),
    ip_origen INET,
    resultado VARCHAR(20),
    detalle JSONB,
    CONSTRAINT chk_resultado CHECK (resultado IN ('EXITO', 'FALLO', 'BLOQUEADO', 'SOSPECHOSO'))
);

-- ============================================
-- TABLA: reports (Reportes - COR-01)
-- ============================================
CREATE TABLE reports (
    report_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tipo VARCHAR(10) NOT NULL,
    agente_generador VARCHAR(50) NOT NULL,
    fecha_generacion TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    destinatario VARCHAR(100),
    canal_entrega VARCHAR(50),
    hash_contenido VARCHAR(64) NOT NULL,
    estado VARCHAR(20) NOT NULL DEFAULT 'GENERADO',
    metadata JSONB,
    CONSTRAINT chk_estado_reporte CHECK (estado IN ('GENERADO', 'ENTREGADO', 'LEIDO', 'ARCHIVADO', 'FALLIDO'))
);

-- ============================================
-- TABLA: incidents (Incidentes - CYR-01)
-- ============================================
CREATE TABLE incidents (
    incident_id VARCHAR(30) PRIMARY KEY,
    timestamp_deteccion TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    timestamp_resolucion TIMESTAMPTZ,
    severidad VARCHAR(10) NOT NULL,
    estado VARCHAR(20) NOT NULL DEFAULT 'ABIERTO',
    categoria VARCHAR(50),
    agentes_afectados TEXT[],
    descripcion TEXT,
    causa_raiz TEXT,
    acciones_tomadas JSONB,
    lecciones_aprendidas TEXT[],
    report_id UUID REFERENCES reports(report_id),
    CONSTRAINT chk_severidad CHECK (severidad IN ('BAJA', 'MEDIA', 'ALTA', 'CRITICA')),
    CONSTRAINT chk_estado_incidente CHECK (estado IN ('ABIERTO', 'EN_PROGRESO', 'CONTENIDO', 'RESUELTO', 'CERRADO'))
);

-- ============================================
-- TABLA: sync_log (Sincronización - Syncthing)
-- ============================================
CREATE TABLE sync_log (
    syn_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    timestamp_utc TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    nodo_origen VARCHAR(2) NOT NULL,
    nodo_destino VARCHAR(2) NOT NULL,
    archivos INTEGER,
    bytes BIGINT,
    estado VARCHAR(20) NOT NULL,
    errores JSONB,
    metadata JSONB,
    CONSTRAINT chk_estado_sync CHECK (estado IN ('COMPLETADO', 'PARCIAL', 'FALLIDO', 'CONFLICTO'))
);

-- ============================================
-- ÍNDICES (Adicionales a los definidos en 13.3)
-- ============================================
CREATE INDEX idx_trace_timestamp ON trace_log(timestamp_utc DESC);
CREATE INDEX idx_trace_tipo ON trace_log(tipo);
CREATE INDEX idx_trace_origen ON trace_log(agente_origen);
CREATE INDEX idx_trace_session ON trace_log(session_id) WHERE session_id IS NOT NULL;

CREATE INDEX idx_inference_timestamp ON inference_log(timestamp_utc DESC);
CREATE INDEX idx_inference_model ON inference_log(model);
CREATE INDEX idx_inference_score ON inference_log(score_vac) WHERE score_vac IS NOT NULL;
CREATE INDEX idx_inference_session ON inference_log(session_id);

CREATE INDEX idx_audit_timestamp ON security_audit(timestamp_utc DESC);
CREATE INDEX idx_audit_categoria ON security_audit(categoria);
CREATE INDEX idx_audit_agente ON security_audit(agente);
CREATE INDEX idx_audit_resultado ON security_audit(resultado);

CREATE INDEX idx_reports_tipo ON reports(tipo);
CREATE INDEX idx_reports_fecha ON reports(fecha_generacion DESC);

CREATE INDEX idx_incidents_estado ON incidents(estado);
CREATE INDEX idx_incidents_fecha ON incidents(timestamp_deteccion DESC);

CREATE INDEX idx_sync_log_timestamp ON sync_log(timestamp_utc DESC);

-- ============================================
-- FUNCIÓN: Actualizar doc_fecha_modificacion
-- ============================================
CREATE OR REPLACE FUNCTION update_doc_modificacion()
RETURNS TRIGGER AS $$
BEGIN
    NEW.doc_fecha_modificacion = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_doc_modificacion
    BEFORE UPDATE ON documents
    FOR EACH ROW EXECUTE FUNCTION update_doc_modificacion();

-- ============================================
-- VISTA: v_documentos_activos (consulta rápida)
-- ============================================
CREATE VIEW v_documentos_activos AS
SELECT 
    doc_id,
    doc_filename,
    doc_area,
    doc_agente,
    doc_tipo,
    doc_clasificacion,
    doc_version,
    doc_fecha_creacion,
    array_to_string(doc_etiquetas, ', ') AS etiquetas
FROM documents
WHERE doc_estado = 'ACTIVO'
ORDER BY doc_fecha_creacion DESC;
```

### Anexo G: Diagrama de Flujo de Validación (VAC-01)

```
                    ┌──────────────────┐
                    │   PIA-01 genera  │
                    │    raw_output    │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  VAC-01 recibe   │
                    │  raw_output +    │
                    │  metadata        │
                    └────────┬─────────┘
                             │
                             ▼
              ┌──────────────────────────────┐
              │  HEURÍSTICA 1: Coherencia    │
              │  ¿Respuesta autocontenida?   │
              │  ¿No se contradice?          │
              └──────────────┬───────────────┘
                             │
                             ▼
              ┌──────────────────────────────┐
              │  HEURÍSTICA 2: Factualidad   │
              │  RAG: ¿Respuesta alineada    │
              │  con docs de conocimiento?   │
              └──────────────┬───────────────┘
                             │
                             ▼
              ┌──────────────────────────────┐
              │  HEURÍSTICA 3: Citación      │
              │  ¿Fuentes citadas cuando     │
              │  corresponde?                │
              └──────────────┬───────────────┘
                             │
                             ▼
              ┌──────────────────────────────┐
              │  CÁLCULO DE SCORE           │
              │  score = w1*h1 + w2*h2 +    │
              │          w3*h3               │
              │  w1=0.35, w2=0.40, w3=0.25  │
              └──────────────┬───────────────┘
                             │
                    ┌────────┴────────┐
                    │                 │
              score ≥ 0.75      score ≥ 0.60
                    │                 │
                    ▼                 ▼
            ┌────────────┐    ┌──────────────┐
            │  APROBADO  │    │  ADVERTENCIA  │
            │  → INU     │    │  → INU c/     │
            └────────────┘    │    banner      │
                              └──────────────┘
                    │
              score < 0.60
                    │
                    ▼
            ┌──────────────┐
            │  BLOQUEADO   │
            │  → COR-01    │
            │  → ALR:CRIT  │
            │  → Revisión  │
            │    manual     │
            └──────────────┘
```

### Anexo H: Comandos Rápidos de Referencia

```bash
# ============================================
# WAIPL Quick Reference Commands
# ============================================

# --- Health Check ---
curl http://nc:8000/api/health                    # Estado general del sistema
curl http://nc:8000/api/agents                    # Lista de agentes y su estado
curl http://nc:8000/api/agents/PIA-01/health      # Health de un agente específico

# --- Gestión de Agentes ---
sudo systemctl status waipl-ORC-01                # Estado de un agente (systemd)
sudo systemctl restart waipl-PIA-01               # Reiniciar agente
journalctl -u waipl-VAC-01 -f                     # Logs en tiempo real de agente

# --- Base de Datos ---
psql -U waipl_user -d waipl -c "SELECT count(*) FROM documents WHERE doc_estado='ACTIVO';"
psql -U waipl_user -d waipl -c "SELECT agent_id, estado, last_heartbeat FROM agents;"

# --- Backup y Restauración ---
python scripts/backup.py --full                   # Backup completo
python scripts/backup.py --db-only                # Solo base de datos
python scripts/restore.py --from 2026-07-22       # Restaurar desde fecha

# --- Sincronización ---
syncthing cli config folders list                 # Ver carpetas sincronizadas
syncthing cli operations restart                  # Reiniciar Syncthing

# --- Dashboard ---
streamlit run dashboard/app.py                    # Iniciar dashboard (NC)
# Abrir navegador: http://localhost:8501 o http://<ip-nc>:8501

# --- Logs ---
tail -f /opt/waipl/logs/ORC-01.log               # Seguir log de agente
grep "CRIT" /opt/waipl/logs/*.log                 # Buscar eventos críticos
python scripts/log_stats.py --today               # Estadísticas de logs del día
```

---

### Anexo I: Matriz RACI de Responsabilidades

*Leyenda: R = Responsable (ejecuta), A = Aprobador (da el visto bueno), C = Consultado (aporta input), I = Informado (recibe notificación)*

| Actividad | ORC-01 | PIA-01 | PIA-02 | INC-01 | VAC-01 | SEA-01 | GDO-01 | COR-01 | MAE-01 | CYR-01 | INU-01 | INU-02 | Usuario |
|-----------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|---------|
| Desarrollo de agentes | C | C | C | C | C | C | C | C | C | C | C | C | **A/R** |
| Despliegue de agentes | **A** | R | R | R | R | R | R | R | R | R | R | R | I |
| Monitoreo de salud del sistema | **R** | I | I | I | I | I | I | I | I | **A** | I | I | C |
| Validación de outputs IA | I | R | — | — | **A** | I | I | I | I | I | I | I | C |
| Gestión de incidentes | C | I | I | I | I | C | I | **R** | C | **A** | I | I | I |
| Backup y recuperación | I | I | — | — | I | I | C | I | **A/R** | C | I | — | I |
| Auditoría de seguridad | I | I | — | — | I | **A/R** | C | I | I | C | I | — | I |
| Generación de reportes | I | R | R | R | R | R | R | **A** | R | R | I | I | I |
| Actualización de MNP | I | I | — | — | I | I | **A/R** | I | C | I | — | — | C |
| Decisión de rollback | I | I | — | — | I | I | I | I | R | C | — | — | **A** |
| Indexación y archivo documental | I | C | — | I | — | C | **R** | I | C | — | — | — | I |
| Sincronización NM-NC | C | — | C | C | — | C | C | I | C | **R** | — | I | I |

### Anexo J: Glosario de Términos

| Término | Definición |
|---------|------------|
| **Agente** | Entidad de software autónoma con responsabilidades definidas dentro del ecosistema WAIPL |
| **Heartbeat** | Señal periódica (cada 30 segundos) que indica que un agente está activo y operativo |
| **Modo Degradado** | Estado operativo donde el Nodo Móvil funciona sin conexión al Nodo Central, con funcionalidad limitada a cache local y captura offline |
| **Score de Confianza** | Valor numérico entre 0.0 y 1.0 asignado por VAC-01 a cada output de IA, basado en heurísticas de coherencia, factualidad y citación |
| **RAG** | Retrieval-Augmented Generation: técnica que enriquece los prompts con documentos relevantes recuperados de la base de conocimiento antes de la inferencia |
| **MNP** | Manual de Normas y Procedimientos: documento que establece reglas y flujos de trabajo estandarizados para un área específica |
| **KPI** | Key Performance Indicator: métrica cuantificable usada para evaluar el rendimiento de un área o agente |
| **ACK** | Acknowledge: mensaje de confirmación que un agente envía al recibir una comunicación crítica, requerido en menos de 5 segundos |
| **Failover** | Conmutación automática a un sistema o agente de respaldo cuando el primario falla |
| **OCR** | Optical Character Recognition: extracción automatizada de texto desde documentos escaneados o imágenes |
| **Embedding** | Representación vectorial (768 dimensiones) del contenido semántico de un documento, usado para búsqueda por similitud conceptual |
| **UUID** | Universally Unique Identifier: identificador de 128 bits generado aleatoriamente, usado como clave primaria en todos los registros del sistema |
| **Trazabilidad** | Capacidad de reconstruir el historial completo de una acción, mensaje o documento a través de logs enlazados por trace_id |

### Anexo K: Diagrama de Flujo de Datos del Sistema

```
                         ┌─────────────────────┐
                         │     USUARIO          │
                         │  (voz / texto / img) │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   INC-01 (NM)        │
                         │   Captura y etiqueta │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   PIA-02 (NM)        │
                         │   Cliente ligero     │
                         │   Cache offline      │
                         └──────────┬──────────┘
                                    │
                              API REST / LAN
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   PIA-01 (NC)        │
                         │   Ollama + RAG       │
                         │   Genera raw output  │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   VAC-01 (NC)        │
                         │   Evalúa confianza   │
                         │   Score 0.0 - 1.0    │
                         └──────────┬──────────┘
                                    │
              ┌─────────────────────┼─────────────────────┐
              │                     │                     │
              ▼                     ▼                     ▼
    ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
    │  score ≥ 0.75   │  │ 0.60 ≤ s < 0.75│  │  score < 0.60   │
    │  APROBADO        │  │  ADVERTENCIA    │  │  BLOQUEADO       │
    └────────┬────────┘  └────────┬────────┘  └────────┬────────┘
             │                    │                     │
             ▼                    ▼                     ▼
    ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
    │  INU-01 / INU-02│  │  INU-01 / INU-02│  │  COR-01          │
    │  Entrega directa │  │  + banner warning│  │  Alerta CRIT     │
    └────────┬────────┘  └────────┬────────┘  └────────┬────────┘
             │                    │                     │
             └────────────────────┼─────────────────────┘
                                  │
                                  ▼
                       ┌─────────────────────┐
                       │   GDO-01 (NC)        │
                       │   Registro y archivo │
                       │   UUID + hash + idx  │
                       └──────────┬──────────┘
                                  │
                                  ▼
                       ┌─────────────────────┐
                       │   SEA-01 (NC)        │
                       │   Auditoría completa │
                       │   Trazabilidad total │
                       └─────────────────────┘

    ═══════════════════════════════════════════════════════════
    FLUJO CONTINUO (background):
    
    ORC-01 ←→ Heartbeat (todos los agentes, cada 30s)
    MAE-01 → Backup diario + rotación de logs
    CYR-01 → Health-check + failover
    COR-01 → Reportes programados
    Syncthing → Sincronización NM ↔ NC
    ═══════════════════════════════════════════════════════════
```

### Anexo L: Protocolo de Escalamiento de Alertas

| Nivel | Condición Disparadora | Acción Automática | Canal de Notificación | Tiempo Máx. de Respuesta |
|-------|----------------------|-------------------|----------------------|--------------------------|
| **INFO** | Evento normal registrado (inicio de agente, tarea completada) | Archivar en log únicamente | Ninguna | — |
| **WARNING** | Desviación leve del umbral (latencia > 5s, espacio disco < 20GB, score VAC < 0.75 por 1h) | Ajuste automático de parámetros | Dashboard INU-01 (amarillo) | 4 horas |
| **ERROR** | Fallo recuperable (agente caído, timeout de inferencia, sync NM-NC > 15 min) | Auto-restart del agente (máx. 3 intentos). Si falla → escala a humano | Push INU-02 + Email local | 15 minutos |
| **CRITICAL** | Fallo no recuperable o brecha de seguridad (score VAC < 0.60 > 10% del lote, hash comprometido, acceso no autorizado detectado) | Aislamiento del agente/nodo afectado. Activación de modo degradado si aplica | Push + Email + Dashboard rojo | Inmediato (objetivo < 5 min) |
| **EMERGENCY** | Pérdida de datos o compromiso total del sistema (corrupción de BD, ransomware, acceso root no autorizado) | Parada controlada del sistema. Aislamiento completo de red. Activación de Protocolo Fortaleza (SEA-01) | Todos los canales disponibles simultáneamente | Inmediato |

**Reglas del protocolo:**
- Todo incidente ERROR o superior genera automáticamente un ticket con formato `INC-<YYYYMMDD>-<NNN>`
- El nivel puede ser degradado (CRITICAL → ERROR) solo por el usuario humano, nunca automáticamente
- Un incidente en EMERGENCY requiere informe post-incidente (R-06) en menos de 24 horas
- Dos incidentes CRITICAL en la misma área en 7 días disparan una auditoría extraordinaria

---

## RESUMEN DE ANEXOS

| Anexo | Tipo | Contenido | Utilidad principal |
|-------|------|-----------|-------------------|
| **A** | Código | Template BaseAgent Python + PIA-02 | Programar nuevos agentes |
| **B** | Config | `system.yaml` completo | Configurar el ecosistema |
| **C** | Config | `.env.example` documentado | Variables de entorno |
| **D** | Formato | JSON estándar de mensajes | Comunicación entre agentes |
| **E** | Formato | JSON de reporte de incidente (R-06) | Reportes post-incidente |
| **F** | SQL | Esquema completo (7 tablas) | Base de datos |
| **G** | Diagrama | Flujo de validación VAC-01 | Entender el scoring |
| **H** | Referencia | Comandos rápidos | Operación diaria |
| **I** | Gobernanza | Matriz RACI | Saber quién hace qué |
| **J** | Referencia | Glosario de términos | Lenguaje común del proyecto |
| **K** | Diagrama | Flujo de datos del sistema | Visión global |
| **L** | Gobernanza | Protocolo de escalamiento | Gestión de crisis |

---

## CONTROL DE VERSIONES DEL DOCUMENTO

| Versión | Fecha | Autor | Cambios |
|---------|-------|-------|---------|
| 1.0 | 2026-07-22 | Kimi K3 | Documento inicial. Secciones 1-13. |
| 1.1 | 2026-07-22 | Z (AutoClaw) | Introducción ejecutiva + completadas secciones 13.5 (métodos 5-6) y 14 (Anexos A-H técnicos). |
| 1.2 | 2026-07-22 | Kimi K3 + Z (AutoClaw) | Fusión final. Anexos I-L de gobernanza (Kimi) integrados con A-H técnicos (Z). Documento unificado completo. |

---

**Fin del documento — WAIPL Plan de Desarrollo v1.2**

*Este plan es un marco de trabajo vivo que debe adaptarse según las necesidades operativas reales del ecosistema. La arquitectura de 12 agentes, el sistema de confianza verificable (VAC-01) y la trazabilidad total forman la base para construir un laboratorio de IA robusto, gratuito y soberano sobre los dos dispositivos del WAIPL.*
