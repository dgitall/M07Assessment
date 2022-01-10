
from dataclasses import dataclass, field
import datetime as dt

import HolidayListClass as HLC

@dataclass
class WeatherData:
    date: dt.datetime = dt.datetime(1900,1,1)
    temp: int = 0
    weather: str = ''
    
    def __str__(self):
        return f"{self.weather}, {self.temp}degF"      
    
    
if __name__ == "__main__":
    holidaylist = HLC.HolidayList()
    
    result, weatherList = holidaylist.getWeather()
    
    # Find the forecase for three days from now using lambdas
    date = (dt.datetime.now() + dt.timedelta(days=3))
    day = date.date()
    
    forecast = filter(lambda weather: weather.date.date() == day, weatherList)
    forecast = list(forecast)
    for weather in forecast:
        print(weather)