"""CRUD SQLAlchemy con transacciones y protección contra duplicados."""
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserPatch, UserUpdate

def find_user(db: Session, user_id: int) -> User | None:
    return db.get(User, user_id)

def find_user_by_email(db: Session, email: str) -> User | None:
    return db.scalar(select(User).where(User.email == email))

def check_duplicate_email(db: Session, email: str, exclude_id: int | None = None):
    existing = find_user_by_email(db, email)
    if existing is not None and existing.id != exclude_id:
        raise HTTPException(400, "El correo electrónico ya está registrado")

def list_users(db: Session, role=None, is_active=None, sort_by="name", order="asc"):
    query = select(User)
    if role is not None:
        query = query.where(User.role == role)
    if is_active is not None:
        query = query.where(User.is_active == is_active)
    column = {"name": User.name, "created_at": User.created_at}[sort_by]
    return db.scalars(query.order_by(column.desc() if order == "desc" else column.asc(), User.id)).all()

def _commit(db: Session):
    try:
        db.commit()
    except IntegrityError as error:
        db.rollback()
        if "UNIQUE constraint failed: users.email" in str(error.orig):
            raise HTTPException(400, "El correo electrónico ya está registrado") from error
        raise HTTPException(400, "Los datos incumplen una restricción de la base de datos") from error

def create_user(db: Session, data: UserCreate) -> User:
    check_duplicate_email(db, str(data.email))
    user = User(**data.model_dump())
    db.add(user)
    _commit(db)
    db.refresh(user)
    return user

def _apply_changes(db: Session, user: User, values: dict) -> User:
    if "email" in values:
        check_duplicate_email(db, values["email"], exclude_id=user.id)
    for field, value in values.items():
        setattr(user, field, value)
    _commit(db)
    db.refresh(user)
    return user

def update_user(db: Session, user: User, data: UserUpdate) -> User:
    return _apply_changes(db, user, data.model_dump())

def patch_user(db: Session, user: User, data: UserPatch) -> User:
    values = data.model_dump(exclude_unset=True)
    if not values:
        raise HTTPException(400, "Debe enviar al menos un campo para actualizar")
    return _apply_changes(db, user, values)

def delete_user(db: Session, user: User) -> None:
    db.delete(user)
    _commit(db)
