from psycopg2.errors import  Error, UniqueViolation
from database import Database
from utility_functions.geolocation import geolocator, postcode_to_city, get_location_from_city


class User:
    dbm = Database(database="z2j_map", user="postgres", password="superuser", host="localhost")

    def get(self):
        try:
            response = self.dbm.get_users()
        except:
            response = 500
        return response

    def post(self, discord, zip_code, stack):
        if stack not in ["be", "fe"]:
            return 404

        city_name = postcode_to_city(zip_code)
        if not city_name:
            return 404

        if not self.dbm.city_exists(city_name):
            lat, lng = get_location_from_city(city_name)
            self.dbm.add_city(city_name, lat, lng)
        try:
            response = self.dbm.add_user(discord, city_name, stack)
        except UniqueViolation:
            response = 409
        except Error:
            response = 500
        return response

    def patch(self, **kwargs):     ### You need to provide which argument you pass, eg (discord = "username", city_name = "Warsaw")
        discord = kwargs.get("discord")
        new_discord = kwargs.get("new_discord")
        zip_code = kwargs.get("zip_code")
        stack = kwargs.get("stack")

        try:
            if not discord or not any((new_discord, zip_code, stack)) or not self.dbm.user_exists(discord):
                return 404

            response = {}

            if new_discord:
                name_response = self._update_user_name(discord, new_discord)
                response["name"] = name_response

            if zip_code:
                city_response = self._update_user_city(discord, zip_code)
                response["city"] = city_response

            if stack:
                stack_response = self._update_user_stack(discord, stack)
                response["stack"] = stack_response
        except:
            response = 500

        return response

    def delete(self, discord):
        try:
            if not self.dbm.user_exists(discord):
                return 404
            response = self.dbm.delete_user(discord)
        except:
            response = 500
        return response

    def _update_user_name(self, discord, new_discord):
        if new_discord == discord:
            return 409
        if self.dbm.user_exists(new_discord):
            return 404
        response = self.dbm.update_user_name(discord, new_discord)
        return response

    def _update_user_city(self, discord, zip_code):
        city_name = postcode_to_city(zip_code)
        if not city_name:
            return 404
        if not self.dbm.city_exists(city_name):
            lat, lng = get_location_from_city(city_name)
            self.dbm.add_city(city_name, lat, lng)
        city_id = self.dbm.select_city_id(city_name)
        user_current_city_id = self.dbm.select_user_city_id(discord)  #### check that the new id is not the same as the previous one
        if city_id == user_current_city_id:
            return 409
        response = self.dbm.update_user_city(discord, city_id)
        return response

    def _update_user_stack(self, discord, stack):
        if stack not in ["be", "fe"]:
            return 404
        user_current_stack = self.dbm.select_user_stack(discord)   ####check that the new stack is not the same as the previous one
        if user_current_stack == stack:
            return 409
        response = self.dbm.update_user_stack(discord, stack)
        return response

