
import datetime
from imoex import get_candles

yesterday = str(datetime.date.today() - datetime.timedelta(days=1))
# sber__data = get_candles(engine='stock', market='shares', security='SBER', start=yesterday, end=yesterday)
sber__data = get_candles(engine='stock', market='shares', security='SBER')
