Smart Python based multi-threaded application that can download the weather forecast from the open weather map and store the
data in the document form in the NoSQL database(MongoDB). It will print the alerts for freezing temperature, display graph of forecast for each city and shows weather temperature map layer on the browser

Steps to run the application
1- First, make sure to install all the required libraries to run the python code. Required libraries are:
    1-requests
    2-json
    3-datetime
    4-pymongo
    5-time
    6-threading
    7-matplotlib
    8-webbrowser

    To make sure, all libraries are installed, kindly run the following command in terminal:
        "pip install requests json datetime pymongo time threading matplotlib webbrowser"
    If pip is not installed, follow here to install pip on your system
        https://pip.pypa.io/en/stable/installing/
2- Start mongodb server on your device locally or remotely and change credentials accordingly in the code. If need help installing mongodb, follow instruction here according to your OS:
    https://docs.mongodb.com/manual/administration/install-community/
3- Create Database named 'weather' or your own database name but don't forget to rename it in the code
4- Create Collection named 'forecast' in the weather database.
5- Put your API keys at two places
    5a- In Configuration file (configuration_file.json)
    5b- In the weather_map.html file in scripts around line number 110
    If need API keys, you can get it from here: https://home.openweathermap.org/api_keys
6- Run the code and see the results.

References:
https://openweathermap.org/api
https://docs.mongodb.com/
https://developers.arcgis.com/
https://matplotlib.org/
