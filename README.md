Inferential [![tests](https://github.com/jncraton/inferential/actions/workflows/unit-tests.yml/badge.svg)](https://github.com/jncraton/inferential/actions/workflows/unit-tests.yml)
[![Code Style black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
===========

Inferential is a web application that houses several large language models to run inference locally

This project helps those at a beginner programming level understand the fundamentals of large language models, tokenization, and API's. This web application follows an encoder-decoder format where a query is sent to the API where it will encode the query into tokens, generate a response in tokens, and then decode those tokens into readable text. For more information on this process ![Attention is All You Need](https://arxiv.org/pdf/1706.03762.pdf)

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

While using the built in "flask run" command is useful for developing,It is not ideal for a production environment.
You will need to deploy the application to a server that isn't locally hosted. This process is started by creating
a wheel (.whl) file. To do this, you need to install the "build" python  package.

Install the build package

```sh
pip install build
```

Run build to create the wheel file

```sh
python -m build --wheel
```

Once you have run those commands, you can find the file in "dist/flaskr-1.0.0-py3-none-any.whl" which follows
the format {project name}-{version}-{python tag} -{abi tag}-{platform tag}. Then 