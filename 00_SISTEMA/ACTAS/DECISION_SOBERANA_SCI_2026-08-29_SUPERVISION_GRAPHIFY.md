# ACTA — DECISIÓN SOBERANA SCI

**Fecha:** 2026-08-29  
**Ámbito:** SCI n8n-WAIPL  
**Autoridad:** William Mejías Navarro — Soberano

## 1. DECISIÓN

Queda establecido canónicamente:

- **Graphify** es el Sistema Nervioso Central (SNC) del ecosistema WAIPL.
- **Hermes** es el **Director Operativo** y corresponde a Hermes la **supervisión operativa de Graphify**.
- **WILLIAM-SCY-01** es el **avatar del Soberano**.
- WILLIAM-SCY-01 constituye la **capa independiente de comprobación y contraste del Soberano** respecto de las comunicaciones, decisiones, informes, estados o conclusiones que cualquier nodo, agente o sistema comunique al Soberano.
- La función de WILLIAM-SCY-01 no queda subordinada a Hermes, Graphify, Carla, Ada ni a ningún otro nodo cuya información pueda ser objeto de contraste.
- WILLIAM-SCY-01 no sustituye a Hermes como Director Operativo ni adquiere por esta función jurisdicción operativa sobre Graphify.

## 2. CONSECUENCIA ARQUITECTÓNICA

Se distinguen formalmente dos funciones:

### Supervisión operativa

**Hermes → Graphify**

Comprende la supervisión del funcionamiento operativo del SNC dentro de la jurisdicción del Director Operativo.

### Contraste soberano independiente

**Cualquier nodo/agente/sistema → Soberano → WILLIAM-SCY-01**

WILLIAM-SCY-01 comprueba y contrasta la información antes de informar al Soberano conforme a su función. Esta capa debe conservar independencia respecto de la fuente que está siendo contrastada.

## 3. CONSECUENCIA PARA EL SCI

El diseño del SCI no deberá implementar una dependencia obligatoria de WILLIAM-SCY-01 respecto de Hermes, Graphify, Carla o Ada para ejercer su función de contraste soberano.

La comunicación operativa y la comunicación de contraste soberano deben tratarse como funciones diferenciadas.

## 4. CONSECUENCIA DOCUMENTAL

La formulación anterior del Principio IV de la **Arquitectura Fisiológica Alegórica WAIPL v1.0** atribuía la supervisión de Graphify al Vórtice. Esa formulación queda sustituida por la decisión soberana de esta acta.

El documento canónico correspondiente ha sido actualizado en la misma rama de reconciliación del SCI.

## 5. REGLA DE IMPLEMENTACIÓN

Ningún workflow, tabla, prompt, nodo o documento de implementación podrá reinterpretar esta decisión. Ante discrepancia entre implementación y esta decisión canónica, se considera que existe **DERIVA DE IMPLEMENTACIÓN** y la implementación afectada deberá detenerse y elevar la discrepancia.

## 6. ESTADO

**DECISIÓN SOBERANA: CONFIRMADA.**  
**Pendiente:** reconciliación completa CANON → n8n antes del piloto.
