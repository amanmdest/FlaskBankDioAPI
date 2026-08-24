import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.app import db
from src.models.user import User


class Role(db.Model):
    __tablename__ = 'roles'

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(sa.String, nullable=False, unique=True)
    users: Mapped[list['User']] = relationship(back_populates='role')

    def __repr__(self) -> str:
        return f'Role(id={self.id!r}, \
            name={self.name!r})'
