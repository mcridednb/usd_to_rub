import decimal
import sys

from src import models
from src import utils



def start():
    rate = models.Rate()
    try:
        amount = utils.get_amount(sys.argv[1:])
        result = rate.convert(amount)
    except decimal.InvalidOperation:
        raise SystemExit('Error. Invalid amount')
    else:
        print(f'Dollar exchange rate as of {rate.date.strftime("%m/%d/%Y")}: {rate.rate} rubles')
        print(f'{amount} USD in RUB: {result}')


if __name__ == "__main__":
    start()
