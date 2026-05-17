#!/usr/bin/env python3
import os, time, json, re, subprocess
from datetime import datetime

from flask import Flask, render_template, request, jsonify
import requests

import regex_google
import locations 

app = Flask(__name__)

DATES_DICT = {
    'Today': 0,
    'Tomorrow': 1,
    '2 days from now': 2,
    '3 days from now': 3,
    '4 days from now': 4,
}

# NUMBER_OF_DAYS = ["1", "2", "3", "4", "5", "6", "7"]
NUMBER_OF_DAYS = [str(i) for i in range(1,8)]

KELVIN_TO_CELCIUS = -273.15

global PLACES
PLACES=[]

@app.route("/")
def homepage():
    userPlaceChoice = request.args.get("Location", "London")

    if userPlaceChoice not in PLACES:
        print(f"\nUser Choice: |{userPlaceChoice}|") # This is to show the choice for debugging!
        PLACES.append(userPlaceChoice)

    Date = request.args.get("Date", "Today")
    Length_Of_Stay = request.args.get("Length_Of_Stay", "1")

    new_places = set(PLACES)
    location_infos = []
    print("Current list of places: ", PLACES) # This is to show the list of places in case their is a hiccup!

    if userPlaceChoice == '':
        userPlaceChoice = "British Museum"
    
    for place in new_places:
        existingPlace = place.title()
        if existingPlace in locations.ITINARY.keys():
            Location_Info = get_info(Place=place.title(), coOrdinates=locations.ITINARY[place], Length_Of_Stay=Length_Of_Stay, Date=Date)
            location_infos.append({"Location": place, "Info": Location_Info})

        elif 'google' in place:
            googlePlace = regex_google.getGoogleURL(place),
            lat = googlePlace[0][1]['lat'][0]
            lon = googlePlace[0][1]['long'][0]
            locations.ITINARY[googlePlace[0][0]] = {'lat': [lat], 'long': [lon]}
            Location_Info = get_info(Place = googlePlace[0][0], coOrdinates= googlePlace[0][1], Length_Of_Stay=Length_Of_Stay, Date=Date)
            location_infos.append({"Location": googlePlace[0][0], "Info": Location_Info})

        else:
            # Check cache does the location exist there
            location_infos.append({"Location": place, "Info": [["Unable to identify location"]]})
            
    # Get a list of all available cities
    Cities = list(locations.ITINARY.keys())

    # Debug printing
    # print(location_infos)

    # Render the template with multiple location information
    return render_template("locations.html",
                           Date=Date,
                           Length_Of_Stay=Length_Of_Stay,
                           DATES=DATES_DICT.keys(),
                           NUMBER_OF_DAYS=NUMBER_OF_DAYS,
                           Location_Infos=location_infos,
                           Cities=Cities)

@app.route('/clear_places', methods=['POST'])
def clear_places():
    global PLACES
    PLACES=['British Museum']
    print("Empty places", PLACES)
    return jsonify({"status": "success", "message": "PLACES array has been cleared"}), 200

def getKey():
    with open('key.txt', 'r') as f:
        key = f.read()
        key = key.strip()
    return key


def get_info(Place, coOrdinates, Length_Of_Stay, Date):
    print("Checking file exsits: ", Place)
    checkFileExists = checkFileExistance(Place, coOrdinates)

    with open(checkFileExists, 'r') as r:
        contents = r.read()

    weatherData = json.loads(contents)
    results = []
    dayGroup = []
    prev_day = datetime.fromtimestamp(weatherData['list'][0]['dt'])
    prev_day = prev_day.strftime('%d-%m-%Y') # yes this can be combined with the above but like this for readability
    count = weatherData['cnt']
    length_of_stay_number = 8
    too_big = False
    if (int(Length_Of_Stay) * 8) < 40:
        length_of_stay_number = int(Length_Of_Stay) * 8
        too_big = False
    else:
        length_of_stay_number = count
        too_big = True 
    x = 0 # just so X can't be unbound although i should always start as 0 as this is the start of the range, and logic is in place to make sure it only runs the first time and then can compound going forward!

    for i in range(0, length_of_stay_number):
        # Work out how many days to go through here
        if i == 0:
            x = 0
            offset_day = datetime.fromtimestamp(weatherData['list'][x]['dt'])
            looking_for_day = offset_day.strftime('%d')
            looking_for_day = DATES_DICT[Date] + int(looking_for_day)
            while looking_for_day != offset_day:
                offset_day = int(datetime.fromtimestamp(weatherData['list'][x]['dt']).strftime('%d'))
                # print(f'Offset day is: {offset_day}, Looking for day is: {looking_for_day}')
                if Date != "Today":
                    x += 1
        dayOffset = i + x
        print(f'Day offset is: {dayOffset} i is: {i} x is {x}')

        if dayOffset < len(weatherData['list']):
        # Getting all the details
            if int(str(datetime.fromtimestamp(weatherData['list'][dayOffset]['dt']).strftime('%H'))) < 5:
                continue
            weatherTime = str(datetime.fromtimestamp(weatherData['list'][dayOffset]['dt']).strftime('%H:%M'))
            day = datetime.fromtimestamp(weatherData['list'][dayOffset]['dt'])
            day = day.strftime('%d-%m-%Y')
            feelsLike = str(int(round(
                weatherData['list'][dayOffset]['main']['feels_like'], 0) + KELVIN_TO_CELCIUS)) + " ᵒC"
            weatherType = weatherData['list'][dayOffset]['weather'][0]['main']
            weatherDetail = weatherData['list'][dayOffset]['weather'][0]['description']
            windSpeed = round((weatherData['list'][dayOffset]['wind']['speed']) * 3.6, 2)

            if weatherType == "Rain":
                rainVolumeLast3Hours = weatherData['list'][dayOffset]['rain']['3h']
            else:
                rainVolumeLast3Hours = 0

            if day == prev_day:
                dayGroup.append({'weatherTime':weatherTime, 'feelsLike':feelsLike, 'weatherType':weatherType, 'weatherDetail':weatherDetail, 'rainVolume':rainVolumeLast3Hours, 'windSpeed': windSpeed})
            else:
                print(dayGroup)
                if dayGroup != []:
                    results.append({'timeDate':prev_day, 'listOfInfo':dayGroup})
                dayGroup = []
                prev_day = day

            print(day, {'weatherTime':weatherTime, 'feelsLike':feelsLike, 'weatherType':weatherType, 'weatherDetail':weatherDetail, 'rainVolume':rainVolumeLast3Hours, 'windSpeed': windSpeed})

    if dayGroup != []:
        results.append({'timeDate':prev_day, 'listOfInfo':dayGroup})

    # capture last day
    if too_big:
        results.append({'timeDate':prev_day, 'listOfInfo':dayGroup})
        results.append({'timeDate':"A future date - I am unable to predict beyond this point", 'listOfInfo':[]})

    return results


def checkFileExistance(Place, coOrdinates):
    checkFileExists = './caches/' + Place + '_cache.json'

    doesExist = os.path.exists(checkFileExists)
    
    if not doesExist:
        getNewLocation(coOrdinates, filePath=checkFileExists)
    else:
        max_age_hours = 3
        current_time = time.time()
        file_mod_time = os.path.getmtime(checkFileExists)
    
        # Calculate the file's age in seconds
        file_age_seconds = current_time - file_mod_time
    
        # Convert max_age_hours to seconds
        max_age_seconds = max_age_hours * 3600
    
        # Check if the file is older than the specified max age
        if file_age_seconds > max_age_seconds:
            os.remove(checkFileExists)
            getNewLocation(coOrdinates, checkFileExists)
    
    return checkFileExists

def getNewLocation(coOrdinates, filePath, key=getKey()):
    lat = coOrdinates['lat'][0]
    lon = coOrdinates['long'][0]
    website = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={key}"
    response = requests.get(website)

    if response.status_code == 200:
        with open(filePath, 'w') as w:
            w.write(response.text)
    else:
        print("Status response as it's not ok!", response)

    time.sleep(1)

pattern = re.compile("\d{3}.\d{3}.\d{1}.\d{3}")
output = subprocess.getoutput(['ifconfig'])

if __name__ == '__main__':
    # Replace '192.168.x.x' with your actual IP address
    app.run(host=re.findall(pattern, output)[0], port=5000, debug=True)
