# The-Farm

## Table of Contents
- [About](#about)
- [Getting started](#getting-started)
- [Technology Stack](#technology-stack)
    - [Python3](#python)
    - [Javascript](#javascript)
    - [Django Web Framework](#django)
- [Other Technologies](#other-technologies-used)
    - [Flutterwave](#flutterwave)
    - [Heroku](#heroku)
    
  

## About
- This is a farm management system that allows users to view and purchase farm products built in Python and the Django web framework. It uses javascript to handle interactivity and to enhance the user experience. The application has an admin panel that allows for management of stock, orders and employees of the target organisation using the application.

## Getting started

- Setup a virtual environment
 ```bash
 python -m venv .venv
 ```
 
 - Activate Virtual environment
 ```
 source .venv/bin/activate
 ```
 
- Install project dependencies.

```bash
    pip install -r requirements.txt
```

## Technology Stack

- [Python3](https://www.python.org/) - is a high-level, interpreted, general-purpose programming language..
- [Django Web Framework](https://www.djangoproject.com/) - is a free and open-source, Python-based web framework that follows the model–template–views (MTV) architectural pattern
- [Javascript](https://developer.mozilla.org/en-US/docs/Web/javascript) - is a lightweight, interpreted, or just-in-time compiled programming language with first-class functions. 


### Other Technologies used

- [Flutterwave](https://developer.flutterwave.com/docs/) -  Provides a payment infrastructure for global merchants and payment. It is used to handle payments within the application.
- [Heroku](https://www.heroku.com) - The cloud platform as a service used for deploying the application


## Setup Database
```bash
python manage.py makemigrations
```

```bash
python manage.py migrate
```

## Running the application
```bash
python manage.py runserver
```

- The app should run by default on [localhost:8000](http://localhost:8000)


***Happy Coding***



