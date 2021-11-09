# What companies are reporting earnings 
#   today after market hours and 
#   tomorrow before market hours?

# Gathers data from at least 3 sources
# Crosschecks, marks the overlapping info
# Output in the form: common: TICKER1, TICKER2, ...; outliers: TICKER5, TICKER6, ...

# 
# https://www.youtube.com/watch?v=2tigfln9kv8

import datetime
import pandas as pd # pip install pandas

# Requests allows you to send HTTP/1.1 requests
import requests # pip install requests

# BeautifulSoup pulls data out of HTML and XML files
from bs4 import BeautifulSoup # pip install beautifulsoup4

# Get HTML
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0',
}
url = 'https://www.marketwatch.com/tools/earningscalendar'
response = requests.get(url, headers=headers) 
# <Response [200]> means that the request has succeeded

# Parsing a document by pass it into the BeautifulSoup constructor
soup = BeautifulSoup(response.content, 'html.parser')

# Inspecting the HTML with Chrome Dev tools we found that 
# earnings tables are in <div class="tabpane">

# Find "div" tag, class "tabpane"
tabpane = soup.find('div', 'tabpane')

# Within the tabpane, our earnings info is in 
# <div id="Oct25page" class "daypage">
# Extract all "div" tags with non-zero id
earning_tables = tabpane.find_all('div', {'id': True})

# Setting up an empty dictionary for earnigns tables
dfs = {}

# Getting current datetime and formatting it
current_datetime = datetime.datetime.now().strftime('%m-%d-%y %H_%M_%S')

# Initialize ExcelWriter to write our dataframes into an .xlsx file
xlsxwriter = pd.ExcelWriter('D:/Code/EP-tool/Earning Calendar ({0}).xlsx'.format(current_datetime), index=False)

# Write each earnings table into a separate sheet
for earning_table in earning_tables:
    # Outside of earnings season the table contains the following text 'Sorry, this date currently does not have any earnings announcements scheduled'
    # We don't want to save those tables
    if not 'Sorry, this date currently does not have any earnings announcements scheduled' in earning_table.text:
        # Extractign earnings date and reformatting for readability
        earning_date = earning_table['id'].replace('page', '')
        earning_date = earning_date[:3] + '_' + earning_date[3:]
        print(earning_date)
        # Saving each earnings table in the dfs dictionary with the earning_date key
        dfs[earning_date] = pd.read_html(str(earning_table.table))[0]
        # Saving each dict entry to a separate excel sheet
        dfs[earning_date].to_excel(xlsxwriter, sheet_name=earning_date, index=False)

# Saving the document
xlsxwriter.save()
print('earning tables Excel file exported')