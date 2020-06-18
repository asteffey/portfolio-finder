from __future__ import annotations

from itertools import combinations
from math import floor
from typing import Callable, List, Union

import pandas as pd

from .returns import Returns
from ..util.self_pickling import SelfPickling


class Allocations(SelfPickling):
    """A range of portfolio allocations.

    This is the primary starting point when using
    Portfolio Finder.  All other features can be
    reached from here through method chaining,
    starting with `with_returns`.

    **Example:**

    >>> Allocations(0.25, ['A','B'])
          A     B
    0  0.00  1.00
    1  0.25  0.75
    2  0.50  0.50
    3  0.75  0.25
    4  1.00  0.00

    :param step: step amount between each allocation percent
                 (i.e., 0.25 would produce allocations of 0, 0.25, 0.5, 0.75, 1)
    :param funds: fund symbols for allocations
    """

    def __init__(self, step: float, funds: List[str]):
        values = _RangeOfAllocations(step, len(funds))
        self._allocations = pd.DataFrame(values, columns=funds)

    @classmethod
    def _from_dataframe(cls, allocations: pd.DataFrame):
        a = cls.__new__(cls)
        super(Allocations, a).__init__()
        a._allocations = allocations
        return a

    def __repr__(self):
        return self._allocations.__repr__()

    def __str__(self):
        return self._allocations.__str__()

    def as_dataframe(self) -> pd.DataFrame:
        """Gets this as a pandas DataFrame.

        Note that changes to the returned DataFrame will modify this object.
        """
        return self._allocations

    def filter(self, expression: Union[Callable[[pd.DataFrame], pd.Series], str]):
        """Filters the range of allocations.

        **Examples:**

        >>> abc = Allocations(0.25, ['A','B','C'])
        >>> abc.filter(lambda a: (a.A<=0.25) & (a.B>=0.75))
              A     B     C
        3  0.00  0.75  0.25
        4  0.00  1.00  0.00
        8  0.25  0.75  0.00

        >>> xyz = Allocations(0.25, ['X','Y','Z'])
        >>> xyz.filter('X>=0.5 & Z==0')
               X     Y    Z
        11  0.50  0.50  0.0
        13  0.75  0.25  0.0
        14  1.00  0.00  0.0

        :param expression: expression to filter by
        :return: a new instance of Allocations
        """
        if isinstance(expression, str):
            return Allocations._from_dataframe(self._allocations.query(expression))
        if callable(expression):
            return Allocations._from_dataframe(self._allocations[expression(self._allocations)])
        raise ValueError("invalid filter expression")

    def with_returns(self, fund_returns: Union[pd.DataFrame, str], risk_free: str = None) -> Returns:
        """Adds a collection of fund returns, by year, to these portfolio allocations to
        calculate a set of portfolio returns, by year.

        :param fund_returns: a pandas DataFrame or path to CSV file with fund symbols as column headers
        :param risk_free: fund symbol representing the risk free rate from fund_returns
        :return:
        """
        if isinstance(fund_returns, str):
            fund_returns = pd.read_csv(fund_returns, index_col=0)
        elif not isinstance(fund_returns, pd.DataFrame):
            raise TypeError('returns must be a path to csv file or pandas DataFrame')

        if risk_free is not None:
            fund_returns = fund_returns.apply(_adjust_for(fund_returns[risk_free]), axis=1)

        return Returns(fund_returns, self.as_dataframe())


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


def _adjust_for(rates: pd.Series):
    """Creates a function to adjust for a rate.

    :param rates: rate by year to adjust for
    :return: adjusting function
    """
    def _adjust(returns_for_year):
        year = returns_for_year.name
        rate = rates[year]
        return (returns_for_year + 1) / (rate + 1) - 1
    return _adjust
