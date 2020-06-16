from .contributions import Contributions


class InitialContribution(Contributions):  # pylint: disable=too-few-public-methods
    """This should be used when only a single contribution is made to a portfolio
    at its inception.
    """
    def __init__(self, starting_value: float):
        """Creates an initial contribution.

        :param starting_value: initial contribution at inception of portfolio
        """
        super().__init__()
        self.starting_value = starting_value

    def get_contribution_for_year(self, year):
        if year == 0:
            return self.starting_value
        return 0
