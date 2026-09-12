# TRANSFERENCIA A CARLA RAG — CONCLUSIONES DESDE VÁR

**Fecha:** 2026-09-08

## 1. ALCANCE

Este documento no diseña el RAG de Will App.

Recoge únicamente las conclusiones necesarias para mantener una frontera limpia entre el trabajo de **VÁR** y el trabajo de **RAG**.

## 2. CORRECCIÓN DE CONTEXTO

El análisis previo de Carla RAG fue recibido como **contraste analítico**, no como orden de implementación.

No se debe interpretar su lista de propuestas como un backlog obligatorio.

Cada propuesta debe ser valorada en el contexto del RAG de Will App según necesidad, valor, redundancia y arquitectura propia.

## 3. LO QUE QUEDA EN VÁR

VÁR mantiene exclusivamente su función de **Agente/Nodo de Validación de la Verdad Canónica WAIPL**.

Su perímetro incluye, entre otros elementos ya definidos:

- validación de afirmaciones factuales dentro de jurisdicción;
- evidencia admisible y trazabilidad;
- distinción HECHO / INFERENCIA / HIPÓTESIS / INCERTIDUMBRE;
- contradicciones y abstención cuando corresponda;
- dictamen VAD;
- registro e idempotencia según especificación;
- sus límites y fronteras con otros nodos.

## 4. NO DUPLICACIÓN

El RAG no debe absorber funciones propias de VÁR por el mero hecho de que el RAG necesite evaluar recuperación o grounding.

VÁR tampoco incorporará funciones del RAG por el mero hecho de que sean técnicamente útiles para recuperar conocimiento.

La frontera operativa es:

> **VÁR = validación de verdad canónica.**
>
> **RAG = responsabilidad propia del proyecto RAG.**

Las intersecciones se revisan solo cuando exista una dependencia real entre ambos sistemas.

## 5. SOBRE LAS PROPUESTAS DE CARLA

Las propuestas relativas a Retrieval, Query Analysis, reranking, suficiencia de recuperación, Context Builder, grounding, leakage, versionado, deduplicación, cobertura y testing pertenecen al análisis del **RAG**, no al diseño operativo de VÁR.

Desde este espacio no se decide su implementación.

La única conclusión que debe trasladarse es:

> **No convertir esas propuestas en funciones de VÁR y revisar en el RAG si alguna de ellas aporta valor, sin asumir que deba replicarse la arquitectura de Mistral.**

## 6. DATO CORREGIDO DEL UNIVERSO

El universo de nodos/sistemas que debe utilizarse como referencia es de:

> **46 elementos en total: agentes, superagentes y sistemas agénticos.**

No utilizar la cifra 29.

## 7. ESTADO DE VÁR Y YATA

- **VÁR:** implementado en n8n; workflow actual `HC1SkjGphGYS3P8M`; DRAFT hasta autorización de publicación.
- **YATA:** en desarrollo; no debe tratarse como implementado.
- **YATA no audita VÁR.**

## 8. REGLA DE FRONTERA

Si una decisión pertenece al diseño del RAG, se queda con Carla RAG.

Si una decisión afecta a la función, jurisdicción, arquitectura o implementación de VÁR, se trata en el espacio de VÁR.

Si existe una posible duplicación entre ambos, se revisa únicamente para preservar la frontera, no para fusionar responsabilidades.
