import re

def getGoogleURL(url):
    # Regex pattern to extract the location name and latitude/longitude
    pattern = r"/place/([^/]+)/@([\d.-]+),([\d.-]+)"
    second_pattern = r"/@([\d.-]+),([\d.-]+)"

    # Search the URL using the pattern
    match = re.search(pattern, url)

    # Extract and structure the data
    if match:
        location = match.group(1).replace('+', ' ')
        latitude = float(match.group(2))
        longitude = float(match.group(3))
        result = [location, {'lat': [latitude], 'long': [longitude]}]
    else:
        second_match = re.search(second_pattern, url)
        if second_match:
            location = "Unknown - there is no location in the google website"
            latitude = float(second_match.group(1))
            longitude = float(second_match.group(2))
            result = [location, {'lat': [latitude], 'long': [longitude]}]
        else:
            result = ["Unable to find a location, longitude or latitude", {'lat': [], 'long': []}]


    return result
