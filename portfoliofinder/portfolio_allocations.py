from __future__ import annotations

from itertools import combinations
from math import floor
from typing import Callable, List, Union

import pandas as pd


class _CountInBinEnumeration:
    def __init__(self, object_count, bin_count):
        # each combination will be the location of dividers which divide up the objects
        self._combos = combinations(
            range(object_count+bin_count-1), bin_count-1)
        self._ceiling = object_count + bin_count - 1

    def __iter__(self):
        return self

    def __next__(self):
        try:
            divider_locations = (-1,) + next(self._combos) + (self._ceiling,)
            return tuple(map(lambda n: divider_locations[n] - divider_locations[n - 1] - 1,
                             range(1, len(divider_locations))))
        except StopIteration:
            raise StopIteration


class _RangeOfAllocations:
    def __init__(self, step, bin_count):
        self._step_reciprocal = floor(1 / step)
        self._count_in_bin_enumeration = _CountInBinEnumeration(
            self._step_reciprocal, bin_count)

    def __iter__(self):
        return self

    def __next__(self):
        return tuple(map(lambda n: n / self._step_reciprocal, next(self._count_in_bin_enumeration)))


class PortfolioAllocations:
    """A range of portfolio allocations.

    For example:
    >>> PortfolioAllocations.from_combo(0.25, ['A','B']).as_dataframe()
          A     B
    0  0.00  1.00
    1  0.25  0.75
    2  0.50  0.50
    3  0.75  0.25
    4  1.00  0.00

    >>> PortfolioAllocations.from_combo(0.25, ['A','B','C']).filter(lambda x: (x.A<=0.25) & (x.B>=0.75)).as_dataframe()
          A     B     C
    3  0.00  0.75  0.25
    4  0.00  1.00  0.00
    8  0.25  0.75  0.00

    >>> PortfolioAllocations.from_combo(0.25, ['A','B','C']).filter('A<=0.25 & B>=0.75').as_dataframe()
          A     B     C
    3  0.00  0.75  0.25
    4  0.00  1.00  0.00
    8  0.25  0.75  0.00
    """
    def __init__(self, allocations: pd.DataFrame):
        """Creates a range of portfolio allocations.

        :param allocations: DataFrame containing allocations
        """
        self._allocations = allocations

    @classmethod
    def from_combo(cls, step: float, symbols: List[str]) -> PortfolioAllocations:
        """Creates a range of portfolio allocations.

        :param step: step amount between each allocation percent
                     (i.e., 0.25 would produce allocations of 0, 0.25, 0.5, 0.75, 1)
        :param symbols: fund symbols for allocations

        :return a range of portfolio allocations
        """
        values = _RangeOfAllocations(step, len(symbols))
        return cls(pd.DataFrame(values, columns=symbols))

    def as_dataframe(self) -> pd.DataFrame:
        """Gets as pandas DataFrame."""
        return self._allocations

    def to_tuples(self):
        return self._allocations.itertuples(name="Allocation", index=False)

    def filter(self, expression: Union[Callable[[pd.DataFrame], pd.Series], str]):
        """Filters the range of allocations."""
        if type(expression) == str:
            return PortfolioAllocations(self._allocations.query(expression))
        elif callable(expression):
            return PortfolioAllocations(self._allocations[expression(self._allocations)])
        else:
            raise ValueError("invalid filter expression")
