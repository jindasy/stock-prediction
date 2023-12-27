from stock import *


class Company:
    """Class defined company name and it classes."""
    def __init__(self):
        self.COMPANY = {"Microsoft": Microsoft(),
                        "Google": Google(),
                        "Tesla": Tesla(),
                        "Intel": Intel(),
                        "Meta": Meta(),
                        "Amazon": Amazon(),
                        "Apple": Apple()}

    def __iter__(self):
        """Iterator to get name of company and class name."""
        for name, company in self.COMPANY.items():
            yield name, company
