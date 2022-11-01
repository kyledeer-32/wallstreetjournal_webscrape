from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver import EdgeOptions
from selenium.webdriver.common.by import By
from selenium import webdriver
import pandas as pd
import time
import datetime as dt

def save_financial_data(ticker, name, df):
    save_path = "C:\\Users\\kyled\\OneDrive\\Kyle\\Coding\\coding_projects\\costco_strat_mgmt\\wscrape_files"
    fname = f"{ticker}_{name}.xlsx"
    df.to_excel(f"{save_path}{fname}", index=False)
    print(f"{fname} saved to: {save_path}")

def get_wsj_homepage(user, pw, save_path):
    s = Service(executable_path=EdgeChromiumDriverManager().install())
    o = EdgeOptions()

    args = ['start-maximized']

    for arg in args:
        o.add_argument(arg)
    
    o.add_experimental_option('prefs', {'download.default_directory':save_path})

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
    driver.get(f'https://www.wsj.com/market-data/quotes/{ticker}')
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
    df_news.columns = ['date', 'source', 'headline', 'link']

    #save table to folder
    name = "headlines"
    save_financial_data(ticker, name, df_news)

    #return to homepage
    driver.back()
    time.sleep(3)

    return df_news

def get_income_statement_annual(driver, ticker):
    #####
    #data to get: income statement annual
    driver.get(f'https://www.wsj.com/market-data/quotes/{ticker}/financials/annual/income-statement')
    time.sleep(5)

    html = driver.page_source

    inc_stmt = pd.read_html(html, attrs= {'class':'cr_dataTable'})
    df_inc = inc_stmt[0]
    df_inc.drop(axis=1, labels='5-year trend', inplace=True)
    col_names = list(df_inc)
    col_name = str(col_names[0])
    df_inc.rename(columns = {col_name:'measure'}, inplace=True)

    #save table to folder
    name = "income_statement_yrs"
    save_financial_data(ticker, name, df_inc)

    #return to homepage
    driver.back()
    time.sleep(3)
    return df_inc

def get_income_statement_quarter(driver, ticker):
    #####
    #data to get: income statement quarter
    driver.get(f'https://www.wsj.com/market-data/quotes/{ticker}/financials/quarter/income-statement')
    time.sleep(5)

    html = driver.page_source

    inc_stmt = pd.read_html(html, attrs= {'class':'cr_dataTable'})
    df_incqtr = inc_stmt[0]
    df_incqtr.drop(axis=1, labels='5-qtr trend', inplace=True)
    col_names = list(df_incqtr)
    col_name = str(col_names[0])
    df_incqtr.rename(columns = {col_name:'measure'}, inplace=True)

    #save table to folder
    name = "income_statement_qtrs"
    save_financial_data(ticker, name, df_incqtr)

    #return to homepage
    driver.back()
    time.sleep(3)
    return df_incqtr

def get_balance_sheet_annual(driver, ticker):
    ###
    #data to get: balance sheet annual
    driver.get(f'https://www.wsj.com/market-data/quotes/{ticker}/financials/annual/balance-sheet')
    time.sleep(5)

    html = driver.page_source

    inc_stmt = pd.read_html(html, attrs= {'class':'cr_dataTable'})
    df_bs = inc_stmt[0]
    df_bs.drop(axis=1, labels='5-year trend', inplace=True)
    col_names = list(df_bs)
    col_name = str(col_names[0])
    df_bs.rename(columns = {col_name:'measure'}, inplace=True)

    #save table to folder
    name = "balance_sheet"
    save_financial_data(ticker, name, df_bs)

    #return to homepage
    driver.back()
    time.sleep(3)
    return df_bs

def get_balance_sheet_quarter(driver, ticker):
    ###
    #data to get: balance sheet quarter
    driver.get(f'https://www.wsj.com/market-data/quotes/{ticker}/financials/quarter/balance-sheet')
    time.sleep(5)

    html = driver.page_source

    inc_stmt = pd.read_html(html, attrs= {'class':'cr_dataTable'})
    df_bsqtr = inc_stmt[0]
    df_bsqtr.drop(axis=1, labels='5-qtr trend', inplace=True)
    col_names = list(df_bsqtr)
    col_name = str(col_names[0])
    df_bsqtr.rename(columns = {col_name:'measure'}, inplace=True)

    #save table to folder
    name = "balance_sheet_qtrs"
    save_financial_data(ticker, name, df_bsqtr)

    #return to homepage
    driver.back()
    time.sleep(3)
    return df_bsqtr

def get_cashflows_annual(driver, ticker):
    ###
    #data to get: statement of cash flows annual
    driver.get(f'https://www.wsj.com/market-data/quotes/{ticker}/financials/annual/cash-flow')

    time.sleep(5)

    html = driver.page_source

    inc_stmt = pd.read_html(html, attrs= {'class':'cr_dataTable'})
    df_cfs = inc_stmt[0]
    df_cfs.drop(axis=1, labels='5-year trend', inplace=True)
    col_names = list(df_cfs)
    col_name = str(col_names[0])
    df_cfs.rename(columns = {col_name:'measure'}, inplace=True)

    #save table to folder
    name = "cashflows"
    save_financial_data(ticker, name, df_cfs)

    #return to homepage
    driver.back()
    time.sleep(3)
    return df_cfs

def get_cashflows_quarter(driver, ticker):
    ###
    #data to get: statement of cash flows quarter
    driver.get(f'https://www.wsj.com/market-data/quotes/{ticker}/financials/quarter/cash-flow')
    time.sleep(5)

    html = driver.page_source

    inc_stmt = pd.read_html(html, attrs= {'class':'cr_dataTable'})
    df_cfsqtr = inc_stmt[0]
    df_cfsqtr.drop(axis=1, labels='5-qtr trend', inplace=True)
    col_names = list(df_cfsqtr)
    col_name = str(col_names[0])
    df_cfsqtr.rename(columns = {col_name:'measure'}, inplace=True)

    #save table to folder
    name = "cashflows_qtrs"
    save_financial_data(ticker, name, df_cfsqtr)

    #return to homepage
    driver.back()
    time.sleep(3)
    return df_cfsqtr

def get_histprices(driver, ticker):
    #####
    #data to get: all historical prices PARAMS: Dates: (##/##/1984 - today)
    driver.get(f'https://www.wsj.com/market-data/quotes/{ticker}/historical-prices')

    # <input type="text" value="07/31/2022" class="datePicker hasDatepicker" id="selectDateFrom">
    driver.find_element(By.XPATH, "//input[@id='selectDateFrom']").clear()
    driver.find_element(By.XPATH, "//input[@id='selectDateFrom']").send_keys("01/01/1900")

    # <input type="text" value="10/29/2022" class="datePicker hasDatepicker" id="selectDateTo">
    # driver.find_element(By.XPATH, "//input[@id='selectDateTo']").send_keys(f"{todate}")

    # <input type="button" value="go" id="datPickerButton">
    driver.find_element(By.XPATH, "//input[@id='datPickerButton']").click()

    # <a href="#" class="dl_button" id="dl_spreadsheet">Download a Spreadsheet</a>
    driver.find_element(By.XPATH, "//a[@id='dl_spreadsheet']").click()
    time.sleep(10)

    # return to homepage
    driver.back()
    time.sleep(3)

def get_profile(driver, ticker):
    #####
    #data to get: Key people (board of directors, All executives), Average Growth Rates, Insider Trading, Ownership (mutual funds that own COST, Institutions that own COST)
    
    driver.get(f'https://www.wsj.com/market-data/quotes/{ticker}/company-people')
    time.sleep(5)

    divs = driver.find_elements(By.TAG_NAME, 'div')
    data_divs = {}
    i = 1
    for div in divs:
        if 'zonedModule' in div.get_attribute('class'):
            if 'company' in div.get_attribute('data-module-zone'):
                id = div.get_attribute('data-module-id')
                name = div.get_attribute('data-module-name')
                zone = div.get_attribute('data-module-zone')
                data_divs[zone] = div
                #print(f"{i}: {id} --- {name} --- {zone}")
                i += 1

    print(data_divs)

    all_uls = driver.find_elements(By.TAG_NAME, 'ul')
    cr_uls = []
    i = 1
    for ul in all_uls:
        if 'cr' in ul.get_attribute('class'):
            cr_uls.append(ul)
            print(i, ul.get_attribute('class'))
            i += 1
    
    for ul in cr_uls:
        elements = ul.find_elements(By.TAG_NAME, 'span')

def main(driver, ticker):
    get_headlines(driver, ticker)
    get_income_statement_annual(driver, ticker)
    get_income_statement_quarter(driver, ticker)
    get_balance_sheet_annual(driver, ticker)
    get_balance_sheet_quarter(driver, ticker)
    get_cashflows_annual(driver, ticker)
    get_cashflows_quarter(driver, ticker)
    #get_histprices(driver, ticker)
    


