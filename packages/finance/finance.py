#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   finance.py
Author:     Chen Yanfei
@contact:   fasionchan@gmail.com
@version:   $Id$

Description:

Changelog:

'''

from decimal import Decimal

from sina import sina as sina_api
from yahoo import yahoo as yahoo_api

REALTIME_FIELDS = ('corp', 'closing', 'last_closing', 'opening', 'highest',
        'lowest')
REALTIME_HEADERS = ('Corp', '实时', '昨收', '今开', '最高', '最低')
#REALTIME_HEADERS = tuple((f.upper() for f in REALTIME_FIELDS))

MARKET2CURRENCY = {
    'hk': 'HKD',
    'nasdaq': 'USD',
}

CURRENCY2NAME = {
    'USD': '美元',
    'HKD': '港元',
    'CNY': '人民币',
}

CURRENCY2SYMBOL = {
    'USD': '$',
    'HKD': 'HK$',
    'CNY': '￥',
}

def unichar_print_len(c):
    if ord(c) <= 127:
        return 1
    else:
        return 2

def print_width(s, encoding='utf8'):
    if not isinstance(s, unicode):
        s = str(s).decode(encoding)
    len = sum([unichar_print_len(c) for c in s])
    return len

def do_print(s, left, right, splits):
    print ' ' * left + s + ' ' * right + ' ' * splits,

def print_center(s, width, l=None, splits=0):
    if l is None:
        l = print_width(s)

    left = (width - l) / 2
    right = width - l - left

    do_print(s, left, right, splits)

def print_left(s, width, l=None, splits=0):
    if l is None:
        l = print_width(s)

    left = 0
    right = width - l

    do_print(s, left, right, splits)

def print_right(s, width, l=None, splits=0):
    if l is None:
        l = print_width(s)

    left = width - l
    right = 0

    do_print(s, left, right, splits)


def print_table(table, encoding='utf8'):
    table = [[(f, print_width(f, encoding=encoding)) for f in r] for r in table]
    widthes = [max([l for _, l in column]) for column in zip(*table)]

    for row in table:
        for width, (value, l) in zip(widthes, row):
            print ' ' * (width - l) + value + ' ' * 1,
            continue
            fmt = '%% %ds' % (l,)
            print fmt % (value,),
        print

class Finance(object):
    def show_realtime(self, *l):
        table = [[str(data.get(f, '')) for f in REALTIME_FIELDS]
            for data in sina_api.realtime(*l)]
        table_header = [REALTIME_HEADERS]
        table_header.extend(table)
        print_table(table_header)

    def market_value(self, stocks):
        value_set = {}
        for stock, number in stocks.iteritems():
            market, symbol = stock.split('.')
            market, symbol = market.lower(), symbol.lower()

            price = sina_api.realtime(stock)[0]['closing']
            value = price * Decimal(int(number))

            currency = MARKET2CURRENCY.get(market)
            value_set[currency] = value_set.setdefault(currency, 0) + value
        return value_set

    def forex_convert(self, frs, to):
        total = Decimal(0)
        for fr, number in frs.iteritems():
            if fr == to:
                total += Decimal(number)
            else:
                forex = sina_api.forex_realtime(fr, to)['closing']
                total += number * forex
        return total

    def show_market_value(self, stocks, cash):
        stock_value = self.market_value(stocks)
        market_value = dict(cash)
        for currency, number in stock_value.iteritems():
            market_value[currency] = \
                market_value.setdefault(currency, Decimal(0)) + Decimal(number)

        headers, values = [], []
        currencies = list(set(market_value))
        currencies.sort()
        for currency in currencies:
            value = stock_value.get(currency)
            if value:
                currency_name = CURRENCY2NAME.get(currency)
                currency_symbol = CURRENCY2SYMBOL.get(currency)
                headers.append('%s证券%s' % (currency_name, currency_symbol))
                values.append('%.2f' % (value,))

            value = cash.get(currency)
            if value:
                currency_name = CURRENCY2NAME.get(currency)
                currency_symbol = CURRENCY2SYMBOL.get(currency)
                headers.append('%s现金%s' % (currency_name, currency_symbol))
                values.append('%.2f' % (value,))

            value = market_value.get(currency)
            if value:
                currency_name = CURRENCY2NAME.get(currency)
                currency_symbol = CURRENCY2SYMBOL.get(currency)
                headers.append('%s合计%s' % (currency_name, currency_symbol))
                values.append('%.2f' % (value,))

        value = self.forex_convert(market_value, 'CNY')
        headers.append('等价人民币￥')
        values.append('%.2f' % (value,))

        print_table([headers, values])

finance = Finance()

def test():
    stocks = {
        'hk.00700': 200,
        'nasdaq.dang': 200,
        'nasdaq.bac': 150,
    }
    print finance.market_value(stocks)
    print

    finance.show_realtime('hk.00700', 'hk.01022', 'nasdaq.jd', 'nasdaq.dang',
            'nasdaq.bac')
    print

    stocks = {
        'hk.00700': 200,
        'hk.01022': 1500,
        'nasdaq.dang': 200,
        'nasdaq.bac': 150,
    }
    cash = {
        'USD': ['79.87'],
        'HKD': ['556.31'],
    }
    cash = {
        c: sum(map(Decimal, ['0'] + v))
        for c, v in cash.iteritems()
    }
    finance.show_market_value(stocks, cash)

if __name__ == '__main__':
    test()
