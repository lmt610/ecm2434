# ecm2434

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
python project/manage.py migrate
```

5. create an admin (optional)
```sh
python project/manage.py createsuperuser
```

5. Run the (development) server
```sh
python project/manage.py runserver
```

## Usage
When the server is running, you can view the website at http://127.0.0.1:8000

You can access the admin panel by going to http://127.0.0.1:8000/admin and logging in with the credentials
you set up earlier

To run tests (not set up yet):
```sh
python project/manage.py test
```
