# Weather skill AI

import pyowm
import numpy
import pytz
from collections import Counter
from geopy import Nominatim, location
from datetime import datetime, timedelta

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
        self.uk_tz = pytz.timezone('Europe/London')
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
        sunrise_utc = datetime.fromisoformat(forecast.sunrise_time('iso').replace('Z', '+00:00'))
        sunset_utc = datetime.fromisoformat(forecast.sunset_time('iso').replace('Z', '+00:00'))
        sunrise = sunrise_utc.astimezone(self.uk_tz).strftime('%I:%M %p')
        sunset = sunset_utc.astimezone(self.uk_tz).strftime('%I:%M %p')
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
    
    def tomorows_forcast(self):
        "Returns the forecast for tomorrow"

        current_weather = self.mgr.weather_at_place(self.__location).weather
        sunrise_utc = datetime.fromisoformat(current_weather.sunrise_time('iso').replace('Z', '+00:00'))
        sunset_utc = datetime.fromisoformat(current_weather.sunset_time('iso').replace('Z', '+00:00'))
        sunrise = sunrise_utc.astimezone(self.uk_tz).strftime('%I:%M %p')
        sunset = sunset_utc.astimezone(self.uk_tz).strftime('%I:%M %p')

        forecast = self.mgr.forecast_at_place(self.__location, '3h')
        tomorrow = datetime.utcnow().date() + timedelta(days=1)

        weather_list = []

        for weather in forecast.forecast:
            weather_time = datetime.utcfromtimestamp(weather.reference_time())

            if weather_time.date() == tomorrow and 9 <= weather_time.hour <= 21:
                wind = weather.wind()
                temp = weather.temperature('celsius')
                entry = {
                    'time': weather_time.strftime('%I:%M %p'),
                    'temperature': temp.get('temp'),
                    'temp_min': temp.get('temp_min'),
                    'temp_max': temp.get('temp_max'),
                    'humidity': weather.humidity,
                    'wind_speed': wind.get('speed', 0.0),
                    'wind_direction': self.deg_to_compass(wind.get('deg', 0)),
                    'status': weather.detailed_status
                }
                weather_list.append(entry)
        
        avg_temp = numpy.average([w['temperature'] for w in weather_list])
        avg_humidity = numpy.average([w['humidity'] for w in weather_list])
        avg_wind = numpy.average([w['wind_speed'] for w in weather_list])
        temp_min = min(w['temp_min'] for w in weather_list)
        temp_max = max(w['temp_max'] for w in weather_list)
        status_summary = " ".join(
            [f"{w['status']} at {w['time']}," for w in weather_list]
        ).rstrip(',') + '.'

        wind_dir = Counter([w['wind_direction'] for w in weather_list]).most_common(1)[0][0]

        message = (
            "Here's the weather for tomorrow: " \
            f"Temperatures will range from {round(temp_min)} to {round(temp_max)} degrees, "
            f"averaging around {round(avg_temp)} degrees. "
            f"wind averaging {round(avg_wind, 1)} meters per a second from the {wind_dir.lower()}. "
            f"Sunrise at {sunrise}, sunset at {sunset}."
            f"There will be: {status_summary}"
        )

        return message