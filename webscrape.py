from dataclasses import dataclass, field
from pprintpp import pprint as pp
from bs4 import BeautifulSoup as bs
import requests
import datetime as dt

import HolidayClass as HC
import HolidayGlobals as gbl


# Create a utility class for the webscraping to keep it self-containted.
# Include unit tests below to test this before including in the full program
class WebScraper:
    def getHTML(self, url):
        try:
            response = requests.get(url)
            result = response.text
        except:
            result = "ERRORERRORERROR"
            
        return result
    
    def scrape(self, year):
        result = gbl.RSLT_NONE
        
        url = f"https://www.timeanddate.com/calendar/custom.html?year={year}&country=1&cols=3&hol=34689401&df=1"
    
        # Get the HTML from the website
        html = self.getHTML(url)
        # Parse the data
        soup = bs(html,'html.parser')

        # Look for article class = "product_pod" which is the article around each book
        table = soup.find('table',attrs = {'class':'cht lpad'})
        
        holidays = []
        for row in table.find_all('tr'):
            cells = row.find_all('td')
            date = cells[0].string
            try:
                date = dt.datetime.strptime(f"{year} {date}", "%Y %b %d")
            except:
                date = dt.datetime(1900,1,1)
            name = cells[1].a.text
            holiday = HC.Holiday(name, date)  
            holidays.append(holiday)
        
        return result, holidays
    


# If running this file on its own, do the following test code to make sure it works
if __name__ == "__main__":
    result = 0

    webscraper = WebScraper()
    result, holidays = webscraper.scrape(2022)
    
    for holiday in holidays:
        print(holiday)