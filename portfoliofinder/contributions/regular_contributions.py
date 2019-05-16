from .contributions import Contributions

class RegularContributions(Contributions):
    def __init__(self, starting_value, annual_contribution):
        self.starting_value = starting_value
        self.annual_contribution = annual_contribution

    def get_contribution_for_year(self, year):
        if year==0:
            return self.starting_value
        else:
            return self.annual_contribution