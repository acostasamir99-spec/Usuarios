"""Tabla persistente y restricciones de integridad."""
from datetime import datetime, timezone
from sqlalchemy import Boolean, CheckConstraint, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column
from app.database.connection import Base

class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint("length(trim(name)) >= 3", name="ck_users_name"),
        CheckConstraint("role IN ('admin', 'support', 'user')", name="ck_users_role"),
        {"sqlite_autoincrement": True},
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String(collation="NOCASE"), unique=True, nullable=False, index=True)
    role: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(create_constraint=True), nullable=False, default=True, server_default="1")
    # SQLite guarda esta fecha UTC sin información de zona horaria.
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False,
        default=lambda: datetime.now(timezone.utc).replace(tzinfo=None), server_default=func.current_timestamp())
