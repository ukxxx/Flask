import os

from sqlalchemy import DateTime, String, create_engine, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "secret")
POSTGRES_USER = os.getenv("POSTGRES_USER", "app")
POSTGRES_DB = os.getenv("POSTGRES_DB", "app")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5431")

PG_DSN = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(PG_DSN)
Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class Advert(Base):
    __tablename__ = "app_adverts"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(100), unique=True, index=True, nullable=False
    )
    description: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    owner_id: Mapped[int] = mapped_column(nullable=False)

    @property
    def dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at,
            "owner_id": self.owner_id,
        }


class User(Base):
    __tablename__ = "app_users"
    id: Mapped[int] = mapped_column(primary_key=True)
    mail: Mapped[str] = mapped_column(
        String(100), unique=True, index=True, nullable=False
    )
    password: Mapped[str] = mapped_column(String(100), nullable=False)

    @property
    def dict(self) -> dict:
        return {"id": self.id, "mail": self.mail, "password": self.password}


# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
