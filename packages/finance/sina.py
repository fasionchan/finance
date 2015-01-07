#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   sina.py
Author:     Chen Yanfei
@contact:   fasionchan@gmail.com
@version:   $Id$

Description:

Changelog:

'''

import requests
from decimal import Decimal

REALTIME_URL = 'http://hq.sinajs.cn/?list=%s'

REALTIME_FIELDS_CN = [('corp_code', str), ('corp', str), ('opening', Decimal),
    ('last_closing', Decimal), ('highest', Decimal), ('lowest', Decimal),
    ('closing', Decimal)]

REALTIME_FIELDS_HK = [('corp_code', str), ('corp', str), ('opening', Decimal),
    ('last_closing', Decimal), ('highest', Decimal), ('lowest', Decimal),
    ('closing', Decimal)]

REALTIME_FIELDS_US = [('corp', str), ('closing', Decimal),
    ('percent', Decimal), ('time', str), ('delta', Decimal),
    ('opening', Decimal), ('highest', Decimal), ('lowest', Decimal),
    ('closingg', Decimal)]

FOREX_REALTIME_URL = 'http://hq.sinajs.cn/?list=%s'

FOREX_REALTIME_FIELDS = (('time', str), ('bid', Decimal), ('ask', Decimal),
    ('last_closing', Decimal), ('delta', Decimal), ('opening', Decimal),
    ('highest', Decimal), ('lowest', Decimal), ('closing', Decimal))

class SinaFinance(object):

    def realtime_api(self, *l):
        raw = requests.get(REALTIME_URL % (','.join(l),)).text.encode('utf8')
        return [line.split('"')[1].split(',')
            for line in raw.split('\n') if line]

    def parse_symbol_us(self, loc, symbol):
        return 'gb_%s' % (symbol.lower(),), REALTIME_FIELDS_US

    parse_symbol_nasdaq = parse_symbol_us

    def parse_symbol_cn(self, loc, symbol):
        return '%s%s' % (loc.lower(), symbol), REALTIME_FIELDS_CN

    parse_symbol_sh = parse_symbol_cn
    parse_symbol_sz = parse_symbol_cn

    def parse_symbol_hk(self, loc, symbol):
        return 'hk%s' % (symbol,), REALTIME_FIELDS_HK

    def parse_symbol(self, symbol):
        loc, code = symbol.split('.')
        loc, code = loc.lower(), code.lower()
        fmt, symbol = getattr(self, 'parse_symbol_%s' % (loc,))(loc, code)
        return fmt, symbol

    def realtime(self, *symbols):
        results = []
        for symbol in symbols:
            symbol, fmt = self.parse_symbol(symbol)
            data = self.realtime_api(symbol)[0]
            if data:
                pairs = zip(fmt, data)
                kvs = [(key, cls(value)) for (key, cls), value in pairs]
                results.append(dict(kvs))
        return results

    def forex_realtime_api(self, fr, to='CNY'):
        raw = requests.get(REALTIME_URL % (fr+to,)).text.encode('utf8')
        return [line.split('"')[1].split(',')
            for line in raw.split('\n') if line]


    def forex_realtime(self, fr, to='CNY'):
        data = self.forex_realtime_api(fr)[0]
        return dict([(key, cls(value))
            for (key, cls), value in zip(FOREX_REALTIME_FIELDS, data)])

sina = SinaFinance()

def test():
    print sina.parse_symbol('sh.000002')[0]
    print sina.parse_symbol('sz.000002')[0]

    print sina.parse_symbol('hk.00700')[0]
    print sina.realtime('hk.00700')

    print sina.parse_symbol('nasdaq.jd')[0]
    print sina.realtime('nasdaq.jd')

    print sina.forex_realtime('USD')
    print sina.forex_realtime('HKD')

if __name__ == '__main__':
    test()
