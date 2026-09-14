# Resultado de validación

Validación realizada el 14 de septiembre de 2026 en Windows con Python 3.13.14.

## Pruebas automatizadas

```text
.venv/Scripts/python.exe -m pytest -q
58 passed, 2 warnings in 1.82s

.venv/Scripts/python.exe -m pip check
No broken requirements found.
```

Los avisos provienen de dependencias: Starlette señala una futura migración de
su TestClient de httpx a httpx2 y la deprecación de un alias de BlockingPortal en
AnyIO. No se ocultaron. Se mantiene httpx conforme al requisito de la actividad;
las pruebas terminaron correctamente y no hay errores funcionales detectados.

Versiones utilizadas: FastAPI 0.141.1, Uvicorn 0.53.0, Pydantic 2.13.5,
python-dotenv 1.2.3, pytest 9.1.1 y httpx 0.28.1. `requirements.txt` define
rangos de versiones; instalaciones futuras pueden resolver versiones diferentes.

## Uvicorn y HTTP real

Se inició Uvicorn en un puerto local disponible, se verificó la aplicación y se
detuvo el proceso al finalizar:

- GET `/`, `/users`, `/users/1`, `/docs`, `/redoc` y `/openapi.json`: 200.
- POST: 201; PUT y PATCH: 200; filtro combinado: resultado correcto.
- DELETE: 204 sin cuerpo.
- Cabecera `X-App-Name`: presente.
- TestClient verificó además las dos cabeceras, los errores y las seis operaciones
  OpenAPI bajo el tag `Users`.

No se tomaron capturas ni se verificó visualmente la carga de las CDN de Swagger
y ReDoc en un navegador. Sus páginas HTTP y el documento OpenAPI respondieron correctamente.

## Archivos y Git

Los archivos C# se movieron a `legacy_csharp/` y se compararon sus hashes para
comprobar que el respaldo conserva su contenido. No se borró historial Git.

La raíz Git detectada es `C:/Users/SAMIR ACOSTA`, superior a este proyecto.
Se consultaron `git status`, `git diff --stat` y `git diff --check` limitados a
la carpeta `Usuario`. Esta carpeta figura como nueva, sin archivos versionados;
por eso `git diff` normal no muestra todavía el código creado. No se ejecutó
`git add`, `git commit` ni `git push`, ni se modificaron otros proyectos.

Ejecuta las operaciones Git desde la raíz de este proyecto, no desde la carpeta
personal, y revisa los archivos preparados antes del commit. Las rutas `.venv/`,
`.env`, cachés y `legacy_csharp/` quedan ignoradas.
