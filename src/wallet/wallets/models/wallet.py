import uuid
from enum import Enum

from django.db import models


class Wallet(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    balance = models.BigIntegerField(default=0)

    def deposit(self, amount: int):
        self.balance += amount
        self.save()
