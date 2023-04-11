from flask_api.exceptions import APIException


class InternalServerError(APIException):
    detail = "Internal Server Error"
    status_code = 500

class BadRequest(APIException):
    detail = None
    status_code = 400