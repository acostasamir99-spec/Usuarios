# Validación de persistencia

Fecha: 17 de septiembre de 2026.

- Python 3.13.14, FastAPI 0.141.1 y SQLAlchemy 2.0.54.
- Comando: `.\.venv\Scripts\python.exe -m pytest -q`.
- Resultado: **71 passed**, dos avisos de deprecación en dependencias
  (integración de httpx con Starlette y alias BlockingPortal de AnyIO).
- SQLite temporal independiente por prueba, con sesiones reales SQLAlchemy.
- CRUD, filtros combinados, orden ascendente/descendente, validación 422,
  duplicados 400 y usuarios inexistentes 404.
- Verificación de constraints con INSERT directo y rollback.
- Reapertura de la base con un engine nuevo: usuario conservado.
- Peticiones concurrentes: IDs únicos y un solo alta por correo.
- Verificación de documentación OpenAPI, schemas de respuesta y cabeceras.

El generador `docs/generar_evidencias.py` ejecuta 17 peticiones HTTP contra
Uvicorn y comprueba cada código esperado. Usa una base temporal y genera
`resultados.json`, `evidencias.html` y capturas PNG. Las capturas del informe
representan respuestas reales; no son imágenes simuladas de Swagger.
