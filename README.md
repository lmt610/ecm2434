# ExePlore
![{C41BB442-C6B2-40F0-9812-39882C24F71B}](https://github.com/user-attachments/assets/f28dc08f-3b81-4d7c-b061-0d6505f0e311)
ExePlore is a web application that allows users to run races between real locations! Encouraging exploration of the outdoors, ExePlore aims to get people out and about engaging with nature!

![GitHub last commit](https://img.shields.io/github/last-commit/lmt610/ecm2434)         ![GitHub top language](https://img.shields.io/github/languages/top/lmt610/ecm2434)         ![GitHub repo size](https://img.shields.io/github/repo-size/lmt610/ecm2434)
## Contents 
- [Authors](#Authors)
- [Features](#Features)
- [Project Structure](#Project-structure)
- [Depployed App Demo](#Live-Deployment-Demo-Link )
- [Running the App Locally](#Running-the-app-locally )
  - [Dependencies](#Dependencies)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Populating-database](#Populating-databases)


## Authors 
the developers of this project are:
- Alex Norris
- Dan Loveless
- Aria Noroozi
- Barnaby wreford
- Laila Tayeb
- Oliver Greet
- Nathan Gillings

## Features
- User profiles
- Geographically defined races
- Leaderboards for users to compete for top times!
- An exploration mode to soak in the surrounding nature
- Achievements to reward users for getting outside
## Project-structure
The project takes advantage of the modular nature of Django apps. Sections of the web app with compartmental functionality are placed into their own apps. The list of apps includes:
- users
- race
- leaderboard
- tasks
- achievements
  
Within each app:
- Django Python files sit at root
- Static folder is used for CSS, JS, images etc...
- Templates folder is used for HTML files

## Live-Deployment-Demo-Link
The project demo can be found here: 
  https://ecm2434-fy7q.onrender.com/


# Running-The-App-Locally 

## Dependencies
Python library dependencies are stored in `requirements.txt`. This project
uses Django 5, the minimum supported version of Python is `3.10`.
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
5. Create an admin (optional)
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
To run all tests with test labels:
```sh
python manage.py test -v 2
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
    - race page  - `race.tests.RaceMenuPageTests`, `race.tests.CalculateDistanceViewTest`, `race.tests.UpdateRaceTimeViewTest`
## Process
A kanban board was used during production to organise and manage tasks. 

Link to Kanban Board: https://trello.com/b/ak80OHzE/exeplore-group-software-eng-project-natywinat
  
  
  Github was used to host our code. 

Link to Github: https://github.com/lmt610/ecm2434

## Populating-databases
The databases can be populated with mock data by running commands in your terminal.
To create teams and users, navigate to the project directory and enter:
```sh
python manage.py create_teams
```
To create race entries:
```sh
python manage.py create_race_entries
```
And to delete:
```sh
python manage.py delete_teams
```
or
```sh
python manage.py delete_races
```


