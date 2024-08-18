#
import pandas_datareader.data as web

#


#


#
APIKEY = ''

start = '2021-11-29'
end = '2022-11-30'
"""
df = web.DataReader('GE', 'yahoo', start=start, end=end)
actions = web.DataReader('GOOG', 'yahoo-actions', start, end)
dividends = web.DataReader('IBM', 'yahoo-dividends', start, end)
"""

# av_data = web.get_quote_av(["AAPL", "TSLA"])
'''
f = web.DataReader("USD/JPY", "av-forex-daily", start=start, end=end,
                   api_key=APIKEY)

g = web.DataReader("AAPL", "av-intraday", start=start,
                       end=end,
                      api_key=APIKEY)
'''
data = web.DataReader("SBER", "moex", start=start, end=end)
# get_quote_av

# f = web.DataReader(["USD/JPY", "BTC/CNY"], "av-forex",
#                     api_key=os.getenv('ALPHAVANTAGE_API_KEY'))

# av_sector = web.get_sector_performance_av()


"""
export.finam.ru/SBER_20170101_20171231.csv?market=0&em=3&code=SBER&apply=0&df=1&mf=0&yf=2017&from=2017-01-01&dt=31&mt=11&yt=2017&to=2017-12-31&p=7&f=SBER_20170101_20171231&e=.csv&cn=SBER&dtf=1&tmf=1&MSOR=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1
https://www.finam.ru/profile/moex-akcii/adr-sberbank-of-russia-ord-shs_sber-me-liqo/export/?market=1&em=2854942&token=&code=SBER-ME&apply=0&df=30&mf=10&yf=2022&from=30.11.2022&dt=30&mt=10&yt=2022&to=30.11.2022&p=7&f=SBER-ME_221130_221130&e=.txt&cn=SBER-ME&dtf=1&tmf=1&MSOR=1&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1
https://www.finam.ru/profile/moex-akcii/sberbank/export/?market=1&em=3&token=&code=SBER&apply=0&df=30&mf=10&yf=2022&from=30.11.2022&dt=30&mt=10&yt=2022&to=30.11.2022&p=2&f=SBER_221130_221130&e=.csv&cn=SBER&dtf=1&tmf=1&MSOR=1&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1&fsp=1
"""

a = "https://www.finam.ru/profile/moex-akcii/sberbank/export/" \
    "?market=1&em=3&token=&code=SBER&apply=0&df=30&mf=10&yf=2022&from=30.11.2022&dt=30&mt=10&yt=2022" \
    "&to=30.11.2022&p=2&f=SBER_221130_221130&e=.csv&cn=SBER&dtf=1&tmf=1&MSOR=1&mstime=on&mstimever=1" \
    "&sep=1&sep2=1&datf=1&at=1&fsp=1"


