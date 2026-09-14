"""Datos por proceso: se reinician al reiniciar el servidor."""

from copy import deepcopy
from itertools import count
from threading import RLock

INITIAL_USERS = [
    {"id": 1, "name": "Administrador", "email": "admin@devicesystems.com",
     "role": "admin", "is_active": True},
    {"id": 2, "name": "Soporte Sistema", "email": "support@devicesystems.com",
     "role": "support", "is_active": True},
    {"id": 3, "name": "Usuario Inactivo", "email": "user@devicesystems.com",
     "role": "user", "is_active": False},
]

users_db: list[dict] = deepcopy(INITIAL_USERS)
db_lock = RLock()
_ids = count(max(user["id"] for user in INITIAL_USERS) + 1)


def get_next_id() -> int:
    """Generar IDs sin reutilizar los eliminados durante este proceso."""
    with db_lock:
        return next(_ids)


def reset_users() -> None:
    """Restaurar datos e IDs para aislar las pruebas; no es un endpoint."""
    global _ids
    with db_lock:
        users_db[:] = deepcopy(INITIAL_USERS)
        _ids = count(max(user["id"] for user in INITIAL_USERS) + 1)
