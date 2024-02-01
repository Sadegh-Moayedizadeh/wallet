from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from wallets.models import Wallet
from wallets.serializers import WalletSerializer


class CreateWalletView(CreateAPIView):
    serializer_class = WalletSerializer


class RetrieveWalletView(RetrieveAPIView):
    serializer_class = WalletSerializer
    queryset = Wallet.objects.all()
    lookup_field = "uuid"


class CreateDepositView(APIView):
    def post(self, request, *args, **kwargs):
        wallet_uuid = request.data.get('wallet_uuid')
        deposit_amount = request.data.get('amount')

        try:
            wallet = Wallet.objects.get(uuid=wallet_uuid)
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
