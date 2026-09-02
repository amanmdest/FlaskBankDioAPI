from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.app import db
from src.models.user import User


class Account(db.Model):
    __tablename__ = 'accounts'

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False
    )
    user: Mapped['User'] = relationship(back_populates='accounts')
    holder: Mapped[str] = mapped_column(sa.String(150), nullable=False)
    balance: Mapped[float] = mapped_column(sa.Float, default=0.0)
    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime, server_default=sa.func.now()
    )

    def __repr__(self) -> str:
        return f'account(id={self.id!r}, \
            user_id={self.user_id!r}, \
            holder={self.holder!r}, \
            balance={self.balance!r}),'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'holder': self.holder,
            'balance': self.balance,
        }
