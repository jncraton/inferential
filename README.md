[![tests](https://github.com/jncraton/inferential/actions/workflows/unit-tests.yml/badge.svg)](https://github.com/jncraton/inferential/actions/workflows/unit-tests.yml) [![Code Style black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Inferential

Inferential is a web application that provides a playground and API for running large language models.

## QuickStart

Use the following to clone the git repository, install dependencies, and run the application:

```sh
git clone https://github.com/jncraton/inferential.git
cd inferential
pip install -r requirements.txt
make run
```

Here's a Python example communicating with the API:

```python
>>> import requests
>>> requests.get("http://localhost:5000/api?input=Where is Paris").text
'Paris is located in France.'
```

## Production Deployment

While using the built in server is useful for development, it is not ideal for a production environment. You will need to deploy the application to a server that is safer for production use. One way you can deploy is using the gunicorn package. Gunicorn only works on Unix based machines so if you use this method be sure to use a Unix machine. To start the process, clone the git repository onto your Unix machine.

Clone the repository

```sh
git clone git@github.com:jncraton/inferential.git
```

Then you will need to create a new virtual environment. Navigate to the project folder and enter the following command.

```sh
python3 -m venv venv
```

Then activate the environment

```sh
source venv/bin/activate
```

Once you have activated your environment, you need to install all the requirements if you haven't already installed them.

```sh
pip install -r requirements.txt
pip install gunicorn
```

Then all that is left is to start the server using gunicorn using the following command

```sh
gunicorn -w 4 -b 0.0.0.0:8000 "inferential:create_app()"
```

Once you have run that command you should be able to connect to your server on 0.0.0.0:8000 For further help, refer to the Gunicorn documentation. (https://gunicorn.org/)
