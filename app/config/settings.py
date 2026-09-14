"""Variables opcionales del entorno; no se necesitan secretos para ejecutar."""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[2] / ".env")

APP_NAME = os.getenv("APP_NAME") or "device_systems"
APP_VERSION = os.getenv("APP_VERSION") or "2.0.0"
ADMIN_USER = os.getenv("ADMIN_USER") or "admin"
