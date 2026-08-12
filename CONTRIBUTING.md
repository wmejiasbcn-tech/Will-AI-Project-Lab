# Contribuir al Will-AI Project Lab

Este repositorio sigue un flujo de trabajo GitHub Flow combinado con las normas del Lab. Para contribuir efectivamente, lee este documento antes de enviar issues o pull requests.

## 1. Antes de comenzar

- Revisa `README.md` y `06_SISTEMA_OPERATIVO/GITHUB_FLOW_PROTOCOLO.md`.
- Verifica que no exista ya un issue abierto sobre el mismo tema.
- Usa las plantillas de issue en `.github/ISSUE_TEMPLATE/`.

## 2. Reportar un problema o proponer una mejora

- Usa `bug_report.md` para errores y fallos.
- Usa `feature_request.md` para nuevas ideas y mejoras.
- Si no hay una plantilla exacta, usa la plantilla de solicitud de mejora.

## 3. Crear una rama de trabajo

Nombra tu rama con un prefijo claro:

- `feature/` para nuevas funcionalidades
- `fix/` para correcciones de errores
- `docs/` para documentación
- `infra/` para cambios de infraestructura y automatizaciones
- `task/` para tareas de mantenimiento y organización

Ejemplo:

```bash
git checkout -b feature/plantillas-github
```

## 4. Enviar un Pull Request

- Usa `.github/PULL_REQUEST_TEMPLATE.md` como guía.
- Describe el objetivo, los cambios principales y cómo probarlos.
- Añade los issues relacionados con `#` o `GH-`.
- Asegúrate de que no haya conflictos con `main`.

## 5. Revisión y validación

- El Vórtice de 180 grados supervisa la integración en `main`.
- Espera revisiones y comentarios antes de fusionar.
- Si el cambio implica automatización, aplica primero el principio de coste del Lab: gratis, local, simple.

## 6. Normas de comportamiento

- Respeta el `CODE_OF_CONDUCT.md` del repositorio.
- Mantén la comunicación clara, humilde y colaborativa.
- Sé honesto sobre el estado de tu aporte y los riesgos asociados.

## 7. Calidad y automatización

- Usa el workflow de salud del repositorio en `.github/workflows/repo-health.yml`.
- Antes de automatizar una nueva tarea, prueba manualmente y documenta el proceso en `06_SISTEMA_OPERATIVO/05_AUTOMATIZACIONES.md`.

## 8. Etiquetas y gestión de issues

- Usa etiquetas del repositorio cuando crees issues.
- Consulta `.github/labels.yml` para la lista de etiquetas recomendadas.

## 9. Enlaces útiles

- `.github/ISSUE_TEMPLATE/bug_report.md`
- `.github/ISSUE_TEMPLATE/feature_request.md`
- `.github/PULL_REQUEST_TEMPLATE.md`
- `.github/CODE_OF_CONDUCT.md`
- `.github/CODEOWNERS`
- `.github/workflows/repo-health.yml`
