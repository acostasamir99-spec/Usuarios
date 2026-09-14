"""Validación de datos con Pydantic v2; los roles se validan en el servicio."""

from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, StringConstraints, field_validator

UserName = Annotated[str, StringConstraints(strip_whitespace=True, min_length=3)]


class UserBase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: UserName
    email: EmailStr
    role: str
    is_active: bool = True


class UserCreate(UserBase):
    """El cliente no puede enviar un ID."""


class UserUpdate(UserBase):
    is_active: bool


class UserPatch(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: UserName | None = None
    email: EmailStr | None = None
    role: str | None = None
    is_active: bool | None = None

    @field_validator("name", "email", "role", "is_active", mode="before")
    @classmethod
    def reject_explicit_null(cls, value):
        # Omitir un campo es válido; enviar null no debe borrar datos requeridos.
        if value is None:
            raise ValueError("El campo no admite null")
        return value


class UserResponse(UserBase):
    id: int
