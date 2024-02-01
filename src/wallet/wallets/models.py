import uuid
from enum import Enum
from django.db import models


class Wallet(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    balance = models.BigIntegerField(default=0)

    def deposit(self, amount: int):
        self.balance += amount
        self.save()


class Transaction(models.Model):
    class Type(Enum):
        DEPOSIT = "deposit"
        WITHDRAW = "withdraw"

    class Status(Enum):
        PENDING = 'pending'
        COMPLETED = 'completed'
        CANCELED = 'canceled'

    _TYPE_CHOICES = [
        (Type.DEPOSIT, "Deposit"),
        (Type.WITHDRAW, "Withdraw"),
    ]

    _STATUS_CHOICES = [
        (Status.PENDING, 'Pending'),
        (Status.COMPLETED, 'Completed'),
        (Status.CANCELED, 'Canceled'),
    ]

    amount = models.BigIntegerField()
    type = models.CharField(max_length=10, choices=_TYPE_CHOICES)
    status = models.CharField(max_length=10, choices=_STATUS_CHOICES, default=Status.PENDING)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
