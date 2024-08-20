from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class BulbModel(db.Model):
    __tablename__ = "bulbs"

    id: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column(unique=True)