from pyknow import *


class Weather(Fact):
    """Stores info about the weather conditions."""
    temperature = Field(int, mandatory=False)
    wind_speed = Field(int, mandatory=False)
    precipitation = Field(str, mandatory=False)
    pass

class Recommendation(Fact):
    """Stores the recommendation based on the weather conditions."""
    advice = Field(str, mandatory=False)
    pass

#Gets the Windspeed from end user. This function prevents invalid values from being entered
def get_windspeed():
    while True:
        wind_speed = input("What is the Wind Speed in your area?\n")
        if wind_speed.isnumeric():
            return int(wind_speed)
        else:
            print("Please input an integer.")
    pass

#Gets the type of precipitation that is expected for the day. This function prevents invalid values from being entered.
def get_precipitation():
    options = {1:"Rain",2:"Snow",3:"No"}
    while True:
        print("\nIs there a chance of Precipitation today?\nPlease Select from the following options.")
        for key in options:
            print(str(key) + ". " + options[key])
        selection = input("\n")
        if selection not in ["1","2","3"]:
            print("Please select option 1, 2, or 3.")
        else:
            return options[int(selection)]
    pass

#Gets Temperature from End user. This function prevents invalid values from being entered.
def get_temp():
    while True:
        temp = input("What is the temperature outside? (In Fahrenheit)\n")
        if temp.isnumeric():
            return int(temp)
        else:
            print("Please input an integer.")
    pass

class WeatherRecommenderDSS(KnowledgeEngine):

    #TEMPERATURE RULES#    

    # P() Function = Predicate Field Contraint - If the Lambda is True, the field contraint will match.
    @Rule(Weather(temperature=P(lambda temp: temp >= 80)) ) #If Temperature is 80 or above
    def hot_temperature(self):
        self.declare(Recommendation(advice="-It is going to be hot. Be sure to stay hydrated, and wear light clothes."))
        pass

    @Rule(Weather(temperature=P(lambda temp: temp > 60) & P(lambda temp: temp < 80))) #If Temperature is above 60 and Less than 80
    def comfortable_temperature(self):
        self.declare(Recommendation(advice="-The weather will be comfortable. Perfect day for a walk. Wear light clothes."))
        pass

    @Rule(Weather(temperature=P(lambda temp: temp <= 60))) #If Temperature is 60 or below
    def chilly_temperature(self):
        self.declare(Recommendation(advice="-It's chilly outside. Be sure to wear a Jacket."))
        pass

    @Rule(Weather(temperature=P(lambda temp: temp > 32)),Weather(temperature=P(lambda temp: temp < 60))) #If Temperature is above 32 and below 60
    def cold_temperature(self):
            self.declare(Recommendation(advice="-It's cold outside. Be sure to wear a heavy jacket."))
            pass

    @Rule(Weather(temperature=P(lambda temp: temp <= 32))) #If Temperature is 32 or below
    def freezing_temperature(self):
            self.declare(Recommendation(advice="-It's freezing outside. Be sure to wear your snow gear."))
            pass
    

    #PRECIPITATION RULES#
    @Rule(Weather(precipitation='Rain')) #If Rain is expected
    def rainy_weather(self):
        self.declare(Recommendation(advice="-Since rain is in the forecast, be sure to bring an umbrella with you today just in case."))
        pass

    @Rule(Weather(precipitation='Snow'),Weather(temperature=P(lambda temp: temp <= 32)),) #If Snow is expected
    def snowy_weather(self):
        self.declare(Recommendation(advice="-The conditions are good for snow to stick to the ground. If you do not have 4-wheel drive, I suggest you do not go driving today."))
        pass

    @Rule(Weather(precipitation='Snow'),Weather(temperature=P(lambda temp: temp > 32))) #If Temperature is greater than 32 and Snow is expected
    def snowy_and_warm(self):
        self.declare(Recommendation(advice="-It is too hot for the snow to stick to the ground. The Roadways should be safe to travel, but be cautious."))
        pass


    #WINDSPEED RULES
    @Rule(Weather(wind_speed=P(lambda ws: ws > 30))) #If Wind Speed is above 30
    def windy_weather(self):
        self.declare(Recommendation(advice="-It is a windy day. It might be a good day to wear a wind-breaker jacket."))
        pass


    #RECOMMENDATION RULES
    @Rule(AS.recommendation << Recommendation()) # If the 'Fact' is a Recommendation
    def recommendation_function(self, recommendation):
        print(recommendation['advice'])
        pass

if __name__ == '__main__':
    intro = "Welcome to the Weather Recommender. I will provide you with some weather tips that you should consider based on the current weather in your area.\nAnswer the following questions, and I will give you some recommendations.\n"
    print(intro)
    engine = WeatherRecommenderDSS()
    engine.reset()

    wind_speed = get_windspeed()
    engine.declare(Weather(wind_speed=wind_speed))

    precipitation = get_precipitation()
    engine.declare(Weather(precipitation=precipitation))

    temp = get_temp()
    engine.declare(Weather(temperature=temp))

    engine.run()
    pass

    