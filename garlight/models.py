from sqlalchemy.orm import Mapped, mapped_column
from garlight.database import db


class BulbModel(db.Model):
    __tablename__ = "bulbs"

    pk: Mapped[int] = mapped_column(primary_key=True)
    id: Mapped[str] = mapped_column(unique=True)
    ip: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column(unique=True)
