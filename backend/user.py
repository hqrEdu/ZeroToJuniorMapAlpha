from database import Database
from utility_functions.geolocation import postcode_to_city, get_location_from_city
from utility_functions.query_helper import QueryHelper

class User:
    def __init__(self):
        self.db = Database(database="z2j_map", user="postgres", password="superuser", host="localhost", port=5432)

    def get(self):
        get_users_query = QueryHelper.query_get_users()
        response = self.db.get_all(get_users_query)        
        return response

    def post(self, discord, zip_code, stack):
        city_name = postcode_to_city(zip_code)        
        city_id_query, city_id_values = QueryHelper.query_get_city_id(city_name)
        city_exists = self.db.get_cell(city_id_query, city_id_values)
        if not city_exists:
            lat, lng = get_location_from_city(city_name)
            add_city_query, add_city_values = QueryHelper.query_add_city(city_name, lat, lng)
            self.db.run_query(add_city_query, add_city_values)
        add_user_query, add_user_values = QueryHelper.query_add_user(discord, city_name, stack)
        response = self.db.run_query(add_user_query, add_user_values) 
        return response

    def patch(self, **kwargs):     ### You need to provide which argument you pass, eg (discord = "username", city_name = "Warsaw")
        zip_code = kwargs.get("zip_code")    
        if zip_code:
            city_name = postcode_to_city(zip_code)
            city_id_query, city_id_values = QueryHelper.query_get_city_id(city_name)
            city_exists = self.db.get_cell(city_id_query, city_id_values)
            if not city_exists:
                lat, lng = get_location_from_city(city_name)
                add_city_query, add_city_values = QueryHelper.query_add_city(city_name, lat, lng)
                self.db.run_query(add_city_query, add_city_values)

            city_id = self.db.get_cell(city_id_query, city_id_values)
            del kwargs["zip_code"]
            kwargs["city_id"] = city_id
        update_user_query, update_user_values = QueryHelper.query_update_user(**kwargs)
        response = self.db.run_query(update_user_query, update_user_values)    
        return response

    def delete(self, discord):
        delete_query, delete_values = QueryHelper.query_delete_user(discord)
        response = self.db.run_query(delete_query, delete_values)     
        return response
