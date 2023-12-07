Inferential [![tests](https://github.com/jncraton/inferential/actions/workflows/unit-tests.yml/badge.svg)](https://github.com/jncraton/inferential/actions/workflows/unit-tests.yml)
[![Code Style black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
===========

Inferential is a web application that houses several large language models to run inference locally

This project helps those at a beginner programming level understand the fundamentals of large language models, tokenization, and API's. This web application follows an encoder-decoder format where a query is sent to the API where it will encode the query into tokens, generate a response in tokens, and then decode those tokens into readable text. For more information on this process [Attention is All You Need](https://arxiv.org/pdf/1706.03762.pdf)

## QuickStart

Clone the git repository

```sh
git clone git@github.com:jncraton/inferential.git
```

```sh
pip install requirements.txt
```

If pip install does not work here is the alternative

```sh
python -m pip install requirements.txt
```

Run the web application

```sh
flask run
```

If this does not work here is the alternative

```sh
python -m flask run
```

Basic python script to communicate with the API

```python
import requests
print(requests.get("http://127.0.0.1:5000/api?input=Where is Paris").text)
# Returns a json object with the following response
'{"data":"Paris is located in France."}'
```

## Production Deployment

While using the built in "flask run" command is useful for developing, it is not ideal for a production environment.
You will need to deploy the application to a server that is safer for production use. One way you can deploy is using the gunicorn package. Gunicorn only works on Unix based machines so if you use this method be sure to use a
Unix machine. To start the process, clone the git repository onto your Unix machine.

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
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

Once you have run that command you should be able to connect to your server on 0.0.0.0:8000
For further help, refer to the Gunicorn documentation. (https://gunicorn.org/)
