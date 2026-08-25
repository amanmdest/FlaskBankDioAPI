from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.app import db
from src.models.account import Account


class User(db.Model):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    username: Mapped[str] = mapped_column(
        sa.String, unique=True, nullable=False
    )
    password: Mapped[str] = mapped_column(sa.String, nullable=False)
    role_id: Mapped[int] = mapped_column(
         sa.ForeignKey('roles.id'), nullable=False
    )
    role: Mapped['Role'] = relationship(back_populates='users')  # type: ignore
    accounts: Mapped[list['Account']] = relationship()
    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime, server_default=sa.func.now()
    )

    def __repr__(self) -> str:
        return f'User(id={self.id!r}, \
            username={self.username!r}), \
            role={self.role!r}, \
            accounts={self.accounts!r})'

    def to_dict(self):
            return {
                "id": self.id,
                "username": self.username,
                "role": self.role.name if self.role else None,
                # Transforma a lista de contas em uma lista de dicionários ou apenas IDs
                "accounts": [account.id for account in self.accounts]
            }
