from .weather_extract import WeatherProcessor




""" Weather Alert Parameters for SMS push notification/response """

class SMS_Alerts:
    ALERT_CODES = {
        200: "thunderstorm with light rain",
        201: "thunderstorm with  rain",
        202: "thunderstorm with heavy rain",
        210: "light thunderstorm",
        211: "thunderstorm",
        212: "heavy thunderstorm",
        221: "ragged thunderstorm",
        230: "thunderstorm with light drizzle",
        231: "thunderstorm with drizzle",
        232: "thunderstorm with heavy drizzle",
        502: "heavy intensity rain",
        503: "very heavy rain",
        504: "exteme rain",
        511: "freezing rain",
        521: "shower rain",
        522: "heavy intensity shower rain",
        521: "ragged shower rain",
        602: "heavy snow",
        611: "sleet", 
        612: "light shower sleet",
        613: "shower sleet",
        615: "light rain and snow",
        616: "rain and snow", 
        621: "shower snow", 
        622: "heavy shower snow",
        711: "smoke",
        731: "sand/dust whirls",
        741: "fog",
        762: "volcanic ash", 
        781: "tornado" 

    }
    def weather_alerts(self, weather_json):
        code = weather_json["weather"][0]["id"]
        if code in self.ALERT_CODES:
            return {
                "type": self.ALERT_CODES[code],
                "location": weather_json["name"],
                "country": weather_json["sys"]["country"],
                "instruction": "Take caution"
            }
        return None

       

