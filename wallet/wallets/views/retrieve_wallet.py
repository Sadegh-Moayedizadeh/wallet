from rest_framework.generics import RetrieveAPIView
from wallets.models import Wallet
from wallets.serializers import WalletSerializer


class RetrieveWalletView(RetrieveAPIView):
    serializer_class = WalletSerializer
    queryset = Wallet.objects.all()
    lookup_field = "uuid"
