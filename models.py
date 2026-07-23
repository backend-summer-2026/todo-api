from sqlalchemy import Boolean, create_engine, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine

# postgresql+psycopg2://foydalanuvchi:parol@host:port/baza
DB_URL = "postgresql+psycopg2://djumanov:Djcjder1120@localhost:5432/dokon_db"
engine = create_engine(DB_URL, echo=False)  # echo=True qilsangiz SQL'ni ko'rasiz
async_engine = create_async_engine(DB_URL, echo=False)


class Base(DeclarativeBase):
    pass


class Tasks(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(128))
    description: Mapped[str] = mapped_column(Text)
    status: Mapped[bool] = mapped_column(Boolean)
