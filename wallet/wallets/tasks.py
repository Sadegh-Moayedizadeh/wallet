from celery import shared_task
from wallets.models import WithdrawTransaction
from wallets.utils import request_third_party_deposit


@shared_task
def process_withdrawal(transaction_id):
    transaction = WithdrawTransaction.objects.get(pk=transaction_id)

    response = request_third_party_deposit()

    if response.get("status") == 200:
        transaction.status = WithdrawTransaction.Status.COMPLETED.value
    else:
        transaction.status = WithdrawTransaction.Status.CANCELED.value
        wallet = transaction.wallet
        wallet.deposit(transaction.amount)

    transaction.save()
