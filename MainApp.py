import datetime as dt

import HolidayClass as HC
import HolidayListClass as hlc
import HolidayGlobals as gbl
import applicationstate as AS



def main():
    result = 0  
    
    result, HolidayList, AppState = ProgramStartup()
    if result != gbl.RSLT_NONE:
        print("ERROR: Program did not start up")
        return result
    
    ApplicationRun = True
    while ApplicationRun:
        
        MenuSelection = MainMenu()
        if MenuSelection == 1:
            result, HolidayList, AppState = AddHoliday(HolidayList, AppState)
        elif MenuSelection == 2:
            result, HolidayList, AppState = RemoveHoliday(HolidayList, AppState)
        elif MenuSelection == 3:
            result, HolidayList, AppState = SaveHolidayList(HolidayList, AppState)
        elif MenuSelection == 4:
            result, HolidayList, AppState = ViewHolidayList(HolidayList, AppState)
        elif MenuSelection == 5:
            if( ExitApp(AppState) == gbl.RSLT_EXIT):
                ApplicationRun = False       

    
    return result

def ProgramStartup():
    result = gbl.RSLT_NONE
    
    print("\n\n" + gbl.StringRscs['StartBanner'])    
    
    try:
        HolidayList = hlc.HolidayList()
    except:
        HolidayList = None
        return gbl.RSLT_ERROR, HolidayList 
       
    HolidayList.read_json(gbl.SaveFilePathJSON)
        
    length = HolidayList.numHolidays()
    print(gbl.fstr(gbl.StringRscs['StartNumberLoaded'], locals()))   
    print("\n")
    userinput = input(gbl.StringRscs['StartWebscrapingPrompt'])
    if(userinput in ('y','Y')):
        scrapingresult = HolidayList.scrapeHolidays()     
        if(scrapingresult == gbl.RSLT_NONE):
            length = HolidayList.numHolidays()
            print(gbl.fstr(gbl.StringRscs['StartWebscrapingComplete'], locals()))
        else:
            print("ERROR: Program Start unable to scrape web for holidays")
            result = gbl.RSLT_ERROR
            
    AppState = AS.ApplicationState()
    
    return result, HolidayList, AppState
    
## Display the main menu and get a selection from the user      
def MainMenu():
    # Display the menu
    print("\n\n" + gbl.StringRscs['MainMenu'])
    # Get User selection
    Selection = 0
    InvalidEntry = True
    while InvalidEntry:
        Selection = input(gbl.StringRscs['MenuPrompt'])
        # Validate selection
        if Selection.isnumeric():
            Selection = int(Selection)
            if Selection > 0 and Selection <= 5:
                InvalidEntry = False

    return Selection

def AddHoliday(HolidayList, AppState):
    result = gbl.RSLT_NONE
    
    # Display the banner
    print("\n\n" + gbl.StringRscs['AddBanner'])
    # Get the Holiday Name and Date from the user
    name = ''
    date = dt.datetime(1900,1,1)
    # Get the name of the holiday from the user
    userinput = 0
    InvalidEntry = True
    while InvalidEntry:
        userinput = input(gbl.StringRscs['AddNamePrompt'])
        # Validate selection
        if (len(userinput) > 0) and (isinstance(userinput, str)):
            name = userinput
            InvalidEntry = False
    # Get the date of the holiday from the user
    userinput = 0
    InvalidEntry = True
    while InvalidEntry:
        userinput = input(gbl.StringRscs['AddDatePrompt'])
        # Validate selection
        if (len(userinput) > 0) and (isinstance(userinput, str)):
            # Check if converting the date in the expected format works
            try:
                date = dt.datetime.strptime(userinput, "%b %d, %Y")
                InvalidEntry = False              
            except:
                print(gbl.StringRscs['AddDateError'])

    holiday = HC.Holiday(name, date)
    # Check if a duplicate
    foundresult, hldy, index = HolidayList.findHoliday(holiday.name,holiday.date)
    # If not found, then create a new holiday object to add to the list
    if foundresult == gbl.RSLT_NOTFOUND:
        if(HolidayList.addHoliday(holiday) != gbl.RSLT_NONE):
            print("ERROR: Can't add holiday from user")
            return gbl.RSLT_ERROR
        else:
            print(gbl.StringRscs['AddSuccess1'])
            print(gbl.fstr(gbl.StringRscs['AddSuccess2'], locals()))
            AppState.HasUnsavedChanges = True
    elif foundresult != gbl.RSLT_FOUND:
        print("ERROR: Error in find within add holiday")
        return gbl.RSLT_ERROR    
    else:
        print(gbl.StringRscs['AddDuplicateError1'])
        print(gbl.fstr(gbl.StringRscs['AddDuplicateError2'], locals()))
        
    return result, HolidayList, AppState 

def RemoveHoliday(HolidayList, AppState):
    result = gbl.RSLT_NONE
    
    # Display the banner
    print("\n\n" + gbl.StringRscs['RemoveBanner'])
    
    # Get the Holiday Name and Date from the user
    name = ''
    date = dt.datetime(1900,1,1)
    userinput = 0
    InvalidEntry = True
    while InvalidEntry:
        userinput = input(gbl.StringRscs['RemoveNamePrompt'])
        # Validate selection
        if (len(userinput) > 0) and (isinstance(userinput, str)):
            name = userinput
            InvalidEntry = False

    removeall = False
    userinput = 0
    InvalidEntry = True
    while InvalidEntry:
        userinput = input(gbl.StringRscs['RemoveDatePrompt'])
        # Validate selection
        if (len(userinput) > 0) and (isinstance(userinput, str)):
            # Check if converting the date in the expected format works
            try:
                date = dt.datetime.strptime(userinput, "%b %d, %Y")
                InvalidEntry = False      
                removeall = False        
            except:
                print(gbl.StringRscs['AddDateError'])
        # If they didn't enter anything then remove all with that name
        elif len(userinput)==0:
            removeall = True
                
    if(removeall):
        numberremoved = 0
        pass
    else:
        # Call the list method to remove the holiday
        removeresult = HolidayList.removeHoliday(name,date)
        # If not found, then create a new holiday object to add to the list
        if removeresult == gbl.RSLT_NOTFOUND:
            print(gbl.StringRscs['RemoveNotFoundError1'])
            print(gbl.fstr(gbl.StringRscs['RemoveNotFoundError2'], locals()))    
        elif removeresult == gbl.RSLT_NONE:
            print(gbl.StringRscs['RemoveSuccess1'])
            print(gbl.fstr(gbl.StringRscs['RemoveSuccess2'], locals()))  
            AppState.HasUnsavedChanges = True           
        elif removeresult == gbl.RSLT_ERROR:          
            print(gbl.StringRscs['RemoveError'])

        
    return result, HolidayList, AppState 

def SaveHolidayList(HolidayList, AppState):
    result = gbl.RSLT_NONE
    
    print(gbl.StringRscs['SaveBanner'])
    userinput = input(gbl.StringRscs['SavePrompt'])
    if(userinput in ('y','Y')):
        result = HolidayList.save_to_json(gbl.SaveFilePathJSON)    
        if(result == gbl.RSLT_NONE):
            print(gbl.StringRscs['SaveSuccess'])
            AppState.HasUnsavedChanges = False
        else:
            print(gbl.StringRscs['SaveError'])
            result = gbl.RSLT_ERROR
    else:
        print(gbl.StringRscs['SaveCanceled'])
    
    return result, HolidayList, AppState

def ExitApp(AppState):
    result = gbl.RSLT_NONE
    
    print(gbl.StringRscs['ExitBanner'])
    # If no changes to be lost
    if AppState.HasUnsavedChanges:
        print(gbl.StringRscs['ExitChangesLost1'])
        print(gbl.StringRscs['ExitChangesLost2'])
        userinput = input(gbl.StringRscs['ExitChangesLost3'])
        if(userinput in ('y','Y')):
            print(gbl.StringRscs['ExitGoodbye'])
            result = gbl.RSLT_EXIT
    else:
        userinput = input(gbl.StringRscs['ExitPrompt'])
        if(userinput in ('y','Y')):
            print(gbl.StringRscs['ExitGoodbye'])
            result = gbl.RSLT_EXIT
            
    return result


def ViewHolidayList(HolidayList, AppState):
    result = gbl.RSLT_NONE
    
    
    print(gbl.StringRscs['ViewBanner'])
    
    year = 0
    week = 0
    # Get the year to display from the user
    userinput = 0
    InvalidEntry = True
    #### Add calling the function to get those from the list
    minYear = 2020
    maxYear = 2024    
    while InvalidEntry:
        userinput = input(gbl.fstr(gbl.StringRscs['ViewYearPrompt'], locals()))
        # Validate selection
        if (len(userinput)>0):
            userinput = int(userinput)
            # Check to see if it is within the range of years in the list
            if (userinput >= minYear) and (userinput <= maxYear):
                year = userinput
                InvalidEntry = False
            else:
                print(gbl.StringRscs['ViewYearError'])
            
    # Get the week to display from the user
    currentYear = False
    userinput = 0
    InvalidEntry = True
    # Get the current year
    thisYear = dt.datetime.now().year
    # Check if the entered year is this year
    if year == thisYear: currentYear=True
    while InvalidEntry:
        if currentYear:
            # Is the current year so allow selecting the current week
            userinput = input(gbl.StringRscs['ViewWeekPrompt1'])
            # Validate selection
            if len(userinput) == 0:
                week = gbl.CURRENT_WEEK 
                InvalidEntry = False
            elif userinput == 'n':
                week = gbl.NEXT_WEEK
                InvalidEntry = False
            elif userinput == 'a':
                week = gbl.ALL_WEEKS
                InvalidEntry = False
            elif userinput.isdigit():
                # Check if in the range of weeks
                userinput = int(userinput)
                if (userinput >= 1) and (userinput <= 52):
                    week = userinput
                    InvalidEntry = False
                else:
                    print(gbl.StringRscs['ViewWeekError'])
            
        else:
            # Not the current year so don't allow selecting the current week
            userinput = input(gbl.StringRscs['ViewWeekPrompt2'])
            # Validate selection
            if (len(userinput) > 0):
                # Check if in the range of weeks
                userinput = int(userinput)
                if (userinput >= 1) and (userinput <= 52):
                    week = userinput
                    InvalidEntry = False
                else:
                    print(gbl.StringRscs['ViewWeekError'])
    
    result, HolidayList, AppState = printTheHolidays(HolidayList, AppState, year, week)  
 
    return result, HolidayList, AppState

def printTheHolidays(HolidayList, AppState, year, week):
        # If week == CURRENT_WEEK that means we want to display the current week   
    if (week > 0):
        # get a list of holidays in the desired week and display them     
        result, displayHolidays = HolidayList.filter_holidays_by_week(year, week)
        if(result == gbl.RSLT_NONE):
            print("\n")
            print(gbl.fstr(gbl.StringRscs['ViewPrintBanner1'], locals()))
            result = HolidayList.displayHolidaysInWeek(displayHolidays, None)
        else:
            print(gbl.StringRscs['ViewPrintError'])    
    else:           
        # Ask if we should show the weather
        userinput = 0
        ShowWeather = False
        userinput = input(gbl.StringRscs['ViewWeatherPrompt'])
        if(userinput in ('y','Y')): ShowWeather = True        
            
        if(week == gbl.CURRENT_WEEK):
            print(gbl.StringRscs['ViewPrintBanner2'])
            result = HolidayList.viewCurrentWeek(ShowWeather)
            if(result != gbl.RSLT_NONE): print(gbl.StringRscs['ViewPrintError'])
        elif(week == gbl.NEXT_WEEK):
            print(gbl.StringRscs['ViewPrintBanner3'])
            result = HolidayList.viewNextWeek(ShowWeather)
            if(result != gbl.RSLT_NONE): print(gbl.StringRscs['ViewPrintError'])
        elif(week == gbl.ALL_WEEKS):
            print(gbl.StringRscs['ViewPrintBanner4'])
            result = HolidayList.viewAllWeeks(year, ShowWeather)
            if(result != gbl.RSLT_NONE): print(gbl.StringRscs['ViewPrintError'])  
        else:
            result = gbl.RSLT_NONE
            print(gbl.StringRscs['ViewPrintError'])  

            
    return result, HolidayList, AppState
    
if __name__ == "__main__":
    main();


# Additional Hints:
# ---------------------------------------------
# You may need additional helper functions both in and out of the classes, add functions as you need to.
#
# No one function should be more then 50 lines of code, if you need more then 50 lines of code
# excluding comments, break the function into multiple functions.
#
# You can store your raw menu text, and other blocks of texts as raw text files 
# and use placeholder values with the format option.
# Example:
# In the file test.txt is "My name is {fname}, I'm {age}"
# Then you later can read the file into a string "filetxt"
# and substitute the placeholders 
# for example: filetxt.format(fname = "John", age = 36)
# This will make your code far more readable, by seperating text from code.

