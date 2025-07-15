# ark_api

My simple unofficial CyberArk API Collection

## Installation

```
pip install git+https://github.com/gonatienza/ark_api
```
or
```
pip install https://github.com/gonatienza/ark_api/archive/refs/tags/latest.tar.gz
```

## Usage

### Example:

```
from ark_api.utils import Secret
from ark_api.authorization import Bearer
from ark_api.token import PlatformToken
from ark_api.safes import Safes
from getpass import getpass


subdomain = input('Subdomain: ')
username = input('Username: ')
password = Secret(
   getpass(f'{username} Password: ')
)
token = PlatformToken(subdomain, username, password)
auth = Bearer(token)
safes = Safes(auth)
```
