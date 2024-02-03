from rest_framework import serializers
from wallets.models import Wallet, WithdrawTransaction


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ("uuid", "balance")
        read_only_fields = ("uuid", "balance")


class WithdrawTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WithdrawTransaction
        fields = ("uuid", "amount", "type", "status", "wallet", "scheduled_timestamp")
