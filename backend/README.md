# ZeroToJuniorMapAlpha

Web application exclusive for ZeroToJunior.dev community members (a place for developer wannabies), that shows an approximated location of particular users. It's meant to help grasp the popularity of this community, its geographic distribution, and potentially even help gather some members for local, offline events. Strength in numbers!

## Stack

- Frontend: HTML + CSS + JavaScript
- Backend: CRUD REST API (Python + Flask + PostgreSQL)

## Installation

To tinker with this project (backend side), follow these steps:

1. Clone this repository to your local machine.
2. Install PostgreSQL and create an empty database.
3. Install all dependencies from `/backend/requirements.txt`.
4. Open `/backend/db_creator.py` and provide appropriate details (host, port, user, password) for the connection in the `__init__()` method.
5. Create an instance of the `DatabaseCreator` class from the `/backend/db_creator.py` file and run the `.check_database()` method.
6. Run `/backend/app.py` to start the application.
7. Make HTTP requests (I recommend using the Postman API Platform).

## Usage

This project is exclusive for members of the ZeroToJunior.dev community. You can access the currently deployed version at the following address: [http://zero2junior.hqr.at/](http://zero2junior.hqr.at/)

1. Visit the website:  [http://zero2junior.hqr.at/](http://zero2junior.hqr.at/)
2. Scroll down and type in your Discord ID into the "Twój nick z Discord" field.
3. Choose "Frontend" or "Backend" to reflect your stack.
4. Provide your postcode into the "Kod pocztowy..." field.
5. Click on the green "Dołączam!" button at the bottom.
6. To view members from your area, simply move the view on the map and scroll in/out if necessary. Members from that area will be displayed on the right under "Programiści w Twojej okolicy".

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For any inquiries or feedback, you can reach out to the project maintainers.