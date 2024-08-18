#


#
import pandas
from sqlalchemy import create_engine, text

#


#
# import sqlite3
# con = sqlite3.connect("db/overseer.db")

conn_str = "postgresql+psycopg2://{0}:{1}@localhost/{2}".format(
    'tester', '12345', 'testy'
)

conn = create_engine(conn_str, future=True)

query = """
CREATE TABLE candles (
  datetime timestamp,
  close numeric,
  ticker text
)
;
"""

with conn.connect() as connection:
    connection.execute(text(query))
    connection.commit()

    data = pandas.read_sql(sql='candles', con=connection)


