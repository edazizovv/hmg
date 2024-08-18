

import pandas
from sqlalchemy import create_engine, text

engine = create_engine("postgresql+psycopg2://tester:12345@localhost/testy", future=True)

with engine.connect() as conn:

    # data = pandas.DataFrame(data={'other': [1,2,3,4,5,], 'butch': ['a', 'Q', 'c', 'XYZ', 'XX']})
    # data.to_sql(name='dummy', con=conn, if_exists='replace')

    query = """
    UPDATE one
    SET second = p.butch, index = p.index
    FROM dummy AS p
    WHERE p.other = one.none
    ;
    """

    conn.execute(text(query))
    conn.commit()

    """
    UPDATE candles
    SET candles.datetime = tmp_update_candles.datetime, candles.ticker = tmp_update_candles.ticker, candles.close = tmp_update_candles.close
    FROM tmp_update_candles
    WHERE candles.datetime = tmp_update_candles.datetime
    AND candles.ticker = tmp_update_candles.ticker
    ;
    """
