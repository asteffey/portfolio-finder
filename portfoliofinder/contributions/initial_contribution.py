from .contributions import Contributions

class InitialContribution(Contributions):
    def __init__(self, starting_value):
        self.starting_value = starting_value

    def get_contribution_for_year(self, year):
        if year==0:
            return self.starting_value
        else:
            return 0

