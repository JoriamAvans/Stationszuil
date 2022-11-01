import requests

START_URL = "https://api.openweathermap.org/data/2.5/weather?"
API_KEY = '547c9d04fe9a79b4d5fa36d08a2a000f'


def getWeather(city):

    call_url = START_URL + "q=" + city + "&appid=" + API_KEY
    response = requests.get(call_url)

    if response.status_code == 200:
        data = response.json()
        main = data['main']

        temp = main['temp']
        temp = round(temp - 273.15, 1)
        humidity = main['humidity']
        pressure = main['pressure']

        report = data['weather']
        report = report[0]['description']
        returnList = [temp, humidity, pressure, report]
        return returnList
    else:
        # showing the error message
        print("Error in the HTTP request")
