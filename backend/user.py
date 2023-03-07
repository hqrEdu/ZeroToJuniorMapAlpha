from psycopg2.errors import  Error, UniqueViolation
from database import Database
from utility_functions.geolocation import geolocator, postcode_to_city, get_location_from_city


class User:
    db = Database(database="z2j_map", user="postgres", password="superuser", host="localhost")

    def get(self):
        self.db.connect()
        try:
            response = self.db.get_users()
        except:
            response = 500
        finally:
            self.db.disconnect()
        return response

    def post(self, discord, zip_code, stack):
        city_name = postcode_to_city(zip_code)
        if not city_name:
            return 404
        
        self.db.connect()
        try:
            if not self.db.city_exists(city_name):
                lat, lng = get_location_from_city(city_name)
                self.db.add_city(city_name, lat, lng)
            response = self.db.add_user(discord, city_name, stack)
        except UniqueViolation:
            response = 409
        except Error:
            response = 500
        finally:
            self.db.disconnect()
        return response

    def patch(self, **kwargs):     ### You need to provide which argument you pass, eg (discord = "username", city_name = "Warsaw")
        discord = kwargs.get("discord")
        new_discord = kwargs.get("new_discord")
        zip_code = kwargs.get("zip_code")
        stack = kwargs.get("stack")

        self.db.connect()
        try:
            if not self.db.user_exists(discord):
                return 404

            response = {}

            if new_discord:
                name_response = self._update_user_name(discord, new_discord)
                if name_response is None:
                    response["name"] = 200
                    discord = new_discord
                else:
                    response["name"] = name_response

            if zip_code:
                city_response = self._update_user_city(discord, zip_code)
                if city_response is None:
                    response["city"] = 200
                else:
                    response["city"] = city_response

            if stack:
                stack_response = self._update_user_stack(discord, stack)
                if stack_response is None:
                    response["stack"] = 200
                else:
                    response["stack"] = stack_response

        except Error:
            response = 500
        finally:
            self.db.disconnect()

        return response

    def delete(self, discord):
        self.db.connect()
        try:
            if not self.db.user_exists(discord):
                return 404
            response = self.db.delete_user(discord)
        except:
            response = 500
        finally:
            self.db.disconnect()
        return response

    def _update_user_name(self, discord, new_discord):
        if new_discord == discord:
            return 409
        if self.db.user_exists(new_discord):
            return 404
        response = self.db.update_user_name(discord, new_discord)
        return response

    def _update_user_city(self, discord, zip_code):
        city_name = postcode_to_city(zip_code)
        if not city_name:
            return 404
        if not self.db.city_exists(city_name):
            lat, lng = get_location_from_city(city_name)
            self.db.add_city(city_name, lat, lng)
        city_id = self.db.select_city_id(city_name)
        user_current_city_id = self.db.select_user_city_id(discord)  #### check that the new id is not the same as the previous one
        if city_id == user_current_city_id:
            return 409
        response = self.db.update_user_city(discord, city_id)
        return response

    def _update_user_stack(self, discord, stack):
        if stack not in ["be", "fe"]:
            return 404
        user_current_stack = self.db.select_user_stack(discord)   ####check that the new stack is not the same as the previous one
        if user_current_stack == stack:
            return 409
        response = self.db.update_user_stack(discord, stack)
        return response
