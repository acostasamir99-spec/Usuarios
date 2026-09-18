from fastapi import HTTPException, status

from app.dependencies.database_dependency import DatabaseSession
from app.models.user_model import User

from app.services.user_service import find_user


def get_user_or_404(user_id: int, db: DatabaseSession) -> User:
    """Resolver el usuario solicitado antes de ejecutar la ruta."""
    user = find_user(db, user_id)
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Usuario no encontrado")
    return user
