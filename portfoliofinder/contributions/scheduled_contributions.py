from .contributions import Contributions

class ScheduledContributions(Contributions):
    def __init__(self, scheduled_contributions):
        self.scheduled_contributions = scheduled_contributions

    def get_contribution_for_year(self, year):
        if year in self.scheduled_contributions:
            return self.scheduled_contributions[year]
        else:
            return 0