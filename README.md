# python-rest

Simple API with Python, Flask and SQLAlchemy.

Requirements:
* python 3.x
* pip3

In order to get the api up, it is necessary to run it in a pip environment. To do so, we must fisrt install Pipenv dependency manager by running

```pip install pipenv```

Next, running ```pipenv shell``` will create a python development environment.
After that, ```pipenv install``` command will install dependencies for the application.
Last, running ```python app.py``` will run the API server.

Application runs on ```localhost:5000```

### Possible HTTP requests
```GET http://localhos:5000/categories``` - returns list of all categories;

```GET http://localhos:5000/categories/{id}/products``` - returns list of products of category with specified id;

```UPDATE```, ```PUT```, ```DELETE``` requests work with ```http://localhos:5000/categories/{id}``` or ```http://localhos:5000/products/{id}```;
