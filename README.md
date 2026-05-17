# 🌪 Zephyrus (Python)

A simple web app using Python and APIs to find the weather for given locations. It includes a set of pre-programmed British locations, and Google Maps URLs work as well.

## 🚀 Features

- Fetches the weather metadata using the OpenWeather API
- Downloads JSON and stores it if it has not had a recent refresh
- Serves the result to an HTML page where a user can specify parameters
- Simple HTML-based front end

## 🛠️ Prerequisites

- [Python] Listed in `requirements.txt`
- OpenWeather API access
- A local API key stored outside the repository

## 📁 Setup

1. Clone this repository:

   ```bash
   git clone https://github.com/jonathon-chew/Zephyrus.git
   cd Zephyrus
   ```

2. Store your OpenWeather API key in a local, untracked file or environment variable before running the app.

3. Run the script:

    `./app.py`

    OR

    `python3 app.py`

## 📂 Output

The information from the returned JSON file is parsed and converted into emojis, along with the relevant weather details.

The script saves basic metadata like latitude, longitude, and URL to JSON files in the cache folder.

## 🧠 Notes

This is currently a work in progress with a few improvements planned for the future.

Issues will be tracked in GitHub Issues.

## 📜 License

This project is licensed under the MIT License. See the LICENSE file for details.
