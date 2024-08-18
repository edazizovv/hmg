#


#
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

"""
market = 'moex-akcii'
name = 'sberbank'
code = 'SBER'
day_from = '1'
month_from = '12'
year_from = '2022'
day_to = '2'
month_to = '12'
year_to = '2022'
filename = 'nein'
extension = '.txt'
"""

market = 'moex-akcii'
name = 'pllc-yandex-n-v'
code = 'YNDX'
day_from = '1'
month_from = '12'
year_from = '2022'
day_to = '2'
month_to = '12'
year_to = '2022'
filename = 'nein'
extension = '.txt'


query_new = "https://export.finam.ru/{filename}{extension}" \
            "?market=1&em=3&token=&code={code}&apply=0&from={day_from}.{month_from}.{year_from}" \
            "&to={day_to}.{month_to}.{year_to}&p=2&f={filename}&e={extension}&cn={code}&dtf=1&tmf=1&MSOR=1&mstime=on&mstimever=1" \
            "&sep=1&sep2=1&datf=1&at=1&fsp=1".format(market=market, name=name, code=code,
                                                     day_from=day_from, month_from=month_from, year_from=year_from,
                                                     day_to=day_to, month_to=month_to, year_to=year_to,
                                                     filename=filename, extension=extension)

print(query_new)
"""
options = Options()
# options.add_argument("--headless")
# prefs = {"download.default_directory": "C:/TET/hmg/data"}
options.set_preference("browser.download.dir", "./data")
driver = webdriver.Firefox(options=options)
driver.get(query_new)

time.sleep(5)

driver.close()
"""
#

from selenium.webdriver.firefox.service import Service
from selenium.common.exceptions import TimeoutException
executable_path = 'C:\\TET\\geckodriver-v0.31.0-win64\\geckodriver.exe'
s = Service(executable_path)
# firefoxProfile = webdriver.FirefoxProfile()
# firefoxProfile.set_preference("http.response.timeout", 10)
# firefoxProfile.set_preference("dom.max_script_run_time", 10)
options = Options()
options.add_argument("--headless")
driver = webdriver.Firefox(service=s, options=options) # , firefox_profile=firefoxProfile)
driver.set_page_load_timeout(10)
try:
    driver.get(query_new)
except TimeoutException as e:
    driver.close()
