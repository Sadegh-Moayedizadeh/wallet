# Generated by Django 5.0.1 on 2024-02-03 12:37

import wallets.models.transaction
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("wallets", "0002_auto_20240201_1419"),
    ]

    operations = [
        migrations.AlterField(
            model_name="deposittransaction",
            name="status",
            field=models.CharField(
                choices=[
                    (
                        wallets.models.transaction.Transaction.Status["PENDING"],
                        "Pending",
                    ),
                    (
                        wallets.models.transaction.Transaction.Status["COMPLETED"],
                        "Completed",
                    ),
                    (
                        wallets.models.transaction.Transaction.Status["CANCELED"],
                        "Canceled",
                    ),
                ],
                default="pending",
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="withdrawtransaction",
            name="status",
            field=models.CharField(
                choices=[
                    (
                        wallets.models.transaction.Transaction.Status["PENDING"],
                        "Pending",
                    ),
                    (
                        wallets.models.transaction.Transaction.Status["COMPLETED"],
                        "Completed",
                    ),
                    (
                        wallets.models.transaction.Transaction.Status["CANCELED"],
                        "Canceled",
                    ),
                ],
                default="pending",
                max_length=10,
            ),
        ),
    ]