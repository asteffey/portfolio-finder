from .contributions import Contributions


class InitialContribution(Contributions):  # pylint: disable=too-few-public-methods
    """A single contribution that is made to a portfolio at its inception.

    :param starting_value: initial contribution at inception of portfolio
    """
    def __init__(self, starting_value: float):
        super().__init__()
        self.starting_value = starting_value

    def get_contribution_for_year(self, year):
        if year == 0:
            return self.starting_value
        return 0
