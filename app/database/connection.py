"""Conexión SQLite y sesiones independientes por petición."""
from pathlib import Path

from sqlalchemy import URL, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Equivale a sqlite:///./device_systems.db desde la raíz del proyecto,
# pero conserva la misma base incluso al ejecutar desde otro directorio.
DATABASE_PATH = Path(__file__).resolve().parents[2] / "device_systems.db"
DATABASE_URL = URL.create("sqlite", database=str(DATABASE_PATH))
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False, "timeout": 30})
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

def get_db():
    with SessionLocal() as db:
        yield db
