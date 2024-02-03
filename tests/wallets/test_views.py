import pytest
from django.urls import reverse
from rest_framework import status
from wallets.models import Wallet


@pytest.fixture
def wallet():
    return Wallet.objects.create(balance=1000)


@pytest.fixture
def payload(wallet):
    return {"amount": 100, "uuid": wallet.uuid}


@pytest.mark.django_db
def test_create_deposit_should_add_to_wallets_balance(client, payload, wallet):
    # Arrange
    url = reverse("deposit", kwargs={"uuid": wallet.uuid})

    initial_balance = wallet.balance
    deposit_amount = 100
    payload = {"amount": deposit_amount, "uuid": wallet.uuid}

    # Act
    response = client.post(url, data=payload, format="json")

    updated_wallet = Wallet.objects.get(uuid=wallet.uuid)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert updated_wallet.balance == initial_balance + deposit_amount
