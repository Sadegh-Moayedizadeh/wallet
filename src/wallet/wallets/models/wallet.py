import uuid

from django.db import models, transaction


class Wallet(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    balance = models.PositiveBigIntegerField(default=0)

    def deposit(self, amount: int):
        self.balance += amount
        self.save()

    def withdraw(self, amount: int):
        if amount <= 0:
            raise ValueError("The ampunt should be a positive number.")

        with transaction.atomic():
            current_balance = Wallet.objects.select_for_update().get(id=self.id).balance
            if amount > current_balance:
                raise ValueError("Insufficient balance for withdrawal.")

            self.balance = current_balance - amount
            self.save()
