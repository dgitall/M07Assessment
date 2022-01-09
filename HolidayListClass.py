from dataclasses import dataclass, field
import json
import datetime as dt
from pprintpp import pprint as pp

import HolidayClass as HC
import HolidayGlobals as gbl
import webscrape
          
           
# -------------------------------------------
# The HolidayList class acts as a wrapper and container
# For the list of holidays
# Each method has pseudo-code instructions
# --------------------------------------------
@dataclass
class HolidayList:
    webscraper: webscrape.WebScraper = webscrape.WebScraper()    
    innerHolidays: list[HC.Holiday] = field(default_factory=list)

   
    def addHoliday(self, holidayObj):
        # Make sure holidayObj is an Holiday Object by checking the type
        # Use innerHolidays.append(holidayObj) to add holiday
        # print to the user that you added a holiday        
        result = gbl.RSLT_NONE

        if (isinstance(holidayObj, HC.Holiday)):
            self.innerHolidays.append(holidayObj)
        else:
            print("ERROR: Tried to add a non-Holiday object")
            result = gbl.RSLT_ERROR
                

        return result
    
    # Search for the requested holiday in the list. 
    ## Refactor this to use lambda function in a filter.
    def findHoliday(self, HolidayName, Date):
        # Find Holiday in innerHolidays
        # Return Holiday
        result = gbl.RSLT_NOTFOUND
        foundHoliday = HC.Holiday()
        
        if(isinstance(Date, str)):
            Date = dt.datetime.strptime(Date, "%Y-%M-%d")
            
        index = 0
        if(self.numHolidays() != 0):
            for index, holiday in enumerate(self.innerHolidays):
                if (holiday.name == HolidayName) and (holiday.date == Date):
                    foundHoliday = holiday
                    result = gbl.RSLT_FOUND
                    break
    
        return result, foundHoliday, index  
    
    def removeHoliday(self, HolidayName, Date):
        result = gbl.RSLT_NONE

        # Find Holiday in innerHolidays by searching the name and date combination.
        # remove the Holiday from innerHolidays
        # inform user you deleted the holiday
        if(isinstance(Date, str)):
            Date = dt.datetime.strptime(Date, "%Y-%M-%d")     
    
        
        foundresult, holiday, hlyindex = self.findHoliday(HolidayName,Date)
        if foundresult == gbl.RSLT_FOUND:
            try:
                self.innerHolidays.remove(holiday)
                result = gbl.RSLT_NONE
            except:
                print("ERROR: Can't remove holiday")     
                result = gbl.RSLT_ERROR  
        else:
            result = gbl.RSLT_NOTFOUND
                     
        
        return result
    
    def findDate(self, DateToFind):
        date = dt.datetime(1900,1,1)
        
        if(DateToFind == gbl.EARLIEST_DATE):
            pass
          #  date = reduce(self.)
        elif(DateToFind == gbl.LATEST_DATE):
            pass
        
        return date
    
    ## Read holidays from the save file at the given location
    def read_json(self, filelocation):
        result = gbl.RSLT_NONE
        # Read in things from json file location
        # Use addHoliday function to add holidays to inner list.
        holidaysJSON = {}
        try:
            with open(filelocation) as json_file:
                holidaysJSON = json.load(json_file)
        except:
            print("ERROR: Could not read from save file")
            return gbl.RSLT_ERROR
        
        # Cycle through all of the holidays read from the file
        for holiday in holidaysJSON['holidays']:
            # Check if it's already in the list
            foundresult, hldy, index = self.findHoliday(holiday['name'],holiday['date'])
            # If not found, then create a new holiday object to add to the list
            if foundresult == gbl.RSLT_NOTFOUND:
                # Change date to datetime type so we are consistent internally
                date = dt.datetime.strptime(holiday['date'], "%Y-%M-%d") 
                newholiday = HC.Holiday(holiday['name'],date)
                if(self.addHoliday(newholiday) != gbl.RSLT_NONE):
                    print("ERROR: Can't add holiday from JSON file")
                    return gbl.RSLT_ERROR
            elif foundresult != gbl.RSLT_FOUND:
                print("ERROR: Error in find within read_json")
                return gbl.RSLT_ERROR

        return result

    def makeDict(self):
        dictionary = [holiday.makeDict() for holiday in self.innerHolidays]
        return dictionary
            
    def save_to_json(self, filelocation):
        result = gbl.RSLT_NONE

        # Write out json file to selected file.
        holidaysJSON = json.dumps(self.makeDict())
        holidaysJSON = '{\"holidays\" : ' + holidaysJSON + '}'        
        try:
            with open(filelocation, "w") as json_file:
                json_file.write(holidaysJSON)
        except:
            print("ERROR: Could not read from save file")
            return gbl.RSLT_ERROR
        return result       
    
     
    def scrapeHolidays(self):
        # Scrape Holidays from https://www.timeanddate.com/holidays/us/ 
        # Remember, 2 previous years, current year, and 2  years into the future. You can scrape multiple years by adding year to the timeanddate URL. For example https://www.timeanddate.com/holidays/us/2022
        # Check to see if name and date of holiday is in innerHolidays array
        # Add non-duplicates to innerHolidays
        # Handle any exceptions.    
        result = gbl.RSLT_NONE
        
        currentYear = dt.datetime.now().year
        years = (currentYear-2, currentYear-1, currentYear, currentYear+1, currentYear+2) 
        for year in years:
            scrapeResult, holidays = self.webscraper.scrape(year)
            if(scrapeResult == gbl.RSLT_NONE):
                # Add all of the holidays to the list that aren't already there
                for holiday in holidays:
                    # Check if it's already in the list
                    foundresult, hldy, index = self.findHoliday(holiday.name,holiday.date)
                    # If not found, then create a new holiday object to add to the list
                    if foundresult == gbl.RSLT_NOTFOUND:
                        if(self.addHoliday(holiday) != gbl.RSLT_NONE):
                            print("ERROR: Can't add holiday from JSON file")
                            return gbl.RSLT_ERROR
                    elif foundresult != gbl.RSLT_FOUND:
                        print("ERROR: Error in find within read_json")
                        return gbl.RSLT_ERROR
            else:
                print("ERROR: Error scraping holidays")
                result = gbl.RSLT_ERROR
                break

        return result
    
    
    def numHolidays(self ):
        # Return the total number of holidays in innerHolidays
        if isinstance(self.innerHolidays, list):
            return len(self.innerHolidays)
        else:
            return gbl.RSLT_ERROR
    
    def filter_holidays_by_week(self, year, week_number):
        result = 0
        return result
        # Use a Lambda function to filter by week number and save this as holidays, use the filter on innerHolidays
        # Week number is part of the the Datetime object
        # Cast filter results as list
        # return your holidays

    def displayHolidaysInWeek(self, holidayList):
        result = 0
        return result
        # Use your filter_holidays_by_week to get list of holidays within a week as a parameter
        # Output formated holidays in the week. 
        # * Remember to use the holiday __str__ method.

    def getWeather(self, weekNum):
        result = 0
        return result
        # Convert weekNum to range between two days
        # Use Try / Except to catch problems
        # Query API for weather in that week range
        # Format weather information and return weather string.

    def viewCurrentWeek(self):
        result = 0
        return result
        # Use the Datetime Module to look up current week and year
        # Use your filter_holidays_by_week function to get the list of holidays 
        # for the current week/year
        # Use your displayHolidaysInWeek function to display the holidays in the week
        # Ask user if they want to get the weather
        # If yes, use your getWeather function and display results

