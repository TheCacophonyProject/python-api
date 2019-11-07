# Cacophony SERVER REST api  python_client V1

This client for the Cacophony Project Server provides a python set of classes to interect with the REST api


## Installation

This API client requires Python 3.6 or later.

* Create a virtualenv using your preferred method.
* Install dependencies: `pip install -r requirements.txt`
* python setup.py install

## Configuration

Modify the  defaultconfig.json with correct user credential 

## API calls

By default the most recent 100 recordings accessible to the user
account are queried but `API.query()` does support a number of
filtering options. The API server supports arbitrary queries so feel
free to extend `API.query()` if required.
