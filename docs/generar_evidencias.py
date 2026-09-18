"""Ejecutar desde la raíz: python docs/generar_evidencias.py.

Requiere playwright y Microsoft Edge; usa una base temporal aislada.
"""
import html
from contextlib import closing
import json
from pathlib import Path
import socket
import sqlite3
import sys
import tempfile
import threading
import time

import httpx
import uvicorn
from sqlalchemy import create_engine
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
DOCS = ROOT / "docs"
IMAGES = DOCS / "images"


def main():
    IMAGES.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="device_systems_evidence_") as temporary:
        with socket.socket() as sock:
            sock.bind(("127.0.0.1", 0))
            port = sock.getsockname()[1]
        base_url = f"http://127.0.0.1:{port}"
        import app.main as application
        from app.database.connection import SessionLocal

        evidence_engine = create_engine(
            "sqlite:///" + str(Path(temporary) / "device_systems.db"),
            connect_args={"check_same_thread": False},
        )
        application.engine = evidence_engine
        SessionLocal.configure(bind=evidence_engine)
        server = uvicorn.Server(uvicorn.Config(application.app, host="127.0.0.1", port=port, log_level="error"))
        server_thread = threading.Thread(target=server.run, daemon=True)
        server_thread.start()
        try:
            with httpx.Client(base_url=base_url, timeout=10) as client:
                for _ in range(100):
                    try:
                        if client.get("/openapi.json").status_code == 200:
                            break
                    except httpx.ConnectError:
                        pass
                    time.sleep(0.1)
                else:
                    raise RuntimeError("Uvicorn no inició")
                records = []

                def request(label, method, path, expected, body=None):
                    response = client.request(method, path, **({"json": body} if body is not None else {}))
                    assert response.status_code == expected, response.text
                    result = response.json() if response.content else None
                    records.append(dict(prueba=label, method=method, path=path,
                                        request=body, status=response.status_code, response=result))
                    return result

                payload = dict(name="Samir Acosta", email="samir@example.com", role="user", is_active=True)
                user = request("Crear usuario", "POST", "/users", 201, payload)
                path = f"/users/{user['id']}"
                request("Correo duplicado", "POST", "/users", 400, payload)
                request("Listar usuarios", "GET", "/users", 200)
                request("Consultar por ID", "GET", path, 200)
                request("Usuario inexistente", "GET", "/users/99999", 404)
                request("Filtrar por rol", "GET", "/users?role=user", 200)
                request("Filtrar activos", "GET", "/users?is_active=true", 200)
                request("Ordenar por fecha", "GET", "/users?sort_by=created_at&order=desc", 200)
                request("Actualizar completo", "PUT", path, 200, {**payload, "name": "Samir Actualizado", "role": "support"})
                request("Actualizar parcial", "PATCH", path, 200, {"is_active": False})
                request("Rol inválido", "POST", "/users", 422, {**payload, "role": "invalid"})
                request("Email inválido", "POST", "/users", 422, {**payload, "email": "invalido"})
                request("Nombre inválido", "POST", "/users", 422, {**payload, "name": "ab"})
                with closing(sqlite3.connect(Path(temporary) / "device_systems.db")) as db:
                    database = "device_systems.db (base aislada de evidencias)\n\n"
                    database += db.execute("SELECT sql FROM sqlite_master WHERE name='users'").fetchone()[0]
                    database += "\n\nSELECT * FROM users;\n" + repr(db.execute("SELECT * FROM users").fetchall())
                    database += "\n\nÍndices:\n" + repr(db.execute("PRAGMA index_list(users)").fetchall())
                request("Eliminar", "DELETE", path, 204)
                request("Verificar eliminación", "GET", path, 404)
                request("Eliminar inexistente", "DELETE", path, 404)
                request("Actualizar inexistente", "PUT", path, 404, payload)

            (DOCS / "resultados.json").write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
            structure = "device_systems/\n" + "\n".join(str(p.relative_to(ROOT)) for p in sorted((ROOT / "app").rglob("*.py")) if "__pycache__" not in str(p))
            style = "<style>body{font:16px Arial;margin:32px;color:#16324f;background:#f4f7fa}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:white;padding:20px;border:1px solid #cbd5e1}h1,h2{color:#124559}section{margin-bottom:32px}</style>"
            sections = []
            for i, record in enumerate(records, 1):
                sections.append(f'<section><h2>{i}. {html.escape(record["prueba"])}</h2><pre>{html.escape(json.dumps(record, ensure_ascii=False, indent=2))}</pre></section>')
            report = '<meta charset="utf-8">' + style + '<h1>device_systems — Evidencias HTTP reales</h1>' + ''.join(sections)
            (DOCS / "evidencias.html").write_text(report, encoding="utf-8")
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(channel="msedge", headless=True)
                try:
                    page = browser.new_page(viewport={"width": 1280, "height": 900}, device_scale_factor=1)
                    page.goto(base_url + "/docs")
                    page.locator(".opblock").first.wait_for(timeout=60000)
                    page.screenshot(path=str(IMAGES / "swagger-ui.png"), full_page=True)
                    page.set_content('<meta charset="utf-8">' + style + '<h1>Estructura del proyecto</h1><pre>' + html.escape(structure) + '</pre>')
                    page.screenshot(path=str(IMAGES / "estructura.png"), full_page=True)
                    page.set_content('<meta charset="utf-8">' + style + '<h1>SQLite: esquema y consulta real</h1><pre>' + html.escape(database) + '</pre>')
                    page.screenshot(path=str(IMAGES / "base-datos.png"), full_page=True)
                    page.set_content(report)
                    for i, section in enumerate(page.locator("section").all(), 1):
                        section.screenshot(path=str(IMAGES / f"prueba-{i:02}.png"))
                finally:
                    browser.close()
            print(f"Generadas {len(records)} evidencias HTTP y capturas en {IMAGES}")
        finally:
            server.should_exit = True
            server_thread.join(timeout=10)
            evidence_engine.dispose()
            if server_thread.is_alive():
                raise RuntimeError("El servidor de evidencias no terminó")


if __name__ == "__main__":
    main()
