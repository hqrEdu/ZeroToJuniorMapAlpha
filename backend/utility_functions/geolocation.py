from geopy.geocoders import Nominatim
from utility_functions.api_exceptions import BadRequest

geolocator = Nominatim(user_agent="z2j_map")

def postcode_to_city(postcode: str):
    location = geolocator.geocode(postcode, addressdetails=True)
    if location.raw["address"].get("city"):
        city = location.raw["address"]["city"]
    elif location.raw["address"].get("town"):
        city = location.raw["address"]["town"]
    elif location.raw["address"].get("village"):
        city = location.raw["address"]["village"]
    else:
        raise BadRequest(detail="The postal code does not exist")
    return city


def get_location_from_city(city):
    location = geolocator.geocode(city)
    return location.latitude, location.longitude


