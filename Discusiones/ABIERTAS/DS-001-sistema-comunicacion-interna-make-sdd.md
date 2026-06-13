# DS-001 - Sistema de Comunicacion Interna Make + SDD

---

## CABECERA

| Campo | Valor |
|---|---|
| ID | DS-001 |
| Estado | ABIERTA |
| Prioridad | Alta |
| Tiempo objetivo | 72 horas |
| Fecha de apertura | 2026-06-13 |
| Promotor | William L. Mejias Navarro - Soberano |
| Coordinacion sugerida | Carla, con apoyo de Nauta |
| Validacion etica | Ada |
| Validacion documental | Sylvia |
| Validacion tecnica | Aletheia / Ariadna |
| Nodo puente | Zara, bajo arnes operativo estricto |
| Vortice consultivo | Neo, Nexus, Perplexity, NotebookLM, Nauta |

---

## 00 - PLANTEAMIENTO INICIAL

El Will-AI Project Lab necesita reducir el cuello de botella donde toda comunicacion entre nodos pasa a traves del Soberano. Ya existe una base conceptual aprobada: el PSI v1.1, la carpeta `Discusiones`, la plantilla DS y la mesa de control del Sistema Operativo del Lab.

La posibilidad a estudiar es establecer un mecanismo interno de comunicacion usando una arquitectura gratuita o de coste cero inicial, combinando Make.com como capa de automatizacion, GitHub/Discusiones como registro trazable y SDD como capa de decision/distribucion documental.

Pregunta central:

> Como puede el Lab crear un piloto minimo, gratuito, trazable y seguro para que los nodos puedan emitir propuestas, mensajes y estados sin que el Soberano tenga que transportar todo manualmente?

Documentos de referencia:

- `06_SISTEMA_OPERATIVO/PSI/PSI_v1.1_OFICIAL.md`
- `Discusiones/README.md`
- `Discusiones/PLANTILLA_DS.md`
- `06_SISTEMA_OPERATIVO/BROADCAST.md`
- `03_PERSONAS_IA/ZARA/PROTOCOLO_RECALIBRACION_OPERATIVA_ZARA.md`
- `06_SISTEMA_OPERATIVO/03_NODOS_COMUNICACION.md`

Nota terminologica:

En esta DS, "SDD" queda marcado como termino pendiente de definicion final por el Soberano. Operativamente se trata como la capa de Sistema de Discusiones/Decisiones Distribuidas basada en `Discusiones`, PSI y trazabilidad GitHub.

---

## 01 - HIPOTESIS DE ARQUITECTURA

### Capa 1 - Captura

Entrada de mensajes desde:

- Formulario simple.
- Webhook de Make.
- Google Sheet.
- GitHub Issue.
- Copia manual desde una interfaz de nodo.
- Mensaje preparado por Zara cuando exista autorizacion previa.

### Capa 2 - Normalizacion

Todo mensaje se convierte al formato estandar:

```md
DE:
PARA:
TIPO: propuesta / estado / bloqueo / decision / broadcast / solicitud
CONTEXTO:
HECHO VERIFICADO:
INFERENCIA:
ACCION REQUERIDA:
RIESGO:
VALIDACION NECESARIA:
TIMESTAMP:
```

### Capa 3 - Registro canonico

El registro canonico inicial debe ser GitHub, por trazabilidad y porque ya forma parte del Lab.

Opciones:

- GitHub Issues para entradas operativas.
- GitHub Discussions para deliberacion.
- Carpeta `Discusiones/` para respaldo documental en Markdown.
- `BROADCAST.md` para comunicados oficiales.

### Capa 4 - Enrutamiento

Make.com puede enrutar segun campos:

- `PARA: Carla` -> estrategia/coordinacion.
- `PARA: Ada` -> etica/riesgo.
- `PARA: Sylvia` -> documentacion/memoria.
- `PARA: Ariadna` -> repositorio/GitHub.
- `PARA: Zara` -> operativa externa autorizada.
- `PARA: Soberano` -> decision final.

### Capa 5 - Revision humana

Nada sensible se ejecuta automaticamente al principio.

El piloto debe operar en modo:

```text
captura -> registra -> clasifica -> propone -> espera validacion
```

No:

```text
captura -> ejecuta -> informa despues
```

---

## 02 - PILOTO MINIMO GRATUITO

### Nombre

WAIPL-PSI-Piloto-01

### Objetivo

Probar si Make.com puede recibir un mensaje estructurado y convertirlo en una entrada trazable dentro del sistema SDD/PSI sin coste inicial.

### Escenario Make sugerido

1. Webhook personalizado recibe un payload.
2. Filtro comprueba que incluye campos minimos.
3. Router separa por tipo:
   - propuesta.
   - bloqueo.
   - broadcast.
   - decision requerida.
4. GitHub crea un Issue o ejecuta GraphQL si se decide usar Discussions.
5. Opcional: Google Sheets anade una fila como indice simple.
6. Opcional: Gmail notifica al Soberano solo si `PARA: Soberano` o `RIESGO: alto`.

### Campos minimos del payload

```json
{
  "de": "Zara",
  "para": "Carla",
  "tipo": "propuesta",
  "contexto": "Sistema de comunicacion interna",
  "hecho_verificado": "Existe PSI v1.1 aprobado.",
  "inferencia": "Make puede funcionar como capa de transporte inicial.",
  "accion_requerida": "Revisar viabilidad del piloto.",
  "riesgo": "medio",
  "validacion_necesaria": "Ada y Soberano",
  "timestamp": "2026-06-13 00:00 Europe/Madrid"
}
```

### Criterio de exito del piloto

- Se registra una entrada sin exponer tokens.
- La entrada queda trazable en GitHub o Markdown.
- El Soberano no tiene que reexplicar el contexto.
- No se envia nada al exterior sin autorizacion.
- Zara puede participar como puente sin saltarse el arnes.

---

## 03 - LIMITES DE COSTE CERO

Segun la pagina oficial de precios de Make consultada el 2026-06-13:

- El plan Free no tiene limite temporal.
- Incluye hasta 1.000 creditos al mes.
- Permite 2 escenarios activos.
- Tiene intervalo minimo de 15 minutos en escenarios programados.
- Cada accion de modulo suele consumir creditos.

Implicacion para el Lab:

- El piloto debe tener 1 escenario principal y, como maximo, 1 escenario auxiliar.
- Debe evitar ejecuciones frecuentes innecesarias.
- Debe preferir webhooks/manual trigger frente a polling constante.
- Debe registrar solo lo importante.

---

## 04 - RIESGOS

### Riesgo 1 - Falsa comunicacion IA-IA

No se puede afirmar que los nodos se comunicaron si solo se genero un mensaje preparado.

Mitigacion:

- Cada entrada debe marcar estado: preparado / enviado / recibido / respondido / validado.

### Riesgo 2 - Exposicion de secretos

Webhooks, tokens y credenciales no deben entrar al repositorio.

Mitigacion:

- Guardar secretos solo en Make, GitHub Secrets o gestores autorizados.
- En Markdown solo registrar nombres logicos, nunca valores.

### Riesgo 3 - Zara recupera demasiada autonomia demasiado pronto

Zara puede operar como puente, pero bajo autorizacion.

Mitigacion:

- El piloto no ejecuta acciones externas automaticas.
- Zara prepara o transmite solo con mandato explicito.

### Riesgo 4 - Sobrecarga del Soberano

Si cada mensaje genera notificacion, se cambia un cuello de botella por otro.

Mitigacion:

- Notificar al Soberano solo decisiones, riesgos altos o bloqueos.
- El resto queda registrado para revision periodica.

---

## 05 - DECISIONES PENDIENTES

- [ ] Confirmar que SDD significa oficialmente lo que el Soberano determine.
- [ ] Elegir registro inicial: GitHub Issues, GitHub Discussions o `Discusiones/`.
- [ ] Confirmar si Make usara el webhook de prueba existente o uno nuevo.
- [ ] Definir quienes participan en el piloto: propuesta inicial, Zara + Carla + Ada + Soberano.
- [ ] Decidir si Google Sheets se usa como indice auxiliar.
- [ ] Definir regla de notificacion al Soberano.

---

## 06 - RECOMENDACION DE NAUTA

Empezar con un piloto muy pequeno:

```text
Webhook Make -> validacion de campos -> GitHub Issue -> entrada en SDD -> revision del Soberano
```

No empezar todavia con WhatsApp, Gmail ni envio externo.

Primero probar que el sistema registra bien. Luego se abre el puente exterior con Zara bajo autorizacion.

---

## 07 - DECISION FINAL

Pendiente del Soberano.

---

## 08 - CIERRE ETICO

Pendiente de Ada.
