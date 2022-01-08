import datetime
import json


import HolidayClass as hc
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
        """ if MenuSelection == 1:
            NewEntrant()
        elif MenuSelection == 2:
            CancelEntrant()
        elif MenuSelection == 3:
            ViewParticipants()
        elif MenuSelection == 4:
            SaveFile()
        elif MenuSelection == 5:
            ApplicationRun = ExitApp()     """
    
    return result

def ProgramStartup():
    result = gbl.RSLT_NONE
    
    print("\n\n" + gbl.StringRscs['StartBanner'])    
    
    try:
        HolidayList = hlc.HolidayList()
    except:
        HolidayList = None
        return gbl.RSLT_ERROR 
       
    HolidayList.read_json(gbl.SaveFilePathJSON)
        
    length = HolidayList.numHolidays
    print(gbl.fstr(gbl.StringRscs['StartNumberLoaded'], locals()))   
    print("\n")
    userinput = input(gbl.StringRscs['StartWebscrapingPrompt'])
    if(userinput in ('y','Y')):
        HolidayList.scrapeHolidays()     
    
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