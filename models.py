import decimal


class Rate:
    def __init__(self, rate, date):
        self.rate, self.date = rate, date

    def convert(self, amount: decimal.Decimal) -> decimal.Decimal:
        return round(self.rate * amount, 2)
