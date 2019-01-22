from itertools import combinations

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
    def __init__(self, precision, bin_count):
        self._count_in_bin_enumeration = count_in_bin_enumeration(precision, bin_count)
        self._precision = precision

    def __iter__(self):
        return self

    def __next__(self):
        return tuple(map(lambda n : n / self._precision, next(self._count_in_bin_enumeration)))

