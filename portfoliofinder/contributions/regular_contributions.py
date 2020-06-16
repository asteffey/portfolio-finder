from .contributions import Contributions


class RegularContributions(Contributions):  # pylint: disable=too-few-public-methods
    """This should be used when annual contributions are made to a portfolio."""
    def __init__(self, starting_value: float, annual_contribution: float):
        """Creates regular contributions.

        :param starting_value: initial contribution made at portfolio inception
        :param annual_contribution: subsequent annual contributions
        """
        self.starting_value = starting_value
        self.annual_contribution = annual_contribution

    def get_contribution_for_year(self, year: int):
        if year == 0:
            return self.starting_value
        return self.annual_contribution
