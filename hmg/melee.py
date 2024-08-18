#
import os
import time
import datetime

#
import pandas
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import InvalidSessionIdException

#


#
def load(market, name, code, frequency='1m'):

    frequency_codes = {'1m': "/html/body/div[19]/div/ul/li[2]/a",
                       '1h': "/html/body/div[19]/div/ul/li[7]/a"}

    day_from = '07'
    month_from = '12'
    year_from = '2022'
    day_to = '07'
    month_to = '12'
    year_to = '2022'
    filename = 'onetwo'
    extension = '.csv'

    query_url = "https://www.finam.ru/profile/{market}/{name}/export/" \
                "?market=1&em=3&token=&code={code}&apply=0&df={day_from}&mf={month_from}&yf={year_from}&from={day_from}.{month_from}.{year_from}&dt={day_to}&mt={month_to}&yt={year_to}" \
                "&to={day_to}.{month_to}.{year_to}&p=2&f=EinsZweiPolizei&e={extension}&cn={code}&dtf=1&tmf=1&MSOR=1&mstime=on&mstimever=1" \
                "&sep=1&sep2=1&datf=1&at=1&fsp=1".format(market=market, name=name, code=code,
                                                         day_from=day_from, month_from=month_from, year_from=year_from,
                                                         day_to=day_to, month_to=month_to, year_to=year_to,
                                                         extension=extension)

    from selenium.webdriver.firefox.service import Service
    from selenium.common.exceptions import TimeoutException
    executable_path = 'C:\\TET\\geckodriver-v0.31.0-win64\\geckodriver.exe'
    s = Service(executable_path)
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')

    driver = webdriver.Firefox(service=s, options=options)
    # driver.set_page_load_timeout(20)

    write_down_key = 'DIGGAH'

    try:
        driver.get(query_url)
        time.sleep(1)
        nein = "/html/body/div[3]/div/div[3]/div/table/tbody/tr/td/div/div/div[2]/div[2]/div/div[2]/div[1]/form/table/tbody/tr[1]/td[3]/div/div[1]"
        elem = driver.find_element(By.XPATH, nein)
        elem.click()
        time.sleep(1)

        nein = frequency_codes[frequency]
        delay = 60
        elem = WebDriverWait(driver, delay).until(expected_conditions.presence_of_element_located((
            By.XPATH, nein)))
        # elem = driver.find_element(By.XPATH, nein)
        elem.click()
        time.sleep(1)

        nein = '//*[@id="issuer-profile-export-file-name"]'
        elem = driver.find_element(By.XPATH, nein)
        elem.send_keys(Keys.CONTROL + "a")
        time.sleep(1)
        elem.send_keys(write_down_key)

        nein = "/html/body/div[3]/div/div[3]/div/table/tbody/tr/td/div/div/div[2]/div[2]/div/div[2]/div[1]/form/div/button/span"
        elem = driver.find_element(By.XPATH, nein)
        elem.click()
        time.sleep(20)

        driver.close()

        default_address = 'C:/Users/Edward/Downloads/'
        result_data = pandas.read_csv('{0}{1}.txt'.format(default_address, write_down_key))
        os.remove('{0}{1}.txt'.format(default_address, write_down_key))

        print('DONE: {0} / {1}'.format(datetime.datetime.now().isoformat(), name))

        return result_data

    except TimeoutException as e:
        print("TimeoutException")
        print(e)
        driver.get_screenshot_as_file("./screenshot.png")
        driver.close()

        return None

    except pandas.errors.EmptyDataError as e:
        print("EmptyDataError")
        print(e)

        default_address = 'C:/Users/Edward/Downloads/'
        os.remove('{0}{1}.txt'.format(default_address, write_down_key))

        return None

    except Exception as e:
        print("UndefinedException")
        print(e)
        try:
            driver.get_screenshot_as_file("./screenshot.png")
            driver.close()
        except InvalidSessionIdException as e:
            pass

        default_address = 'C:/Users/Edward/Downloads/'
        os.remove('{0}{1}.txt'.format(default_address, write_down_key))

        return None






"""
market = 'mosbirzha-valyutnyj-rynok'
name = 'usdrubtod-usd-rub'
code = 'USD000000TOD'
"""
'''
data_usdrub = load(market='mosbirzha-valyutnyj-rynok', name='usdrubtod-usd-rub', code='USD000000TOD')
data_cnyrub = load(market='mosbirzha-valyutnyj-rynok', name='cny-rubtod-cny-rub', code='CNY000000TOD')
data_eurusd = load(market='mosbirzha-valyutnyj-rynok', name='eur-usdtod-eur-usd', code='EURUSD000TOD')

data_spx = load(market='mirovye-indeksy', name='sandp-500', code='INX')

data_ngas = load(market='tovary', name='natural-gas', code='NG')
data_gold = load(market='tovary', name='gold', code='GC')
data_brent = load(market='tovary', name='brent', code='BZ')
'''