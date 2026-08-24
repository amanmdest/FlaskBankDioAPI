from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from src.app import db


class Transfer(db.Model):
    __tablename__ = 'transfers'

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    account_id: Mapped[int] = mapped_column(
        sa.ForeignKey('accounts.id', ondelete='CASCADE'), nullable=False
        )
    amount: Mapped[int] = mapped_column(sa.Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime, server_default=sa.func.now()
    )

    def __repr__(self) -> str:
        return f'''Transfer(id={self.id!r},
                account_id={self.account_id!r},
                amount={self.amount!r},
                created_at={self.created_at!r})'''

    def to_dict(self):
            return {
                "id": self.id,
                "account_id": self.account_id,
                "amount": self.amount,
                "created_at": self.created_at
            }
