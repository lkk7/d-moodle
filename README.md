# d-moodle
A simple moodle-like system for teaching/learning.

## About
- Powered by Django and PostgreSQL
- Simple authentication system
- Teachers can create lessons in courses
- Students can read lessons and ask questions which are answered by teachers
- Mathjax support allowing for math symbols and equations
- 90%+ line and branch test coverage

## Requirements
- PostgreSQL (12.6+) (although other DBs can be used) – core database.
- Django (3.1+) – core web framework.
- psycopg2 (2.8) – PostgreSQL database adapter for Python, used by Django.
- Optionally: coverage (5.5) for checking the test coverage.

A sufficient `requirements.txt` file is provided.

## Running Locally
1. Get the repository.
2. Install the requirements locally or [in a virtual environment](https://docs.python.org/3/tutorial/venv.html).
3. Set appropriate database credentials in `settings.py`. Example `settings.py` file is provided.
4. Create a file `secret_key.py` in `django_moodle` folder and put a long random `SECRET_KEY` in there (preferably 50 characters):
    ```python
    SECRET_KEY = 'b(g7%+6694clqou8yi8f3b_7i0=a(0b=v##3j)*=$3e*v7cc2h'
    # This is just an example, generate your own key...
    ```
5. Create the superuser account (administrator): `python3 manage.py createsuperuser`
6. Run the local development server by `python3 manage.py runserver`.

##### Notes
- Teacher accounts can be added only by the superuser (administrator) in the admin panel (`<website_url>/admin/`). Only students can register through the website. This is for security reasons, but can be changed if inconvenient.
- New `Course` objects are added only by the superuser (administrator). Teachers can only add lessons to existing courses.
- During website registration, student accounts are automatically added to the "Students" group. When creating teacher accounts, the administrator should remember to select the "Teachers" group.

## Things that could be added
- Email confirmation during student registration
- A frontend framework to improve the looks (d-moodle uses simple pure CSS)
- Migration to Docker
- More features (e.g. quizzes, grades)

## A screenshot
![Screenshot](https://raw.githubusercontent.com/lkk7/d-moodle/master/screenshot.png)
