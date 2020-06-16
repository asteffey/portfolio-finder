from .data_by_startyear_by_allocation import _DataByStartYearByAllocation
from .portfolio_timeframe_by_startyear import _get_portfolio_timeframe_by_startyear
from .contributions import Contributions


class PortfolioTimeframesByStartYearByAllocation(_DataByStartYearByAllocation):
    """Timeframes for portfolio to achieve a target value, by start year
    and allocation mix, for a specific contributions schedule.
    """

    def __init__(self, portfolio_returns_by_allocation: dict,
                 target_value: float, contributions: Contributions):
        _DataByStartYearByAllocation.__init__(self,
                                              _get_portfolio_timeframe_by_startyear,
                                              portfolio_returns_by_allocation,
                                              target_value,
                                              contributions)
