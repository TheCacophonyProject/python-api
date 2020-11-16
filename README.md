# Cacophony Project API Client for Python

Python client for the [Cacophony REST API](https://github.com/TheCacophonyProject/cacophony-api).

## Installation

This API client requires Python 3.6 or later. At present the library is not yet available on PyPI.

To install, create a virtualenv using your preferred method then:

```
git clone https://github.com/TheCacophonyProject/python-api.git
cd python-api
pip install .
```

If you plan on making changes to python-api, you'll want to install the test dependencies as well:

```
pip install -r .[test]
```


## Using the package (User API)

### Client setup

Open an instance of the client and use credentials directly
```python
from cacophonyapi.user import UserAPI
client = UserAPI(baseurl=<SERVER-URL>,
                 username=<USER-NAME>,
                 password=<USER-PASSWORD>)
```

Alternatively, using credentials stored in a configuration file:
```python
from cacophonyapi.user import UserAPI
from cacophonyapi.config import Config

config=Config().load_config(config_file=os.path.join(
    os.getcwd(),'defaultconfig.json'))

cp_client = UserAPI(config.api_url,
                            username=config.admin_username ,
                            password=config.admin_password)
```


## API calls

By default the most recent 100 recordings accessible to the user
account are queried but `UserAPI.query()` does support a number of
filtering options. The API server supports arbitrary queries so feel
free to extend `UserAPI.query()` if required.


## Testing

#TODO: expand testing in both `test_client_user_without_server.py` and `test_client_user_with_server.py`

Testing uses the pythony unittest framework where by both unit and integration testing is done.

`test\test_client_user_without_server.py` is tests without requiring a server `nose2 --verbosity 2  cacophonyapi.test.test_client_user_without_server`

and `test\test_client_user_with_server` is full integration testing against a server. This is also part of the travis test `nose2 --verbosity 2 CacophonyClient.test.test_client_user_with_server`.
This integration testing does require a local server setup see [travis.yml](travis.yml)

For individual test `nose2 --verbosity 2  cacophonyapi.test.test_client_user_with_server.mockedCacophonyServer.test_query`

#TODO: Docs improve PEP257 compliance for cacophonyapi UserApi etc,  don't know why it is not failing `tox -e pep257`
