import requests

from dash import html


# getting data from the iss-api with lat-long location

def get_iss_location():   
    open_notify_api = "http://api.open-notify.org/iss-now.json"
    iss_location = requests.get(open_notify_api)
    iss_json = iss_location.json()

    latitude = float(iss_json["iss_position"]["latitude"])
    longitude = float(iss_json["iss_position"]["longitude"])

    return [latitude, longitude]



