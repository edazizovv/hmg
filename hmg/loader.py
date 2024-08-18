#
import os


#
import pandas
from dotenv import load_dotenv
from sqlalchemy import create_engine, text, types
from apscheduler.schedulers.background import BlockingScheduler


#
from melee import load
from imoex import get_candles


#
def preprocess_melee(dataframe):
    if dataframe is None:
        null_dataframe = pandas.DataFrame(columns=['datetime', 'close'])
        null_dataframe['datetime'] = pandas.to_datetime(null_dataframe['datetime'])
        null_dataframe['close'] = null_dataframe['close'].astype(dtype='float64')

        return null_dataframe

    else:
        dataframe['datetime'] = pandas.to_datetime(
            dataframe['<DATE>'].astype(dtype=str) + dataframe['<TIME>'].apply(func=lambda x: str(x).zfill(6)),
            format='%Y%m%d%H%M%S')
        dataframe = dataframe.rename(columns={'<CLOSE>': 'close'})
        dataframe = dataframe[['datetime', 'close']].copy()
        return dataframe


def preprocess_imoex(dataframe):
    if dataframe is None:
        null_dataframe = pandas.DataFrame(columns=['datetime', 'close'])
        null_dataframe['datetime'] = pandas.to_datetime(null_dataframe['datetime'])
        null_dataframe['close'] = null_dataframe['close'].astype(dtype='float64')

    else:
        dataframe = dataframe.rename(columns={'begin': 'datetime'})
        dataframe['datetime'] = pandas.to_datetime(dataframe['datetime'])
        dataframe = dataframe[['datetime', 'close']].copy()
        return dataframe


def update_db(dataframe, connection):

    dataframe.to_sql(name='tmp_candles', con=connection, if_exists='replace', index=False,
                     dtype={'datetime': types.DateTime, 'ticker': types.Text, 'close': types.Numeric})
    connection.commit()

    query_update_select_drop = """
    DROP TABLE IF EXISTS tmp_update_candles
    ;
    """
    query_update_select = """
    CREATE TABLE tmp_update_candles AS
    SELECT tc.*
    FROM tmp_candles AS tc
    INNER JOIN candles AS c
    ON tc.datetime = c.datetime
    AND tc.ticker = c.ticker
    ;
    """

    connection.execute(text(query_update_select_drop))
    connection.commit()
    connection.execute(text(query_update_select))
    connection.commit()

    query_append_select_drop = """
    DROP TABLE IF EXISTS tmp_append_candles
    ;
    """
    query_append_select = """
    CREATE TABLE tmp_append_candles AS
    SELECT tc.*
    FROM tmp_candles AS tc
    LEFT JOIN candles AS c
    ON tc.datetime = c.datetime
    AND tc.ticker = c.ticker
    WHERE c.datetime IS NULL 
    AND c.ticker IS NULL
    ;
    """

    connection.execute(text(query_append_select_drop))
    connection.commit()
    connection.execute(text(query_append_select))
    connection.commit()

    query_update_select_done = """
    UPDATE candles
    SET datetime = tuc.datetime, ticker = tuc.ticker, close = tuc.close
    FROM tmp_update_candles AS tuc
    WHERE candles.datetime = tuc.datetime
    AND candles.ticker = tuc.ticker
    ;
    """

    connection.execute(text(query_update_select_done))
    connection.commit()
    pass

    query_append_select_done = """
    INSERT INTO candles
    SELECT *
    FROM tmp_append_candles
    ;
    """

    connection.execute(text(query_append_select_done))
    connection.commit()
    pass


load_dotenv()

DB_FILENAME = os.getenv('DB_FILENAME')

"""
conn_str = "sqlite:///db/{0}.db".format(
    DB_FILENAME
)
"""
conn_str = "postgresql+psycopg2://{0}:{1}@localhost/{2}".format(
    'tester', '12345', 'testy'
)
conn = create_engine(conn_str, future=True)

sched = BlockingScheduler()


import time
import datetime


@sched.scheduled_job('interval', id='nato', minutes=10)
def total_load():

    print("Starting a job at {0}".format(datetime.datetime.now().isoformat()))
    run_time = time.time()

    with conn.connect() as connection:

        data_usdrub = load(market='mosbirzha-valyutnyj-rynok', name='usdrubtod-usd-rub', code='USD000000TOD')
        data_cnyrub = load(market='mosbirzha-valyutnyj-rynok', name='cny-rubtod-cny-rub', code='CNY000000TOD')
        data_eurusd = load(market='mosbirzha-valyutnyj-rynok', name='eur-usdtod-eur-usd', code='EURUSD000TOD')

        data_spx = load(market='mirovye-indeksy', name='sandp-500', code='INX')

        data_ngas = load(market='tovary', name='natural-gas', code='NG')
        data_gold = load(market='tovary', name='gold', code='GC')
        data_brent = load(market='tovary', name='brent', code='BZ')

        sber__data = get_candles(engine='stock', market='shares', security='SBER')
        gasp__data = get_candles(engine='stock', market='shares', security='GAZP')
        gmkn__data = get_candles(engine='stock', market='shares', security='GMKN')
        yndx__data = get_candles(engine='stock', market='shares', security='YNDX')
        lkoh__data = get_candles(engine='stock', market='shares', security='LKOH')
        rosn__data = get_candles(engine='stock', market='shares', security='ROSN')
        imoex__data = get_candles(engine='stock', market='shares', security='IMOEX')

        data_usdrub = preprocess_melee(data_usdrub)
        data_cnyrub = preprocess_melee(data_cnyrub)
        data_eurusd = preprocess_melee(data_eurusd)

        data_spx = preprocess_melee(data_spx)

        data_ngas = preprocess_melee(data_ngas)
        data_gold = preprocess_melee(data_gold)
        data_brent = preprocess_melee(data_brent)

        sber__data = preprocess_imoex(sber__data)
        gasp__data = preprocess_imoex(gasp__data)
        gmkn__data = preprocess_imoex(gmkn__data)
        yndx__data = preprocess_imoex(yndx__data)
        lkoh__data = preprocess_imoex(lkoh__data)
        rosn__data = preprocess_imoex(rosn__data)
        imoex__data = preprocess_imoex(imoex__data)

        data_usdrub['ticker'] = 'USDRUB'
        data_cnyrub['ticker'] = 'CNYRUB'
        data_eurusd['ticker'] = 'EURUSD'

        data_spx['ticker'] = 'SPX'

        data_ngas['ticker'] = 'NGAS'
        data_gold['ticker'] = 'GOLD'
        data_brent['ticker'] = 'BRENT'

        sber__data['ticker'] = 'SBER'
        gasp__data['ticker'] = 'GASP'
        gmkn__data['ticker'] = 'GMKN'
        yndx__data['ticker'] = 'YNDX'
        lkoh__data['ticker'] = 'LKOH'
        rosn__data['ticker'] = 'ROSN'
        imoex__data['ticker'] = 'IMOEX'

        joint_data = pandas.concat((data_usdrub, data_cnyrub, data_eurusd,
                                    data_spx,
                                    data_ngas, data_gold, data_brent,
                                    sber__data, gasp__data, gmkn__data, yndx__data, lkoh__data, rosn__data, imoex__data))

        update_db(dataframe=joint_data, connection=connection)
        connection.close()

    print("Finishing the job at {0}".format(datetime.datetime.now().isoformat()))
    run_time = time.time() - run_time
    print("Time spent: {0} min".format(run_time / 60))

# total_load()
# run_time = time.time() - run_time


sched.start()
