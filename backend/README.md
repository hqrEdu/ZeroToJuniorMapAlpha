# ZeroToJuniorMapAlpha
# BACKEND CRUD REST API

This repo is a CRUD REST API for our main project: [ZeroToJuniorMapAlpha](https://github.com/hqrEdu/ZeroToJuniorMapAlpha)

## Installation

To tinker with this project (backend side), follow these steps:

1. Clone this repository to your local machine.
2. Install PostgreSQL.
3. Install all dependencies from `/backend/requirements.txt`.
4. Open `/backend/db_creator.py` and provide appropriate details (host, port, user, password) for the connection in the `__init__()` method.
5. Create an instance of the `DatabaseCreator` class from the `/backend/db_creator.py` file and run the `.get_proper_database()` method.
6. Run `/backend/app.py` to start the application.
7. Make HTTP requests (I recommend using the Postman API Platform).

## Documentation

Here's a simple documentation for API with examples how to use it: [ZeroToJuniorMapAlpha API Docs](https://documenter.getpostman.com/view/27582869/2s93m4Y39P)