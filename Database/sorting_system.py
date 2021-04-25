"""
pip install geopy
pip install haversine
"""

import haversine as hs
from geopy.geocoders import Nominatim



def distance(user_address, vaccine_addresses):
    
    geolocator = Nominatim(user_agent="myGeocoder")
    

    user_location = geolocator.geocode(user_address)
    user_coordinates = (user_location.latitude, user_location.longitude)

    min_dist = -1
    name = None
    for vaccine_address in vaccine_addresses:
        vaccine_location = geolocator.geocode(vaccine_address.address)
        vaccine_coordinates = (vaccine_location.latitude, vaccine_location.longitude)

        new_dist = hs.haversine(user_coordinates, vaccine_coordinates)
        if new_dist < min_dist or min_dist == -1:
            min_dist = new_dist
            name = vaccine_address.name


    return f"{name}, {round(min_dist,2)} km"

def age(user_age):
    if user_age >= 75:
        return 15
    elif user_age >= 65:
        return 14
    elif user_age >= 60:
        return 4
    elif user_age >= 50:
        return 3
    elif user_age >= 40:
        return 2
    elif user_age >= 16:
        return 1

def job(user_job):
    if user_job == "FIRST_RESPONDER":
        return 20

def health(user_health):
    if user_health:
        return 9


