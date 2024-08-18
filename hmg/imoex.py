#
import json
import datetime

#
import urllib3

#


#
import pandas


def get_candles(engine, market, security, frequency='1m', start=None, end=None):
    frequency_codes = {'1m': "1",
                       '1h': "60"}

    http = urllib3.PoolManager()
    '''
    url = 'https://iss.moex.com/iss/engines/{engine}/markets/{market}/securities/{security}/candles.json'.format(
        engine=engine, market=market, security=security)

    query = {
        "from": '2022-12-05',
        "till": '2022-12-05',
        "interval": frequency_codes[frequency],
    }

    encoded_body = json.dumps(query)

    r = http.request('GET', url,
                     headers={'Content-Type': 'application/json'},
                     body=encoded_body)
    '''

    if not start:
        start = str(datetime.date.today())
    if not end:
        end = str(datetime.date.today())

    url = 'https://iss.moex.com/iss/engines/{engine}/markets/{market}/securities/{security}/candles.json' \
          '?from={start}&till={end}&interval={interval}'.format(
        engine=engine, market=market, security=security,
        start=start, end=end, interval=frequency_codes[frequency])

    r = http.request('GET', url,
                     headers={'Content-Type': 'application/json'})

    result = r.data

    data = json.loads(result.decode())

    # data['candles']['metadata']
    # data['candles']['columns']
    # data['candles']['data']

    data_frame = pandas.DataFrame(data=data['candles']['data'], columns=data['candles']['columns'])

    return data_frame


'''
sber__data = get_candles(engine='stock', market='shares', security='SBER')
gasp__data = get_candles(engine='stock', market='shares', security='GAZP')
gmkn__data = get_candles(engine='stock', market='shares', security='GMKN')
yndx__data = get_candles(engine='stock', market='shares', security='YNDX')
lkoh__data = get_candles(engine='stock', market='shares', security='LKOH')
rosn__data = get_candles(engine='stock', market='shares', security='ROSN')
imoex__data = get_candles(engine='stock', market='shares', security='IMOEX')
'''
