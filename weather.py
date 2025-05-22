# Weather skill AI

import pyowm
from geopy import Nominatim, location
from datetime import datetime

class Weather():

    # The location of where you want the forecast for

    __location = "Bournemouth, GB"

    # API Key
    api_key = "b8b2780d7a38e59248a172cc4a6847df"

    def __init__(self):
        self.ow = pyowm.OWM(self.api_key)
        self.mgr = self.ow.weather_manager()
        locator = Nominatim(user_agent="myGeocoder")
        city = "Bournemouth"
        country = "GB"
        self.__location = city + "," + country
        loc = locator.geocode(self.__location)
        self.lat = loc.latitude
        self.long = loc.longitude

    @property
    def weather(self):
        forecast = self.mgr.weather_at_place(self.__location)
        return forecast.weather
    
    def deg_to_compass(self, deg):
        directions = [
            "North", "North-Northeast", "Northeast", "East-Northeast",
            "East", "East-Southeast", "Southeast", "South-Southeast",
            "South", "South-Southwest", "Southwest", "West-Southwest",
            "West", "West-Northwest", "Northwest", "North-Northwest"
        ]
        idx = int((deg + 11.25) % 360 / 22.5)
        return directions[idx]
    
    def forecast(self):
        "Returns the forecast today at this location"
        
        forecast = self.mgr.weather_at_place(self.__location).weather
        detailed_status = forecast.detailed_status
        wind_speed = forecast.wind()['speed']
        wind_direction = self.deg_to_compass(forecast.wind()['deg'])
        temp = forecast.temperature('celsius')['temp']
        min_temp = forecast.temperature('celsius')['temp_min']
        max_temp = forecast.temperature('celsius')['temp_max']
        humidity = forecast.humidity
        sunrise = datetime.strptime(forecast.sunrise_time('iso')[:19], "%Y-%m-%d %H:%M:%S").strftime("%I:%M %p")
        sunset = datetime.strptime(forecast.sunset_time('iso')[:19], "%Y-%m-%d %H:%M:%S").strftime("%I:%M %p")

        #print(detailed_status)
        #print(wind_speed)
        #print(wind_direction)
        #print(temp)
        #print(max_temp)
        #print(min_temp)
        #print(humidity)
        #print(sunrise)
        #print(sunset)
        
        message = "Here is the weather: Today will be mostly " + detailed_status \
            + ", temperature of " + str(round(temp)) + 'degrees'\
            + " with a wind speed of " + str(wind_speed) + " meters per a second from the " + wind_direction\
            + ", sunrise is at " + str(sunrise)\
            + ", sunset is at " + str(sunset)
        
        return message
        



#Demo
myWeather = Weather()
weather = myWeather.weather
myWeather.forecast()