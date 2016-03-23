# flask_api_server
simple api server with Flask

# Installation

## General

- Install python-pip,virtualenv in advance.
 - `sudo apt-get install python-pip python-dev libmysqlclient-dev mysql-server`
 - `sudo pip install virtualenv`
- Exec `bash setup.sh`
- Create Mysql Database named 'api_server'.
- Create config.py for your environment.

## Create config.py

```python
# database information
DB_USER = 'username'
DB_PASS = '********'
DB_NAME = 'api_server'
DB_HOST = 'localhost'

# server port number
SERVER_PORT = 8080

```

## For future installation

- When you add a python-module, please run `pip freeze > requirements.txt`


