from abc import ABC, abstractmethod

class Contributions(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def get_contribution_for_year(self, year):
        pass

