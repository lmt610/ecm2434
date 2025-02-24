# ecm2434

## Dependencies
Python library dependencies are stored in `requirements.txt`. This project
uses Django 5, so the minimum supported version of Python is `3.10`.

## Installation
1. Clone the repo:
```sh
git clone https://github.com/lmt610/ecm2434.git
cd ecm2434
```

2. Set up the virtual environment:
```sh
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate  # Windows
```

3. Install dependencies:
```sh
pip install -r requirements.txt
```

4. Run migrations (set up the database)
```sh
cd project/
python manage.py migrate
```

5. create an admin (optional)
```sh
python manage.py createsuperuser
```

5. Run the (development) server
```sh
python manage.py runserver
```

## Usage
When the server is running, you can view the website at http://127.0.0.1:8000

You can access the admin panel by going to http://127.0.0.1:8000/admin and logging in with the credentials
you set up earlier

To run all tests:
```sh
python manage.py test
```

To run an app's tests:
```sh
python manage.py test app_name
```

To run a specific test class, use the full import path. E.g.
```sh
python manage.py test project.users.tests.test_views.LoginViewTest
```

Example tests relevant to sprint 1 assessment:
- All login and signup tests - `users`
    - login page - `users.tests.test_views.LoginViewTest`, `users.tests.test_forms.LoginFormTest`
    - sign up    - `users.tests.test_views.RegisterViewTest`, `users.tests.test_forms.UserRegistrationFormTest`




## Populating databases
The databases can be populated with mock data by running commands in your terminal.
To create teams and users, navigate to the project directory and enter:
```sh
python manage.py create_teams
```

To create race entries:
```sh
python manage.py create_races
```
And to delete:
```sh
python manage.py delete_teams
```
or
```sh
python manage.py delete_races
```
