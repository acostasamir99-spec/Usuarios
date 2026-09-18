> Informe histórico: la estructura actual utiliza `app/`, `tests/`, `requirements.txt` y `device_systems.db` en la raíz. Consulta el README para ejecutar el proyecto.

# Reorganización del backend

Fecha: 17 de septiembre de 2026.
Evidencia: GA1-220501096-01-AA1-EV09 – FastAPI con SQLAlchemy: Persistencia de Datos y CRUD sobre Base de Datos en device_systems.

## Inspección y movimientos

Se inspeccionaron los módulos Python, pruebas, configuración, documentación,
generador de evidencias, base SQLite y respaldo local C#. Había modificaciones
locales previas; se conservaron sin restaurarlas a la versión de Git.

| Antes | Después |
| --- | --- |
| app/ (todos sus archivos) | backend/app/ |
| tests/ (todos sus archivos) | backend/tests/ |
| main.py (consola anterior) | backend/main.py |
| requirements.txt | backend/requirements.txt |
| .env.example | backend/.env.example |
| device_systems.db | backend/device_systems.db |

Se conservaron los módulos históricos `app/data` y `app/usuarios`. No se
duplicaron servicios, rutas, modelos, schemas ni dependencias. El respaldo
`legacy_csharp/`, las imágenes y los informes académicos anteriores permanecen
en su ubicación. `frontend/` contiene únicamente `.gitkeep`.

## Imports y riesgos resueltos

- Los imports `app.*` se mantienen: el paquete completo está en `backend/`.
  Esto incluye consola, configuración, modelos, servicios, rutas, dependencias y pruebas.
- `pytest.ini` permanece en la raíz y usa `testpaths = backend/tests` y
  `pythonpath = backend`. Funciona desde la raíz y desde `backend/`.
- El generador `docs/generar_evidencias.py` añade `backend/` al path de imports
  y obtiene el árbol de fuentes desde `backend/app/`.
- La ruta de SQLite ahora es absoluta, calculada desde `connection.py`;
  evita crear bases distintas al cambiar el directorio de ejecución.
- `settings.py` sigue resolviendo `.env` con `parents[2]`, ahora en `backend/`.
  No había un `.env` existente que trasladar. Se movió su ejemplo.
- README y guía manual reflejan los comandos y las ubicaciones nuevos.

## Pruebas antes y después

Se usó el Python del entorno `.venv` existente, sin cambiar dependencias.

| Ejecución | Aprobadas | Fallidas | Avisos |
| --- | ---: | ---: | ---: |
| Antes, desde raíz: `.\.venv\Scripts\python.exe -m pytest -q` | 71 | 0 | 2 |
| Después, desde raíz: mismo comando | 71 | 0 | 2 |
| Después, desde backend: `..\.venv\Scripts\python.exe -m pytest -q` | 71 | 0 | 2 |

No se eliminaron ni modificaron pruebas. La suite cubre CRUD, búsqueda por
email en el servicio, filtros de rol y estado, orden por nombre y fecha en
ambas direcciones, validaciones, errores 400/404/422, constraints, concurrencia,
inyección de dependencias y OpenAPI.

`test_persistence_after_reconnecting` crea un usuario por HTTP, dispone el
engine y abre otro engine SQLAlchemy contra el mismo archivo temporal. La
búsqueda por email recupera el usuario persistido. Las pruebas de constraints
ejecutan INSERT directamente en SQLite y comprueban errores de integridad.

## Uvicorn y SQLite

Desde `backend/` se ejecutó:

```powershell
..\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Uvicorn inició el reloader WatchFiles y completó el arranque en el puerto 8000.
Peticiones HTTP reales a `/`, `/docs`, `/redoc`, `/openapi.json` y `/users`
devolvieron 200. El OpenAPI conserva los seis endpoints CRUD obligatorios.
Esta comprobación valida las páginas HTML; no constituye una inspección visual
en navegador de sus recursos CDN.

La base original tenía 0 usuarios. Antes y después del traslado y de ejecutar
las pruebas y el servidor, su SHA-256 fue idéntico:

```text
73918bbf8b6333d6c5c9e2266ee05be72b3a8a4cc6f7ad50be43ab58bc8a14b1
```

`PRAGMA integrity_check` devolvió `ok`; no se creó otra base en la raíz.
No se insertaron datos de verificación en la base de trabajo.

El CRUD HTTP conserva `Session`, `select(User)`, `db.get`, `db.add`,
`db.commit`, `db.refresh`, `db.rollback` y `db.delete`. Las rutas no importan
los módulos históricos en memoria. Los contratos HTTP no se modificaron.

## Pendientes y límites

No se detectaron fallos funcionales. Persisten dos avisos previos de deprecación
en dependencias: integración httpx/Starlette y alias BlockingPortal de AnyIO.
No se cambiaron versiones para resolverlos dentro de esta reorganización.
Las capturas anteriores se conservan como evidencia histórica; no se ejecutó
el generador de capturas de Playwright. El frontend no se ha desarrollado.
