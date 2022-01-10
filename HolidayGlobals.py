import json

# Global Return result codes
RSLT_NONE = 0
RSLT_STOP = -1
RSLT_ERROR = -2
RSLT_EXIT = -3

RSLT_NOTFOUND = -10
RSLT_FOUND = -11
RSLT = -12
RSLT_ROUNDOVER = -13
RSLT_FINALROUND = -14
RSLT_FINALWON = -15
RSLT_FINALLOST = -15
RSLT_GAMEEND = -16

EARLIEST_DATE = -1
LATEST_DATE = -2
CURRENT_WEEK = -3
NEXT_WEEK = -4
ALL_WEEKS = -5

SaveFilePathJSON = "Data/holidays.json"
SaveFilePathJSONTest = "Data/holidays-test.json"

# Load the string dictionary from the JSON file
StringRscs = {}
with open('Data\stringfile.json') as json_file:
    StringRscs = json.load(json_file)

# Function to evaluate the loaded f-strings. This is necessary because you can't include
# dictionary keys if doing it inline due to interference with single and double quotes.
# Taken from: https://stackoverflow.com/questions/47597831/python-fstring-as-function
def fstr(fstring_text, locals, globals=None):
    # Dynamically evaluate the provided fstring_text. Passing in locals and globals allows us
    # to access variables to insert into the f string.
    locals = locals or {}
    globals = globals or {}
    ret_val = eval(f'f"{fstring_text}"', locals, globals)
    return ret_val
 