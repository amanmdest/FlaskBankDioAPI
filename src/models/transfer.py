from datetime import datetime
from enum import Enum

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from src.app import db


class TransferType(str, Enum):
    deposit = 'deposit'
    withdraw = 'withdraw'


class Transfer(db.Model):
    __tablename__ = 'transfers'

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    account_id: Mapped[int] = mapped_column(
        sa.ForeignKey('accounts.id', ondelete='CASCADE'), nullable=False
        )
    amount: Mapped[int] = mapped_column(sa.Float, nullable=False)
    transfer_type: Mapped[TransferType]
    description: Mapped[str] = mapped_column(sa.String(100))
    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime, server_default=sa.func.now()
    )

    def __repr__(self) -> str:
        return f'''Transfer(id={self.id!r},
                account_id={self.account_id!r},
                amount={self.amount!r}'''

    def to_dict(self):
            return {
                "id": self.id,
                "account_id": self.account_id,
                "amount": self.amount,
                "description": self.description
            }
