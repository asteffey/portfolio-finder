from typing import Dict

from .contributions import Contributions


class ScheduledContributions(Contributions):  # pylint: disable=too-few-public-methods
    """Contributions which occur at specific years in the life of the portfolio."""
    def __init__(self, scheduled_contributions: Dict[int, float]):
        """Creates scheduled contributions.

        :param scheduled_contributions: contributions by year relative to inception of portfolio
        """
        self.scheduled_contributions = scheduled_contributions

    def get_contribution_for_year(self, year):
        if year in self.scheduled_contributions:
            return self.scheduled_contributions[year]
        return 0
