import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = os.getenv("APP_NAME", "Sistema Usuarios")
APP_VERSION = os.getenv("APP_VERSION", "1.0")
ADMIN_USER = os.getenv("ADMIN_USER", "admin")