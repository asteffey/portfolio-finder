from .data_by_startyear_by_allocation import _DataByStartYearByAllocation
from .portfolio_value_by_startyear import _get_portfolio_value_by_startyear

from .contributions import Contributions


class PortfolioValuesByStartYearByAllocation(_DataByStartYearByAllocation):
    """Portfolio values, by start year and allocation mix,
    for a specific timeframe and contributions schedule.
    """

    def __init__(self, portfolio_returns_by_allocation: dict,
                 timeframe: int, contributions: Contributions):
        _DataByStartYearByAllocation.__init__(self,
                                              _get_portfolio_value_by_startyear,
                                              portfolio_returns_by_allocation,
                                              timeframe,
                                              contributions)
