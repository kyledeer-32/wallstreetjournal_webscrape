from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver import EdgeOptions
from selenium.webdriver.common.by import By
from selenium import webdriver
import pandas as pd
import time

def get_wsj_homepage(user, pw):
    s = Service(executable_path=EdgeChromiumDriverManager().install())
    o = EdgeOptions()

    args = ['start-maximized']

    for arg in args:
        o.add_argument(arg)

    driver = webdriver.Edge(service = s, options = o)

    driver.get('https://sso.accounts.dowjones.com/login-page?op=localop&scope=openid%20idp_id%20roles%20email%20given_name%20family_name%20djid%20djUsername%20djStatus%20trackid%20tags%20prts%20suuid%20createTimestamp&client_id=5hssEAdMy0mJTICnJNvC9TXEw3Va7jfO&response_type=code&redirect_uri=https%3A%2F%2Faccounts.wsj.com%2Fauth%2Fsso%2Flogin&nonce=852ff2b9-e4b2-468d-bdbc-5a228d53c7db&ui_locales=en-us-x-wsj-215-2&mars=-1&ns=prod%2Faccounts-wsj&state=Z9WD4d66MqjzkaGc.zs1-lbAjOIIs3TM2DB2zEpmnglSQNQ89lFRCEaBMy34&protocol=oauth2&client=5hssEAdMy0mJTICnJNvC9TXEw3Va7jfO#!/signin')
    time.sleep(5)
    
    driver.find_element(By.XPATH, "//input[@id='username']").send_keys(user)
    driver.find_element(By.XPATH, "//button[@class='solid-button continue-submit new-design']").click()
    time.sleep(5)

    driver.find_element(By.XPATH, "//input[@id='password-login-password']").send_keys(pw)
    driver.find_element(By.XPATH, "//button[@class='solid-button new-design basic-login-submit']").click()
    time.sleep(5)

    return driver

def get_headlines(driver, ticker):
    #####
    #data to get: competitor data, news headlines with dates
    driver.get('https://www.wsj.com/market-data/quotes/{}'.format(ticker))
    time.sleep(5)

    load_more_button = driver.find_element(By.ID, 'latestNewsLoad')

    i = 0
    while i < 10:
        load_more_button.click()
        i += 1
    
    market_news = driver.find_element(By.XPATH, "//ul[@class='WSJTheme--cr_newsSummary--2RNDoLB9 ']")
    metadata = market_news.find_elements(By.CLASS_NAME, 'WSJTheme--cr_metaData--2WQLD8Fb ')

    dates = []
    sources = []

    for element in metadata:
        date = element.find_element(By.CLASS_NAME, 'WSJTheme--cr_dateStamp--13KIPpOo ')
        date = date.get_attribute('innerText')
        dates.append(date)
        source = element.find_element(By.CLASS_NAME, 'WSJTheme--cr_provider--1VY6JXuV ')
        source = source.get_attribute('innerText')
        sources.append(source)

    print(dates)
    print(sources)

    headlines = market_news.find_elements(By.TAG_NAME, 'a')

    hlines = []
    links = []

    for element in headlines:
        hline = element.get_attribute('innerText')
        hlines.append(hline)
        link = element.get_attribute('href')
        links.append(link)

    print(hlines)
    print(links)

    dates = pd.Series(dates)
    sources = pd.Series(sources)
    hlines = pd.Series(hlines)
    links = pd.Series(links)

    slist = [dates, sources, hlines, links]

    df_news = pd.concat(slist, axis=1)
    return df_news