#!/usr/bin/python
# Libraries
import requests
import json
import datetime
import pymongo
import time
import threading
import matplotlib.pyplot as plt
import webbrowser
from matplotlib.dates import DateFormatter

# Database Connections
client = pymongo.MongoClient('127.0.0.1', 27017)
db = client.weather  # weather Database in MongoDB
collection = db.forecast  # forecast collection in the selected database
#print "Active Conncetions: " + str(db.command("serverStatus")["connections"]['current']) #Printing number of connetions for the database

#LOCATIONS TO TRACK
def locations():
    """Getting locations from the configuration file on the fly to add or remove cities to be monitored"""
    data = json.load(open('configuration_file.json'))
    return data

def weather_forecast(city_id, api_key):
    """Requesting the weather data and converting it to a json object for one request"""
    url_to_process = "http://api.openweathermap.org/data/2.5/forecast?id=" + city_id + "&appid=" + api_key
    response = requests.get(url_to_process)
    return response.json()

def kelvin_to_fahrenheit(kelvins):
    """Converting Kelvin to Fahrenheit scale"""
    return ((9/5) * (kelvins - 273)) + 32

def alerts(city_name, country, required_data):
    """Printing alerts for freezing temperature or depending upon weather conditions"""
    temp = required_data['main']['temp']
    condition = (required_data['weather'][0]['main']).lower()
    timestamp = required_data['dt_txt']
    #print timestamp, temp, condition

    if temp < 2:
        print "*********************     TEMPERATURE   ALERT     ***************************"
        print "Freezing temperature of " + str(temp) + " in the " + str(city_name) + ", " + str(country) + " around " + str(timestamp)

    if condition.find('rain') >= 0 or condition.find('snow') >= 0:
        print "*******************     WEATHER   ALERT     ***************************"
        print "Its going to be " + condition + " in " + str(city_name) + ", " + str(country) + " around " + str(timestamp)

def data_process(dataset):
    """Filtering Data for converitng datetime stamp to date format and massaging rest of it for avoiding duplicate entries in the database"""
    processed_dictionary = dataset
    processed_dictionary['dt_txt'] = datetime.datetime.strptime(dataset['dt_txt'], '%Y-%m-%d %H:%M:%S')
    processed_dictionary['main']['temp'] = kelvin_to_fahrenheit(dataset['main']['temp'])
    dt = dataset['dt']
    try:
        del processed_dictionary['dt']
    except Exception as e:
        return False
    return dt, processed_dictionary

def data_store_db(json_object):
    """Storing data in the mongodb database"""
    cnt = json_object['cnt']
    city_name = json_object['city']['name']
    city_id = json_object['city']['id']
    country = json_object['city']['country']

    for i in range(cnt):
        dt, required_data = data_process(json_object['list'][i])
        alerts(city_name, country, required_data)
        #print dt, required_data
        collection.update_one(
			{"dt": dt,
			 'city_id': city_id,
			 'city_name': city_name,
			 'country': country},
			{
				"$set": required_data
			},
			True
		)

    return True

def plot_temperature_data(city_name,dt_data, temperature_data):
    """Plotting 10 days data on the graph using matplot library"""
    plt.plot_date(dt_data, temperature_data)
    plt.ylabel("Temperatures (F)")
    plt.xlabel("Dates (Month - Date)")
    plt.title("Temperature Forecast for " + city_name)
    formatter = DateFormatter('%m-%d')
    plt.gcf().axes[0].xaxis.set_major_formatter(formatter)
    #plt.gcf().autofmt_xdate()	# Auto-format the xlabel for datetime
    plt.show()
    return True

def five_day_forecast():
    """5 days/3 hour forecast function"""
    while True:
        print '5 days/3 hour Forecast Thread'

        data = locations()
        api_key = data['api']
        cities = data['cities']
        refresh_rate = data['refresh_rate']

        for city in cities:
            print "Processing " + str(city['name']) + ", " + str(city['country']) + " to get data and saving to database"
            json_object = weather_forecast(str(city['id']), api_key)
            status = data_store_db(json_object)
            #print status
        time.sleep(refresh_rate)

def sixteen_days_forecast():
    """16 days/daily forecast function"""
    while True:
        print '16 days/daily Forecast Thread'

        # TODO
        # Code for downloading 16 days/hourly data and putting it in the mongoDB every 60 seconds
        # This is similar to 5 days but need a paid subscription API key

        time.sleep(60)

def weather_maps():
    """weather_maps download function"""
    Browser_flag = True
    while True:
        print 'Weather map layers to show temperature layer in a windowed or browser'

        # TODO
        # Code for downloading weather maps layers every 60 seconds
        #It can be implemented using own customized libraries in future
        #Meanwhile, using JavaScript and Browser to show temperature layer on maps

        #Opening browser only once
        if Browser_flag:
            print "Opening web browser and displaying the latest temperature layer on the world map"
            webbrowser.open_new('weather_map.html')
        time.sleep(60)
        Browser_flag = False

def open_and_display_graph():
    """open_and_display_maps download function"""
    while True:
        #If data is not available, it'll try again after 1 minute
        try:
            print 'Getting the 10 forecast data and showing the graph for temperatures'
            data = locations()
            cities = data['cities']
            for city in cities:
                cursor = collection.find({'city_id': city['id']}).sort([("dt_txt", -1)]).limit(80);  # Temperature is the collection name
                dt_data = []
                temperature_data = []
                for document in cursor:
                    dt_data.append(document['dt_txt'])
                    temperature_data.append(document['main']['temp'])
                    #print document['city_name'] + ": " + str(document['main']['temp'])
                plot_temperature_data(document['city_name'], dt_data, temperature_data)

            time.sleep(90)
        except:
            time.sleep(60)

def controller():
    """Main Controrller to Run all the required threads"""

    print "Application is Started"
    #Creating threads for each task to be performed
    five_day_forecast_thread = threading.Thread(target = five_day_forecast)
    sixteen_days_forecast_thread = threading.Thread(target = sixteen_days_forecast)
    weather_maps_thread = threading.Thread(target = weather_maps)
    open_and_display_maps_thread = threading.Thread(target = open_and_display_graph)

    #Starting created threads
    five_day_forecast_thread.start()
    sixteen_days_forecast_thread.start()
    weather_maps_thread.start()
    open_and_display_maps_thread.start()

if __name__ == '__main__':
    try:
        controller()
    except Exception as e:
        print 'Error Running the code due to: ' + str(e)
        print "Kindly ammend those errors displayed above to run the app"
        exit()
    except KeyboardInterrupt:
        exit()