from django.urls import path
from wallets.views import (
    CreateDepositView,
    CreateWalletView,
    RetrieveWalletView,
    ScheduleWithdrawView,
)

urlpatterns = [
    path("", CreateWalletView.as_view(), name="create-view"),
    path("<uuid>/", RetrieveWalletView.as_view(), name="retrieve-view"),
    path("<uuid>/deposit", CreateDepositView.as_view(), name="deposit"),
    path("<uuid>/withdraw", ScheduleWithdrawView.as_view(), name="withdraw"),
]
