import random
import numpy as np

def rand_max(iterable, key=None):
#max function where the tie brakes are random
    if key is None:
        key = lambda x: x

    max_v = -np.inf
    max_l = []

    for item, value in zip(iterable, [key(i) for i in iterable]):
        if value == max_v:
            max_l.append(item)
        elif value > max_v:
            max_l = [item]
            max_v = value

    return random.choice(max_l)

def first_max(iterable):
#max function where the first max key found is the one chosen
    return max(iterable)