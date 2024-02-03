import pytest
from unittest.mock import patch
from wallets.models import WithdrawTransaction, Wallet
from wallets.tasks import process_withdrawal
from datetime import timedelta
from django.utils import timezone


@pytest.fixture
def wallet():
    return Wallet.objects.create(balance=1000)


@pytest.fixture
def transaction(wallet):
    return WithdrawTransaction.objects.create(
        wallet=wallet,
        amount=500,
        type=WithdrawTransaction.Type.WITHDRAW,
        scheduled_timestamp=timezone.now() + timedelta(hours=1),
    )


@pytest.mark.django_db
def test_process_withdrawal_when_third_party_request_is_successful_should_update_transtaction_status_to_completed(transaction):
    # Arrange
    mock_response = {"status": 200}

    # Act
    with patch('wallets.tasks.request_third_party_deposit', return_value=mock_response):
        process_withdrawal(transaction.id)

    # Assert
    updated_transaction = WithdrawTransaction.objects.get(pk=transaction.id)
    assert updated_transaction.status == WithdrawTransaction.Status.COMPLETED.value


@pytest.mark.django_db
def test_process_withdrawal_when_third_party_request_is_not_successful_should_update_transtaction_status_to_canceled(transaction, wallet):
    # Arrange
    mock_response = {"status": 500}

    # Act
    with patch('wallets.tasks.request_third_party_deposit', return_value=mock_response):
        process_withdrawal(transaction.id)

    updated_transaction = WithdrawTransaction.objects.get(pk=transaction.id)

    # Assert
    assert updated_transaction.status == WithdrawTransaction.Status.CANCELED.value


@pytest.mark.django_db
def test_process_withdrawal_when_third_party_request_is_not_successful_should_deposit_back_transaction_amount_to_wallet(transaction, wallet):
    # Arrange
    mock_response = {"status": 500}

    # Act
    with patch('wallets.tasks.request_third_party_deposit', return_value=mock_response):
        process_withdrawal(transaction.id)

    updated_wallet = Wallet.objects.get(uuid=wallet.uuid)

    # Assert
    assert updated_wallet.balance == wallet.balance + transaction.amount
