from dataclasses import dataclass, field
import datetime as dt

# -------------------------------------------
# Modify the holiday class to 
# 1. Only accept Datetime objects for date.
# 2. You may need to add additional functions
# 3. You may drop the init if you are using @dataclasses
# --------------------------------------------
@dataclass
class Holiday:
    name: str = ''
    date: dt.datetime = dt.datetime(1900, 1, 1)       
    
    def __str__ (self):
        # String output
        # Holiday output when printed.
        return f"{self.name} ({self.date.strftime('%b %d, %Y')})"
    
    def makeDict(self):
        output = {'name': self.name, 'date': self.date.strftime('%Y-%m-%d')}
        return output 
        