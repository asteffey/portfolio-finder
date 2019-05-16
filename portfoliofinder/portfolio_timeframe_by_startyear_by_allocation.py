from .data_by_startyear_by_allocation import DataByStartYearByAllocation
from .portfolio_timeframe_by_startyear import _get_portfolio_timeframe_by_startyear
from .contributions import Contributions

class PortfolioTimeframesByStartYearByAllocation(DataByStartYearByAllocation):

    def __init__(self, portfolio_returns_by_allocation: dict, target_value, contributions: Contributions):
        DataByStartYearByAllocation.__init__(self,
                                             _get_portfolio_timeframe_by_startyear,
                                             portfolio_returns_by_allocation, target_value, contributions)