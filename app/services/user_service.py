"""Operaciones sencillas sobre usuarios, con escrituras protegidas por un lock."""

from fastapi import HTTPException, status

from app.data.users_db import db_lock, get_next_id, users_db
from app.schemas.user_schema import UserCreate, UserPatch, UserUpdate

ALLOWED_ROLES = frozenset({"admin", "support", "user"})


def validate_role(role: str) -> None:
    if role not in ALLOWED_ROLES:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Rol no permitido")


def check_duplicate_email(email: str, exclude_id: int | None = None) -> None:
    if any(user["email"].casefold() == email.casefold() and user["id"] != exclude_id
           for user in users_db):
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
                            "El correo electrónico ya está registrado")


def list_users(role: str | None = None, is_active: bool | None = None) -> list[dict]:
    if role is not None:
        validate_role(role)
    with db_lock:
        return [user.copy() for user in users_db
                if (role is None or user["role"] == role)
                and (is_active is None or user["is_active"] == is_active)]


def find_user(user_id: int) -> dict | None:
    with db_lock:
        return next((user.copy() for user in users_db if user["id"] == user_id), None)


def create_user(data: UserCreate) -> dict:
    values = data.model_dump()
    with db_lock:
        validate_role(values["role"])
        check_duplicate_email(values["email"])
        user = {"id": get_next_id(), **values}
        users_db.append(user)
        return user.copy()


def _apply_changes(user_id: int, values: dict) -> dict:
    with db_lock:
        # La dependencia verificó el ID; también protegemos una eliminación concurrente.
        for user in users_db:
            if user["id"] == user_id:
                if "role" in values:
                    validate_role(values["role"])
                if "email" in values:
                    check_duplicate_email(values["email"], exclude_id=user_id)
                user.update(values)
                return user.copy()
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Usuario no encontrado")


def update_user(user: dict, data: UserUpdate) -> dict:
    return _apply_changes(user["id"], data.model_dump())


def patch_user(user: dict, data: UserPatch) -> dict:
    values = data.model_dump(exclude_unset=True)
    if not values:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
                            "Debe enviar al menos un campo para actualizar")
    return _apply_changes(user["id"], values)


def delete_user(user: dict) -> None:
    with db_lock:
        for index, stored_user in enumerate(users_db):
            if stored_user["id"] == user["id"]:
                users_db.pop(index)
                return
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Usuario no encontrado")
