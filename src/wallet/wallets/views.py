import datetime

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from wallets.models import DepositTransaction, Wallet, WithdrawTransaction
from wallets.serializers import WalletSerializer
from wallets.tasks import process_withdrawal


class CreateWalletView(CreateAPIView):
    serializer_class = WalletSerializer


class RetrieveWalletView(RetrieveAPIView):
    serializer_class = WalletSerializer
    queryset = Wallet.objects.all()
    lookup_field = "uuid"


class CreateDepositView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["amount"],
            properties={"amount": openapi.Schema(type=openapi.TYPE_INTEGER)},
        )
    )
    def post(self, request, uuid, *args, **kwargs):
        deposit_amount = request.data.get("amount")

        try:
            wallet = Wallet.objects.get(uuid=uuid)
        except Wallet.DoesNotExist:
            return Response(
                {"error": "Wallet not found."}, status=status.HTTP_404_NOT_FOUND
            )

        wallet.deposit(deposit_amount)

        transaction = DepositTransaction.objects.create(
            amount=deposit_amount,
            type=DepositTransaction.Type.DEPOSIT,
            wallet=wallet,
            status=DepositTransaction.Status.COMPLETED,
        )

        return Response(
            {"message": "Deposit successful.", "transaction_id": transaction.id},
            status=status.HTTP_200_OK,
        )


class ScheduleWithdrawView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["wallet_uuid", "amount", "scheduled_timestamp"],
            properties={
                "wallet_uuid": openapi.Schema(type=openapi.TYPE_STRING),
                "amount": openapi.Schema(type=openapi.TYPE_NUMBER),
                "scheduled_timestamp": openapi.Schema(type=openapi.FORMAT_DATE),
            },
        ),
        responses={200: "Success", 400: "Bad Request", 404: "Not found"},
        operation_summary="Withdraw from Wallet",
        operation_description="Withdraw a specific amount from a wallet on a scheduled date.",
    )
    def post(self, request, uuid, *args, **kwargs):
        withdraw_amount = request.data.get("amount")

        try:
            wallet = Wallet.objects.get(uuid=uuid)
        except Wallet.DoesNotExist:
            return Response(
                {"error": "Wallet not found."}, status=status.HTTP_404_NOT_FOUND
            )

        try:
            wallet.withdraw(withdraw_amount)
        except ValueError:
            return Response(
                {"error": "The amount specified is more than the current balance."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        scheduled_timestamp = request.data.get("scheduled_timestamp")
        try:
            scheduled_timestamp = datetime.datetime.strptime(
                scheduled_timestamp, "%Y-%m-%d"
            ).date()
        except ValueError:
            return Response(
                {"error": "Invalid date format. Use YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        transaction = WithdrawTransaction.objects.create(
            amount=withdraw_amount,
            type=WithdrawTransaction.Type.WITHDRAW,
            wallet=wallet,
            status=WithdrawTransaction.Status.PENDING,
            scheduled_timestamp=scheduled_timestamp,
        )

        process_withdrawal.apply_async(args=[transaction.id], eta=scheduled_timestamp)

        return Response(
            {"message": "Withdraw successful.", "transaction_id": transaction.id},
            status=status.HTTP_200_OK,
        )
