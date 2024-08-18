
n_days = 200
ticker = 'EURUSD'


# In[14]:


import numpy
import pandas

from melee import load
from imoex import get_candles
from sqlalchemy import create_engine, text


# In[15]:


conn_str = "postgresql+psycopg2://{0}:{1}@localhost/{2}".format(
    '', '', ''
)
conn = create_engine(conn_str, future=True)


# In[16]:


n_days = int(n_days)
n_days += 1


# In[22]:


query = """
SELECT *
FROM candles
WHERE datetime BETWEEN NOW() - INTERVAL '{0} DAYS' AND NOW()
AND ticker = '{1}'
;
""".format(n_days, ticker)

print(query)

with conn.connect() as connection:
    target_data = pandas.read_sql(sql=text(query), con=connection, index_col='datetime', parse_dates=['datetime'])
print(target_data)


# In[23]:


def calculate_stats(dataframe, frequency, ewm_days):

    frequency_multipliers = {'1h': 1,
                             '4h': 4,
                             '1d': 24}
    m = frequency_multipliers[frequency]
    index = [dataframe.index.max() + pandas.tseries.offsets.DateOffset(hours=-j * m) for j in range((dataframe.shape[0] // (60 * m)) + 1)]
    index = pandas.to_datetime(index)

    masked = numpy.isin(dataframe.index.values, index)
    selected = dataframe[masked].copy()

    resulted = selected['close'].ewm(com=ewm_days).mean()

    return resulted



# In[24]:


target_data['{0}_EWM_21'.format(ticker)] = calculate_stats(dataframe=target_data, frequency='1h', ewm_days=1)
# target_data['{0}_EWM_21'.format(ticker)] = calculate_stats(dataframe=target_data, frequency='1h', ewm_days=21)
# target_data['{0}_EWM_55'.format(ticker)] = calculate_stats(dataframe=target_data, frequency='1h', ewm_days=55)

target_data = target_data.rename(columns={'ticker': ticker})
print(target_data)


# In[25]:


target_data.plot()


# In[27]:


print(target_data[~target_data['EURUSD_EWM_21'].isna()])


# In[28]:


print(target_data)


# In[ ]:




