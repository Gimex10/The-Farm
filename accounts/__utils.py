import re
from .models import *

# used to get the total flock for both breeds


def get_total_flock():
    flock = Flock.objects.all()

    active_flock = []
    broilers_count = []
    layers_count = []
    results = []
    for i in flock:

        results.append(i)

        active_flock.append(i.flock_quantity)

    for n in results:
        if n.flock_breedtype == "Broiler":
            broilers_count.append(n.flock_quantity)

        else:
            layers_count.append(n.flock_quantity)

    broilers_quantity = sum(broilers_count)
    layers_quantity = sum(layers_count)

    return {"broilers_quantity": broilers_quantity, "layers_quantity": layers_quantity}

# automatically closes flock when its count gets to zero


def close_flock(id):
    flock = Flock.objects.get(id=id)
    if flock.flock_quantity == 0:
        flock.is_closed = True
        flock.save()
        print("is closed updated")

# validates the users first and last name during registration


def validate_name(name):
    minlen = len(name)
    # """Checks if the received username matches the required conditions."""
    if type(name) != str:
        raise TypeError("Name must be a string")
    if minlen < 1:
        raise ValueError("minlen must be at least 1")

    # Names can't be shorter than minlen
    if len(name) < minlen:
        return False
    # Names can only use letters
    if not re.match("^[a-zA-Z]*$", name):
        return False
    # Names can't begin with a number
    if name[0].isnumeric():
        return False
    return True


# Adds income after an order has been processed


def addIncome(order):
    print("Added income")
    print(order)
    print(order.order_quantity)

    b = Income(order_id=order.id,
               order_income=order.product.price * order.order_quantity)
    b.save()

# Confirm order and Cascade changes


def confirm_order(id):

    order = Order.objects.get(id=id)
    flock_count_ordered = order.order_quantity
    order.is_paid = True
    order.is_accepted = True
    order.save()
    print('order just billed and accepted', order)

    total_flock = get_total_flock()
    broilers_total = int(total_flock["broilers_quantity"])
    layers_total = int(total_flock["layers_quantity"])

    if order.product.name == "Broiler":

        if flock_count_ordered <= broilers_total:

            broiler_flock_affected = Flock.objects.filter(
                flock_breedtype='Broiler')

            broiler_list = []
            for n in broiler_flock_affected:
                broiler_list.append(n)

            deduct_list = []
            for v in broiler_list:
                if v.flock_quantity >= flock_count_ordered:
                    deduct_list.append(v)

            flock_deducted = deduct_list[0]

            print('initial count', flock_deducted.flock_quantity)

            current_broiler_count = flock_deducted.flock_quantity

            flock_deducted.flock_quantity = current_broiler_count - flock_count_ordered

            flock_deducted.save()

    else:

        if flock_count_ordered <= layers_total:

            layers_flock_affected = Flock.objects.filter(
                flock_breedtype='Layers')

            layers_list = []
            for j in layers_flock_affected:
                layers_list.append(j)

            deduction_list = []
            for w in layers_list:
                if w.flock_quantity >= flock_count_ordered:
                    deduction_list.append(w)

            flock_deduction = deduction_list[0]

            print('initial count', flock_deduction.flock_quantity)

            current_layer_count = flock_deduction.flock_quantity

            flock_deduction.flock_quantity = current_layer_count - flock_count_ordered

            flock_deduction.save()

    # print('Income added')
    # print(order)
    # print(deduct_list)
    addIncome(order)

    return True
