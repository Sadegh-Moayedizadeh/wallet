from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from wallets.models import Wallet
from wallets.serializers import WalletSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


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
            required=['amount'],
            properties={
                'amount': openapi.Schema(type=openapi.TYPE_INTEGER)
            }
        )
    )
    def post(self, request, uuid, *args, **kwargs):
        deposit_amount = request.data.get('amount')

        try:
            wallet = Wallet.objects.get(uuid=uuid)
        except Wallet.DoesNotExist:
            return Response({"error": "Wallet not found."}, status=status.HTTP_404_NOT_FOUND)

        wallet.deposit(deposit_amount)

        serializer = WalletSerializer(wallet)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ScheduleWithdrawView(APIView):
    def post(self, request, *args, **kwargs):
        # todo: implement withdraw logic
        pass
        return Response({})
