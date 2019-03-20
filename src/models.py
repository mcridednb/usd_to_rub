import decimal

from src import utils


class Rate:
    def __init__(self):
        self.rate, self.date = utils.get_initial()

    def convert(self, amount: decimal.Decimal) -> decimal.Decimal:
        return round(self.rate * amount, 2)
