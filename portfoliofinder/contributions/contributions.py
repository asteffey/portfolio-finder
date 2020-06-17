from abc import ABC, abstractmethod


class Contributions(ABC):  # pylint: disable=too-few-public-methods
    """The contributions made to a portfolio for each year."""
    @abstractmethod
    def get_contribution_for_year(self, year: int):
        """Gets the contribution for the specified year.

        :param year: year relative to inception of portfolio (i.e., first year is 0)
        :return: contribution for the specified year
        """
