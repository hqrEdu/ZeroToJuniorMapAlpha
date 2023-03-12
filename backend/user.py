from database import Database
from utility_functions.geolocation import postcode_to_city, get_location_from_city


class User:
    db = Database(database="z2j_map", user="postgres", password="superuser", host="localhost")

    def get(self):
        self.db.connect()
        response = self.db.get_users()
        return response

    def post(self, discord, zip_code, stack):
        city_name = postcode_to_city(zip_code)
        if not city_name:
            raise ValueError
        
        self.db.connect()
        if not self.db.city_exists(city_name):
            lat, lng = get_location_from_city(city_name)
            self.db.add_city(city_name, lat, lng)
        response = self.db.add_user(discord, city_name, stack)
        self.db.disconnect()
        return response

    def patch(self, **kwargs):     ### You need to provide which argument you pass, eg (discord = "username", city_name = "Warsaw")
        zip_code = kwargs.get("zip_code")
        self.db.connect()
        if zip_code:
            city_name = postcode_to_city(zip_code)
            if not city_name:
                raise ValueError
            if not self.db.city_exists(city_name):
                lat, lng = get_location_from_city(city_name)
                self.db.add_city(city_name, lat, lng)
            city_id = self.db.select_city_id(city_name)
            del kwargs["zip_code"]
            kwargs["city_id"] = city_id
        response = self.db.update_user(kwargs)
        self.db.disconnect()
        return response

    def delete(self, discord):
        self.db.connect()
        response = self.db.delete_user(discord)
        return response
