import urllib.parse
import urllib.request
import urllib.error
import json
import datetime
import decimal
import argparse

import constants


def get_current() -> decimal.Decimal:
    query = urllib.parse.urlencode({'q': constants.TYPE, 'apiKey': constants.API_KEY, 'compact': 'ultra'})
    response = urllib.request.urlopen(f'{constants.BASE_URL}?{query}')
    result = json.loads(response.read()).get(constants.TYPE)
    return round(decimal.Decimal(result), 4)


def save_rate_to_cache(rate: decimal.Decimal) -> datetime.date:
    date = datetime.datetime.today().date()
    data = {
        'rate': float(round(rate, 4)),
        'date': date.strftime("%d.%m.%Y")
    }
    with open(constants.CACHE_FILE_NAME, 'w') as fp:
        json.dump(data, fp)
    return date


def load_rate_from_cache() -> tuple:
    with open(constants.CACHE_FILE_NAME, 'rb') as fp:
        cached_rate = json.load(fp)
    return (
        round(decimal.Decimal(cached_rate['rate']), 4),
        datetime.datetime.strptime(cached_rate['date'], '%d.%m.%Y').date()
    )


def get_amount(args) -> decimal.Decimal:
    parser = argparse.ArgumentParser(description='USD -> RUB converter.')
    parser.add_argument('amount', type=decimal.Decimal, help='Amount of money to exchange')
    args_ = parser.parse_args(args)
    return round(args_.amount, 4)


def get_initial() -> tuple:
    try:
        rate = get_current()
    except urllib.error.URLError:
        try:
            rate, date = load_rate_from_cache()
        except FileNotFoundError:
            raise SystemExit('Failed to load current rate')
    else:
        date = save_rate_to_cache(rate)
    return rate, date
