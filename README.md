# Web-Monitor-Backend

A backend server for our project web-monitor-dashboard

## Dependencies

- [flask](https://palletsprojects.com/p/flask/): Python server of choise
- [flasgger](https://github.com/flasgger/flasgger): Used to generate the swagger documentation
- [flask-marshmallow](https://flask-marshmallow.readthedocs.io/en/latest/): My favourite serializer
- [apispec](https://apispec.readthedocs.io/en/latest/): Required for the integration between marshmallow and flasgger

## Set Up

1. Check out the code
2. Install pipenv (ignore if installed)
    ```bash
    pip install pipenv # if not installed
    ```
3. Install requirements
    ```bash
    pipenv install
    ```
4. Start the server with:
    ```bash
    pipenv run python -m flask run
    ```
   
5. Visit http://localhost:port/api for the home api, default port is 5000.

6. Visit http://localhost:port/apidocs for the swagger documentation, default port is 5000.

## Tests

The code is covered by tests, to run the tests please execute

```
pipenv run python -m unittest
```