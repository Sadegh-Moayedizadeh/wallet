from rest_framework.generics import CreateAPIView

from wallets.serializers import WalletSerializer


class CreateWalletView(CreateAPIView):
    serializer_class = WalletSerializer
