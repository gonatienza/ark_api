# ark_api

A simple unofficial Cyberark API Collection

## Installation

```
pip install git+https://github.com/gonatienza/ark_api
```

## Usage

### Example:

```
from ark_api.token import Token
from ark_api.safes import Safes
from ark_api.utils import Secret
from getpass import getpass


subdomain = input('Subdomain: ')
username = input('Username: ')
password = Secret(
   getpass(f'{username} Password: ')
)
token = Token(subdomain, username, password)
safes = Safes(token.access_token, subdomain)
```
