# ark_api

My simple unofficial CyberArk API Collection

## Installation

```
pip install git+https://github.com/gonatienza/ark_api
```

## Usage

### Example:

```
from ark_api.token import Secret, PlatformToken
from ark_api.safes import Safes
from getpass import getpass


subdomain = input('Subdomain: ')
username = input('Username: ')
password = Secret(
   getpass(f'{username} Password: ')
)
token = PlatformToken(subdomain, username, password)
safes = Safes(token.access_token, subdomain)
```
