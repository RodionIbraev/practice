import os
import uuid
from dotenv import load_dotenv
from yookassa import Configuration, Payment
from RocketNet.models import Account, BalanceChange


load_dotenv()
Configuration.account_id = os.getenv("ACCOUNT_ID")
Configuration.secret_key = os.getenv("SHOP_SECRET_KEY")


def create_payment(serialized_data):
    data = serialized_data
    user_id = data.get('user_id')
    value = data.get('value')
    return_url = data.get('return_url')
    user_account = Account.objects.get(user_id=user_id)

    balance_change = BalanceChange.objects.create(
        account_id=user_account.id,
        amount=value,
        payment_uuid=None,
        is_accepted=False,
        operation_type='DEPOSIT',
    )

    payment = Payment.create({
        'amount': {
            'value': value,
            'currency': 'RUB',
        },
        'confirmation': {
            'type': 'redirect',
            'return_url': return_url + f"{balance_change.id}/",
        },
        'metadata': {
            'table_id': balance_change.id,
            'user_account_id': user_account.id,
        },
        'capture': True,
        'description': 'Пополнение на ' + str(value),
    }, uuid.uuid4())

    balance_change.payment_uuid = payment.id
    balance_change.save()

    return payment
