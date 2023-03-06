from geopy.geocoders import Nominatim


geolocator = Nominatim(user_agent="z2j_map")

def postcode_to_city(postcode: str):
    location = geolocator.geocode(postcode, addressdetails=True)
    if location:
        if location.raw["address"].get("city"):
            city = location.raw["address"]["city"]
        elif location.raw["address"].get("town"):
            city = location.raw["address"]["town"]
        elif location.raw["address"].get("village"):
            city = location.raw["address"]["village"]
        return city
    else:
        return False

def get_location_from_city(city):
    location = geolocator.geocode(city)
    return location.latitude, location.longitude

