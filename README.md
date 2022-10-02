# wallstreetjournal_webscrape
Python module for obtaining public company data by web scraping from WSJ market data home and returning pandas dataframes. Use requires WSJ subscription.

## Functions
### get_wsj_homepage([user], [pw])
params: [user] = Wall Street Journal Login Username, [pw] = Wall Street Journal Login Password
returns Edge webdriver

### get_headlines([driver], [ticker])
params: [driver] = pass Edge webdriver at WSJ homepage (this is retrieved by calling "get_wsj_homepage" fn), [ticker] = ticker for desired company, e.g., for Costco pass 'COST'
returns pandas dataframe with headlines, dates, sources, and links
