import pytest
from django.urls import reverse
from rest_framework import status
from wallets.models import Wallet
from unittest.mock import Mock, patch
from django.utils import timezone
from datetime import timedelta


@pytest.fixture
def wallet():
    return Wallet.objects.create(balance=1000)


@pytest.fixture
def payload(wallet):
    return {"amount": 100, "uuid": wallet.uuid}


@pytest.mark.django_db
def test_create_deposit_should_add_to_wallets_balance(client, payload, wallet):
    # Arrange
    url = reverse("create-deposit", kwargs={"uuid": wallet.uuid})

    initial_balance = wallet.balance
    deposit_amount = 100
    payload = {"amount": deposit_amount, "uuid": wallet.uuid}

    # Act
    response = client.post(url, data=payload, format="json")

    updated_wallet = Wallet.objects.get(uuid=wallet.uuid)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert updated_wallet.balance == initial_balance + deposit_amount


@pytest.mark.django_db
def test_schedule_withdraw_when_amount_is_more_than_balance_should_fail(wallet, client):
    # Arrange
    url = reverse("schedule-withdraw", kwargs={"uuid": wallet.uuid})
    initial_balance = wallet.balance
    withdraw_amount = initial_balance + 500
    payload = {"amount": withdraw_amount, "uuid": wallet.uuid, "scheduled_timestamp": "2025-01-01"}

    # Act
    response = client.post(url, data=payload, format="json")

    updated_wallet = Wallet.objects.get(uuid=wallet.uuid)

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert updated_wallet.balance == initial_balance


@pytest.mark.django_db
def test_schedule_withdraw_when_date_is_in_wrong_format_should_fail(wallet, client):
    # Arrange
    url = reverse("schedule-withdraw", kwargs={"uuid": wallet.uuid})
    initial_balance = wallet.balance
    withdraw_amount = 500
    payload = {"amount": withdraw_amount, "uuid": wallet.uuid, "scheduled_timestamp": "invalid-date"}

    # Act
    response = client.post(url, data=payload, format="json")

    updated_wallet = Wallet.objects.get(uuid=wallet.uuid)

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert updated_wallet.balance == initial_balance


@pytest.mark.django_db
def test_schedule_withdraw_with_success_should_reduce_wallets_balance(wallet, client):
    # Arrange
    url = reverse("schedule-withdraw", kwargs={"uuid": wallet.uuid})
    initial_balance = wallet.balance
    withdraw_amount = 500
    payload = {"amount": withdraw_amount, "uuid": wallet.uuid, "scheduled_timestamp": "2025-01-01"}

    # Act
    with patch("wallets.tasks.process_withdrawal.apply_async") as mock_apply_async:
        mock_apply_async.return_value = Mock(state="PENDING")
        response = client.post(url, data=payload, format="json")

    updated_wallet = Wallet.objects.get(uuid=wallet.uuid)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert updated_wallet.balance == initial_balance - withdraw_amount
