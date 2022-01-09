import datetime as dt
import json


import HolidayClass as HC
import HolidayListClass as hlc
import HolidayGlobals as gbl



def main():
    result = 0

    # Large Pseudo Code steps
    # -------------------------------------
    # 1. Initialize HolidayList Object
    # 2. Load JSON file via HolidayList read_json function
    # 3. Scrape additional holidays using your HolidayList scrapeHolidays function.
    # 3. Create while loop for user to keep adding or working with the Calender
    # 4. Display User Menu (Print the menu)
    # 5. Take user input for their action based on Menu and check the user input for errors
    # 6. Run appropriate method from the HolidayList object depending on what the user input is
    # 7. Ask the User if they would like to Continue, if not, end the while loop, ending the program.  If they do wish to continue, keep the program going. 
    
    
    result, HolidayList = ProgramStartup()
    if result != gbl.RSLT_NONE:
        print("ERROR: Program did not start up")
        return result
    
    ApplicationRun = True
    while ApplicationRun:
        
        MenuSelection = MainMenu()
        if MenuSelection == 1:
            AddHoliday(HolidayList)
        elif MenuSelection == 2:
            RemoveHoliday(HolidayList)
        elif MenuSelection == 3:
            SaveHolidayList(HolidayList)
        elif MenuSelection == 5:
            if( ExitApp() == gbl.RSLT_EXIT):
                ApplicationRun = False       
        """ elif MenuSelection == 4:
            SaveFile()
     """
    
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
    
    return result, HolidayList
    
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

def AddHoliday(HolidayList):
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
    elif foundresult != gbl.RSLT_FOUND:
        print("ERROR: Error in find within add holiday")
        return gbl.RSLT_ERROR    
    else:
        print(gbl.StringRscs['AddDuplicateError1'])
        print(gbl.fstr(gbl.StringRscs['AddDuplicateError2'], locals()))
        
    return result 

def RemoveHoliday(HolidayList):
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
        elif removeresult == gbl.RSLT_ERROR:          
            print(gbl.StringRscs['RemoveError'])

        
    return result 

def SaveHolidayList(HolidayList):
    result = gbl.RSLT_NONE
    
    print(gbl.StringRscs['SaveBanner'])
    userinput = input(gbl.StringRscs['SavePrompt'])
    if(userinput in ('y','Y')):
        result = HolidayList.save_to_json(gbl.SaveFilePathJSON)    
        if(result == gbl.RSLT_NONE):
            print(gbl.StringRscs['SaveSuccess'])
        else:
            print(gbl.StringRscs['SaveError'])
            result = gbl.RSLT_ERROR
    else:
        print(gbl.StringRscs['SaveCanceled'])
    
    
    return result

def ExitApp():
    result = gbl.RSLT_NONE
    
    print(gbl.StringRscs['ExitBanner'])
    # If no changes to be lost
    userinput = input(gbl.StringRscs['ExitPrompt'])
    if(userinput in ('y','Y')):
        print(gbl.StringRscs['ExitGoodbye'])
        result = gbl.RSLT_EXIT
    return result
    
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




## webscrap on these calendars. Need to dig into a table of where tc class="vt" is the vertical column 
# and the table class="cht lpad" within each are the columns. Probably can find all cht lpad classes
# and within those, the tr's are the individual holidays.
""" https://www.timeanddate.com/calendar/custom.html?year=2022&country=1&cols=3&hol=1134617&df=1
or
https://www.timeanddate.com/calendar/print.html?year=2022&country=1&cols=3&hol=1134617&df=1&cdt=2
or
https://www.timeanddate.com/calendar/custom.html?year=2022&country=1&cols=3&hol=34689401&df=1 which has one column """