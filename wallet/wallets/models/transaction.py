import uuid
from enum import Enum

from django.db import models
from wallets.models.wallet import Wallet


class Transaction(models.Model):
    class Type(Enum):
        DEPOSIT = "deposit"
        WITHDRAW = "withdraw"

    class Status(Enum):
        PENDING = "pending"
        COMPLETED = "completed"
        CANCELED = "canceled"

    _TYPE_CHOICES = [
        (Type.DEPOSIT, "Deposit"),
        (Type.WITHDRAW, "Withdraw"),
    ]

    _STATUS_CHOICES = [
        (Status.PENDING, "Pending"),
        (Status.COMPLETED, "Completed"),
        (Status.CANCELED, "Canceled"),
    ]

    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    amount = models.PositiveBigIntegerField()
    type = models.CharField(max_length=10, choices=_TYPE_CHOICES)
    status = models.CharField(
        max_length=10, choices=_STATUS_CHOICES, default=Status.PENDING.value
    )
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class WithdrawTransaction(Transaction):
    scheduled_timestamp = models.DateTimeField()


class DepositTransaction(Transaction):
    pass
