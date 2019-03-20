import argparse
import datetime
import decimal
import json
import logging.config
import urllib.error
import urllib.parse
import urllib.request

from src import constants

logging.config.fileConfig('logger.conf')
logger = logging.getLogger('converter')


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


def get_amount(args: list) -> decimal.Decimal:
    parser = argparse.ArgumentParser(description='USD -> RUB converter.')
    parser.add_argument('amount', type=decimal.Decimal, help='Amount of money to exchange')
    args_ = parser.parse_args(args)
    return round(args_.amount, 4)


def get_initial() -> tuple:
    try:
        logger.info('Trying to get the current rate from API...')
        rate = get_current()
    except urllib.error.URLError as e:
        logger.error(f'Failed to load the current rate from API. Error from server: {e}')
        try:
            logger.info('Trying to get the current rate from the cache...')
            rate, date = load_rate_from_cache()
        except FileNotFoundError:
            logger.error('Failed to load the current rate from the cache')
            raise SystemExit('Failed to load the current rate')
        logger.info('Success to load the current rate from cache')
        return rate, date
    logger.info('Success to load the current rate from API')
    date = save_rate_to_cache(rate)
    return rate, date
