import decimal

import sys

import models
import utils


def start():
    rate = models.Rate(*utils.get_initial())
    date = rate.date.strftime("%d.%m.%Y")
    try:
        amount = utils.get_amount(sys.argv[1:])
        result = rate.convert(amount)
    except decimal.InvalidOperation:
        raise SystemExit('Error. Invalid amount')
    else:
        print(f'Курс доллара по состоянию на {date}: {rate.rate} rub')
        print(f'{amount} USD in RUB: {result}')


if __name__ == "__main__":
    start()