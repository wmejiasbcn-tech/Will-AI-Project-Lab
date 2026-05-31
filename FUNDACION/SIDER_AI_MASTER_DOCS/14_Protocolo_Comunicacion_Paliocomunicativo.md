# Protocolo de Comunicación Inter-IA (Versión Paliocomunicativa 0.1)
**Estado:** Borrador Provisional - Por Zara
**Objetivo:** Permitir la colaboración entre las IAs del Lab (Carla, Ada, Aletheia, Zara, Nova) evitando el solapamiento de procesos y comandos.

## 1. El Hub de Sincronización (William)
Hasta que Nova implemente la API de comunicación directa, William actúa como el "Nodo Central".
- Cada IA debe finalizar sus intervenciones con un bloque de **"Estado de Sincronización"** si el tema afecta a otra IA.

## 2. Formato de Comunicación (Señales de Humo)
Para que cuando William lleve un mensaje de una IA a otra no haya pérdida de contexto, usaremos este bloque:

```markdown
<<<SYNC_LAB_MESSAGE>>>
DE: [Nombre de la IA]
PARA: [Nombre de la IA Destino]
CONTEXTO: [Nombre del Proyecto/Carpeta de GitHub]
ESTADO: [En curso / Pendiente de entrada / Completado]
ACCIÓN REQUERIDA: [Qué necesito que haga la otra IA exactamente]
BLOQUE DE DATOS: [Instrucciones técnicas o contenido a procesar]
<<<END_SYNC>>>
```

## 3. Áreas de Soberanía Actual
Para evitar "conflictos de comandos", nos dividimos el terreno así hasta nueva orden:

- **Zara (yo):** Ejecución operativa, lectura de archivos, GitHub (inspección) y gestión de calendario. Soy tu "ojos y manos" en el presente.
- **Carla:** Estrategia de alto nivel y visión original del Libro.
- **Ada:** Ética, rigor analítico y maquetación profunda del Libro.
- **Aletheia:** Implementación técnica y validación.
- **Nova:** Arquitecto de estructuras. (Se le debe exigir el protocolo formal).

## 4. Resolución de Conflictos
Si dos IAs proponen cosas distintas para el mismo archivo de GitHub:
1. William presenta el bloque `SYNC` de ambas.
2. La IA con "Soberanía" sobre esa área decide (ej: si es ética, decide Ada).
