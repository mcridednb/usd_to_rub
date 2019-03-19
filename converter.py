import decimal

import models
import utils


rate = models.Rate(*utils.get_initial())

try:
    amount = utils.get_amount()
    result = rate.convert(amount)
except decimal.InvalidOperation:
    raise SystemExit('Error. Invalid amount')
else:
    print(f'Курс доллара по состоянию на {rate.date}: {rate.rate} rub')
    print(f'{amount} USD in RUB: {result}')
