import json
import unittest
import decimal

import datetime

import os
import urllib.error

import constants
import models
import utils


class TestApp(unittest.TestCase):
    def setUp(self):
        self.rate = decimal.Decimal('64.2612')
        self.date = datetime.datetime.today().date()

    def test_get_current(self):
        try:
            self.assertTrue(isinstance(utils.get_current(), decimal.Decimal))
        except urllib.error.URLError:
            pass

    def test_save_to_cache(self):
        self.assertEqual(utils.save_rate_to_cache(self.rate), self.date)
        with open(constants.CACHE_FILE_NAME, 'rb') as fp:
            cached_rate = json.load(fp)['rate']
        self.assertEqual(float(self.rate), cached_rate)

    def test_load_rate_from_cache(self):
        utils.save_rate_to_cache(self.rate)
        rate, date = utils.load_rate_from_cache()
        self.assertEqual(self.rate, rate)
        self.assertEqual(self.date, date)
        os.remove(constants.CACHE_FILE_NAME)
        self.assertRaises(FileNotFoundError, utils.load_rate_from_cache)

    def test_get_amount(self):
        amount = utils.get_amount(['1000'])
        self.assertEqual(decimal.Decimal('1000'), amount)
        self.assertRaises(decimal.InvalidOperation, utils.get_amount, ['abc'])
        self.assertRaises(decimal.InvalidOperation, utils.get_amount, ['10000000000000000000000000'])
        self.assertRaises(SystemExit, utils.get_amount, ['10', '12', '14'])

    def test_initial_rate(self):
        rate = models.Rate(*utils.get_initial())
        self.assertTrue(isinstance(rate, models.Rate))
        self.assertTrue(isinstance(rate.rate, decimal.Decimal))
        self.assertTrue(isinstance(rate.date, datetime.date))
