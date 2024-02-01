import uuid

from django.db import models


class Wallet(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    balance = models.BigIntegerField(default=0)

    def deposit(self, amount: int):
        self.balance += amount
        self.save()


class Transaction(models.Model):
    DEPOSIT = "deposit"
    WITHDRAW = "withdraw"

    TRANSACTION_TYPE_CHOICES = [
        (DEPOSIT, "Deposit"),
        (WITHDRAW, "Withdraw"),
    ]

    amount = models.BigIntegerField()
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
