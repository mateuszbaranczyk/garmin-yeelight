from sqlalchemy.orm import Mapped, mapped_column

from garlight.db.database import db


class BulbModel(db.Model):
    __tablename__ = "bulbs"

    pk: Mapped[int] = mapped_column(primary_key=True)
    id: Mapped[str] = mapped_column(unique=True)
    ip: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column(unique=True)

    def as_dict(self):
        dict_repr = self.__dict__
        return dict_repr
