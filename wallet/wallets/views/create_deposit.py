from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from wallets.models import DepositTransaction, Wallet


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
            type=DepositTransaction.Type.DEPOSIT.value,
            wallet=wallet,
            status=DepositTransaction.Status.COMPLETED.value,
        )

        return Response(
            {"message": "Deposit successful.", "transaction_id": transaction.id},
            status=status.HTTP_200_OK,
        )
