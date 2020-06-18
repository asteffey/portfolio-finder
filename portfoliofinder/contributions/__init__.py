"""
##############################
Portfolio Finder Contributions
##############################

Contains different approaches to make contributions to a portfolio each year.
"""

from .contributions import Contributions
from .initial_contribution import InitialContribution
from .regular_contributions import RegularContributions
from .scheduled_contributions import ScheduledContributions

DEFAULT_CONTRIBUTION = InitialContribution(10000)
"""The default contribution option is simply a $10,000 initial investment."""
