
from dataclasses import dataclass, field
import datetime as dt

@dataclass
class WeatherData:
    date: dt.datetime = dt.datetime(1900,1,1)
    temp: int = 0
    weather: str = ''
    
    def __str__(self):
        return f"{self.weather}, {self.temp}degF"       