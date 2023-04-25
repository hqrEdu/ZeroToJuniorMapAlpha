import os
from database import Database
from utility_functions.geolocation import postcode_to_city, get_location_from_postcode
from utility_functions.query_helper import QueryHelper

class User:
    def __init__(self):
        self.db = Database(
                database=os.environ.get('Z2J_DB_NAME'),
                user=os.environ.get('Z2J_DB_USER'),
                password=os.environ.get('Z2J_DB_PASSWORD'),
                host=os.environ.get('Z2J_DB_HOST'),
                port=os.environ.get('Z2J_DB_PORT')
            )

    def get(self):
        get_users_query = QueryHelper.query_get_users()
        response = self.db.get_all(get_users_query)
        return response

    def post(self, discord, zip_code, stack):
        city_name = postcode_to_city(zip_code)
        city_id_query, city_id_values = QueryHelper.query_get_city_id(city_name)
        city_id = self.db.get_cell(city_id_query, city_id_values)
        if not city_id:
            add_city_query, add_city_values = QueryHelper.query_add_city(city_name)
            self.db.run_query(add_city_query, add_city_values)
            city_id = self.db.get_cell(city_id_query, city_id_values)
        postcode_query, postcode_values = QueryHelper.query_get_postcode(zip_code)
        postcode_id = self.db.get_cell(postcode_query, postcode_values)
        if not postcode_id:
            lat, lng = get_location_from_postcode(zip_code)
            add_postcode_query, add_postcode_values = QueryHelper.query_add_postcode(zip_code, city_id, lat, lng)
            self.db.run_query(add_postcode_query, add_postcode_values)
            postcode_id = self.db.get_cell(postcode_query, postcode_values)
        add_user_query, add_user_values = QueryHelper.query_add_user(discord, city_name, postcode_id, stack)
        response = self.db.run_query(add_user_query, add_user_values)
        return response

    def patch(self, **kwargs):     ### You need to provide which argument you pass, eg (discord = "username", city_name = "Warsaw")
        zip_code = kwargs.get("zip_code")
        if zip_code:
            city_name = postcode_to_city(zip_code)
            city_id_query, city_id_values = QueryHelper.query_get_city_id(city_name)
            city_id = self.db.get_cell(city_id_query, city_id_values)
            if not city_id:
                add_city_query, add_city_values = QueryHelper.query_add_city(city_name)
                self.db.run_query(add_city_query, add_city_values)
                city_id = self.db.get_cell(city_id_query, city_id_values)
            postcode_query, postcode_values = QueryHelper.query_get_postcode(zip_code)
            postcode_id = self.db.get_cell(postcode_query, postcode_values)
            if not postcode_id:
                lat, lng = get_location_from_postcode(zip_code)
                add_postcode_query, add_postcode_values = QueryHelper.query_add_postcode(zip_code, city_id, lat, lng)
                self.db.run_query(add_postcode_query, add_postcode_values)
                postcode_id = self.db.get_cell(postcode_query, postcode_values)
            del kwargs["zip_code"]
            kwargs["city_id"] = city_id
            kwargs["postcode_id"] = postcode_id
        update_user_query, update_user_values = QueryHelper.query_update_user(**kwargs)
        response = self.db.run_query(update_user_query, update_user_values)
        return response

    def delete(self, discord):
        delete_query, delete_values = QueryHelper.query_delete_user(discord)
        response = self.db.run_query(delete_query, delete_values)
        return response

