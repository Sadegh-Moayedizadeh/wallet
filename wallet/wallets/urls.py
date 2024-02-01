from django.urls import path
from wallets.views import (
    CreateDepositView,
    CreateWalletView,
    RetrieveWalletView,
    ScheduleWithdrawView,
)

urlpatterns = [
    path("", CreateWalletView.as_view(), name="wallets"),
    path("<uuid>/", RetrieveWalletView.as_view()),
    path("<uuid>/deposit", CreateDepositView.as_view()),
    path("<uuid>/withdraw", ScheduleWithdrawView.as_view()),
]
