from typing import Annotated

from fastapi import APIRouter, Depends, Response, status

from app.dependencies.user_dependencies import get_user_or_404
from app.schemas.user_schema import UserCreate, UserPatch, UserResponse, UserUpdate
from app.services import user_service

user_router = APIRouter(prefix="/users", tags=["Users"])
ExistingUser = Annotated[dict, Depends(get_user_or_404)]
NOT_FOUND = {404: {"description": "Usuario no encontrado"}}
BUSINESS_ERROR = {400: {"description": "Rol no permitido, correo duplicado o PATCH vacío"}}


@user_router.get("", response_model=list[UserResponse], status_code=status.HTTP_200_OK,
                 summary="Listar usuarios", description="Lista usuarios y permite combinar role e is_active.",
                 response_description="Usuarios que cumplen los filtros", responses=BUSINESS_ERROR)
def list_users(role: str | None = None, is_active: bool | None = None):
    return user_service.list_users(role, is_active)


@user_router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK,
                 summary="Consultar usuario por ID", description="Consulta un usuario mediante su ID.",
                 response_description="Usuario encontrado", responses=NOT_FOUND)
def get_user(user: ExistingUser):
    return user


@user_router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED,
                  summary="Crear usuario", description="Crea un usuario con correo único y rol admin, support o user.",
                  response_description="Usuario creado con ID generado por el servidor", responses=BUSINESS_ERROR)
def create_user(data: UserCreate):
    return user_service.create_user(data)


@user_router.put("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK,
                 summary="Actualizar usuario completamente", description="Reemplaza los cuatro campos editables; conserva el ID.",
                 response_description="Usuario actualizado", responses=NOT_FOUND | BUSINESS_ERROR)
def update_user(data: UserUpdate, user: ExistingUser):
    return user_service.update_user(user, data)


@user_router.patch("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK,
                   summary="Actualizar usuario parcialmente", description="Modifica únicamente los campos enviados. No admite null ni un objeto vacío.",
                   response_description="Usuario actualizado parcialmente", responses=NOT_FOUND | BUSINESS_ERROR)
def patch_user(data: UserPatch, user: ExistingUser):
    return user_service.patch_user(user, data)


@user_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT,
                    summary="Eliminar usuario", description="Elimina el usuario de la colección en memoria.",
                    response_description="Usuario eliminado; respuesta sin cuerpo", responses=NOT_FOUND)
def delete_user(user: ExistingUser) -> Response:
    user_service.delete_user(user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
