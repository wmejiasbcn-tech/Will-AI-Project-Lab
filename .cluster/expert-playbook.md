# Playbook de Agent Cluster(leer antes de S2 / S5)

## Espacio de trabajo (.cluster/<taskId>/)
- plan.md: subtareas, worker, archivo esperado, dependencias, revisión y entrega.
- worker_NN.md: resultado del worker. Formato: conclusión / evidencia / análisis / brechas y riesgos / ubicación sugerida en el documento final.
- review.md: revisión con confianza High / Medium / Low / Conflict.
- brief.md: brief previo a la entrega.
- DELIVERY/: archivos finales. El sistema revisa esta carpeta para confirmar que hubo entrega real.

## S2 Asignación
- Regla base: una subtarea por worker. Las consultas o comandos puntuales pueden quedarse en el hilo principal.
- En textos largos, divide por capítulos y usa al menos tantos writers como dimensiones de investigación.
- Dibuja dependencias y coloca primero las tareas que desbloquean otras.

## S3 Prompt del worker
Primera frase fija: "No estás trabajando solo; no modifiques artefactos fuera de tu responsabilidad."
Entrega siempre: límites de la tarea, contexto necesario, archivo worker_NN.md de destino y formato de retorno. Si no hay evidencia, debe decirlo; no convertir conjeturas en conclusiones.
Los workers de investigación usan autoglm-websearch/open-link y citan solo fuentes leídas. Si un worker usa una skill, dale el nombre de la skill y el límite de la tarea, no pegues todo el contenido.

## S4 Revisión
Levanta revisión si hay conclusiones sintéticas, predicciones, juicios de valor, código no trivial, acciones irreversibles o decisiones relevantes para el usuario. Revisa hechos, lógica, números y código por separado.

## S5 Entrega
- Respeta el formato pedido por el usuario. Si no hay formato, respuestas breves van en texto; lo demás usa `docx` por defecto.
- Informes, planes, minutas e investigación → `docx`; presentaciones → `ppt`; tablas/modelos de datos → `xlsx`; formato fijo → `pdf`; gráficos → `charts`.
- Para textos largos, usa `write-skill` por capítulos y genera el archivo final con `docx` u otra skill de artefacto.
- Mantén UTF-8 estricto; no ignores errores de decodificación.
- Coloca los archivos finales en DELIVERY/. En la respuesta final, muestra progreso completado, enlaces clicables y limitaciones necesarias.