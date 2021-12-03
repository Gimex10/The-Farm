import re
from .models import *

# used to get the total flock


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
        if n.flock_breedtype == 'Broiler':
            broilers_count.append(n.flock_quantity)

        else:
            layers_count.append(n.flock_quantity)

    broilers_quantity = sum(broilers_count)
    layers_quantity = sum(layers_count)

    # print('broilers', broilers_quantity)
    # print(layers_quantity)
    # print(active_flock)
    # print(results)
    return {"broilers_quantity": broilers_quantity,
            "layers_quantity": layers_quantity}


def close_flock(id):
    flock = Flock.objects.get(id=id)
    if flock.flock_quantity == 0:
        flock.is_closed = True
        flock.save()
        print('is closed updated')


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
    if not re.match('^[a-zA-Z]*$', name):
        return False
    # Names can't begin with a number
    if name[0].isnumeric():
        return False
    return True
