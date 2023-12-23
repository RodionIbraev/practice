from django.core.exceptions import ObjectDoesNotExist
from ..models import BalanceChange
from yookassa import Payment


def payment_acceptance(balance_change_id):
    try:
        balance_change = BalanceChange.objects.get(id=balance_change_id)
    except ObjectDoesNotExist:
        return False
    payment_id = str(balance_change.payment_uuid)
    payment = Payment.find_one(payment_id)

    if payment.status == "succeeded":
        balance_change.is_accepted = True
        balance_change.save()
        return {"result": True, "amount": balance_change.amount}
    return {"result": False, "amount": 0}
