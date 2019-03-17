from itertools import combinations
from math import floor
from collections import namedtuple

class count_in_bin_enumeration:
    def __init__(self, object_count, bin_count):
        # each combination will be the location of dividers which divide up the objects
        self._combos = combinations(range(object_count+bin_count-1),bin_count-1)
        self._ceiling = object_count + bin_count - 1

    def __iter__(self):
        return self
    
    def __next__(self):
        try:
            divider_locations = (-1,) + next(self._combos) + (self._ceiling,)
            return tuple(map(lambda n: divider_locations[n] - divider_locations[n-1] - 1, range(1, len(divider_locations))))
        except StopIteration:
            raise StopIteration

class range_of_allocations:
    def __init__(self, step, bin_count):
        self._step_reciprocal = floor(1 / step)
        self._count_in_bin_enumeration = count_in_bin_enumeration(self._step_reciprocal, bin_count)

    def __iter__(self):
        return self

    def __next__(self):
        return tuple(map(lambda n : n / self._step_reciprocal, next(self._count_in_bin_enumeration)))

class named_range_of_allocations:
    def __init__(self, step, field_names):
        self._namedtuple_type = namedtuple('Allocation', field_names)
        self._range_of_allocations = range_of_allocations(step, len(field_names))

    def __iter__(self):
        return self

    def __next__(self):
        return self._namedtuple_type(*next(self._range_of_allocations))

def create_portfolio_allocations(step, symbols):
    return list(named_range_of_allocations(step, symbols))