import uuid

from django.db import models


class Transaction(models.Model):
    amount = models.BigIntegerField()
    # todo: add fields if necessary
    pass


class Wallet(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    balance = models.BigIntegerField(default=0)

    def deposit(self, amount: int):
        self.balance += amount
        self.save()
