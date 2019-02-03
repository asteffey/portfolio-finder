from collections import namedtuple

ALL_FUNDS = ['USA_TSM', 'GLD', 'EM', 'USA_INF', 'RISK_FREE']
SPECIFIC_FUNDS = ['USA_TSM', 'GLD', 'EM']

def get_expected_portfolio_allocation():
    PortfolioAllocation = namedtuple('PortfolioAllocation', SPECIFIC_FUNDS)
    return [PortfolioAllocation(0, 1, 0),
            PortfolioAllocation(0, 0.75, 0.25),
            PortfolioAllocation(0, 0.5, 0.5),
            PortfolioAllocation(0, 0.25, 0.75),
            PortfolioAllocation(0, 0, 1),
            PortfolioAllocation(0.25, 0.75, 0),
            PortfolioAllocation(0.25, 0.5, 0.25),
            PortfolioAllocation(0.25, 0.25, 0.5),
            PortfolioAllocation(0.25, 0, 0.75),
            PortfolioAllocation(0.5, 0.5, 0),
            PortfolioAllocation(0.5, 0.25, 0.25),
            PortfolioAllocation(0.5, 0, 0.5),
            PortfolioAllocation(0.75, 0.25, 0),
            PortfolioAllocation(0.75, 0, 0.25),
            PortfolioAllocation(1, 0, 0)]
