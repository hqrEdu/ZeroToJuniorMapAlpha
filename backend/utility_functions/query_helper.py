class QueryHelper:

    def query_get_users():
        query = """SELECT u.discord, c.city_name, u.stack, p.lat, p.lng
                    FROM user_data u 
                    JOIN cities c ON u.city_id = c.city_id
                    JOIN postcodes p ON u.postcode_id = p.postcode_id;
                    """
        return query
    
    def query_get_city_id(city_name):
        query = "SELECT city_id FROM cities WHERE city_name = %(city_name)s;"
        values = {"city_name": city_name}
        return query, values
    
    def query_add_user(discord, city_name, postcode_id, stack):
        query = """INSERT INTO user_data (discord, city_id, postcode_id, stack) VALUES
                   (%(discord)s, (SELECT city_id FROM cities WHERE city_name = %(city_name)s), %(postcode_id)s, %(stack)s);"""
        values = {"discord": discord, "city_name": city_name, "postcode_id": postcode_id, "stack": stack}
        return query, values
    
    def query_update_user(**kwargs):
        discord = kwargs.get("discord")
        new_discord = kwargs.get("new_discord")
        city_id = kwargs.get("city_id")
        stack = kwargs.get("stack")
        
        query = "UPDATE user_data SET "
        where_condition = ""

        if new_discord:
            query += f"discord = '{new_discord}', "
            where_condition += f" AND discord != '{new_discord}'"
        if city_id:
            query += f"city_id = {city_id}, "
            where_condition += f" AND city_id != {city_id}"
        if stack:
            query += f"stack = '{stack}', "
            where_condition += f" AND stack != '{stack}'"

        query = query[:-2] + " WHERE discord = %(discord)s" + where_condition
        values = {"discord": discord}
        return query, values
    
    def query_delete_user(discord):
        query = "DELETE FROM user_data WHERE discord = %(discord)s;"
        values = {"discord": discord}
        return query, values
    
    def query_add_city(city_name):
        query = "INSERT INTO cities (city_name) VALUES (%(city_name)s);"
        values = {"city_name": city_name}
        return query, values

    def query_get_postcode(zip_code):
        query = "SELECT postcode_id FROM postcodes WHERE postcode = %(postcode)s;"
        values = {"postcode": zip_code}
        return query, values
    
    def query_add_postcode(zip_code, city_id, lat, lng):
        query = "INSERT INTO postcodes (postcode, city_id, lat, lng) VALUES (%(postcode)s, %(city_id)s, %(lat)s, %(lng)s);"
        values = {"postcode": zip_code, "city_id": city_id, "lat": lat, "lng": lng}
        return query, values