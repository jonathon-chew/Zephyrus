# 🌪 Zephyrus (Python)

A simple web app using python and APIs to find the weather at given locations. 100 British locations pre-programmed in but google map URLs work just as well 

## 🚀 Features

- Fetches the weather metadata using the OpenWeather API
- Downloads the json and stores it, if it hasn't had a recent download 
- Serves the result to a HTML page where a user can specify all sorts of paraemters
- Simple and clean HTML based front end 

## 🛠️ Prerequisites

- [Python] Listed in requirements.txt
- [Python] Including script to parse the Google Maps URL
- A NASA API key (get one for free at [api.nasa.gov](https://api.nasa.gov/))

## 📁 Setup

1. Clone this repository:

   ```bash
   git clone https://github.com/jonathon-chew/Zephyrus.git
   cd Zephyrus
   ```

2. Store your OpenWeather API key in the text file located at: ./key.txt

3. Run the script:

    `./app.py`

    OR

    `python3 app.py`

## 📂 Output

The inofrmation from the returned JSON file is parsed and converted into emojis and the relevent information desired.

The script saves basic metadata like latitude, longitude, and URL to the json files in the cache folder.

## 🧠 Notes

This is currently a work in progress with a few inovations planned for the future.

Issues will be tracked in Github issues.

## 📜 License

This project is licensed under the MIT License. See the LICENSE file for details.
