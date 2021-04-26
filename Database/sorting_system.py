"""
pip install geopy
pip install haversine
"""

from geopy.geocoders import Nominatim
from geopy.distance import great_circle



def distance(user_address, vaccine_addresses):
    
    geolocator = Nominatim(user_agent="myGeocoder")
    

    user_location = geolocator.geocode(user_address)
    user_coordinates = (user_location.latitude, user_location.longitude)

    min_dist = -1
    name = None
    full_address = None
    for vaccine_address in vaccine_addresses:
        vaccine_location = geolocator.geocode(vaccine_address.address)
        vaccine_coordinates = (vaccine_location.latitude, vaccine_location.longitude)

        new_dist = great_circle(user_coordinates, vaccine_coordinates).miles
        if new_dist < min_dist or min_dist == -1:
            min_dist = new_dist
            name = vaccine_address.name
            full_address = vaccine_address.full_address


    return f"{name}:{full_address}:{round(min_dist,2)} miles"

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
    else:
        return 0

def job(user_job):
    if user_job.lower()[0] == "y":
        return 50
    else:
        return 0

def health(user_health):
    if user_health.lower()[0] == "y":
        return 9
    else:
        return 0

def priority(num):
    if num >= 50:
        return "First"
    elif num >= 15:
        return "Second"
    elif num >= 14:
        return "Third"
    elif num >= 13:
        return "Fourth"
    elif num >= 5:
        return "Fifth"
    elif num >= 4:
        return "Sixth"
    elif num >= 3:
        return "Seventh"
    elif num >= 2:
        return "Eigth"
    elif num >= 1:
        return "Ninth"
    else:
        return "Tenth"



