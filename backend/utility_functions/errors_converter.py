from werkzeug.exceptions import HTTPException, BadRequest, InternalServerError
import psycopg2


def convert_to_http_exception(e):
    if isinstance(e, HTTPException):
        return e

    elif isinstance(e, ValueError) and str(e):
        return BadRequest(str(e))
    elif isinstance(e, ValueError):
        return BadRequest('Incorrect value provided')

    elif isinstance(e, KeyError) and str(e):
        return BadRequest(str(e))
    elif isinstance(e, KeyError):
        return BadRequest('Missing required parameter')

    elif isinstance(e, TypeError) and str(e):
        return BadRequest(str(e))
    elif isinstance(e, TypeError):
        return BadRequest('Invalid parameter type')

    elif isinstance(e, psycopg2.errors.UniqueViolation):
        return BadRequest('Entered discord username already exists in the database')
    elif isinstance(e, psycopg2.Error):
        return InternalServerError('Database error')

    else:
        return InternalServerError('Internal Server Error')