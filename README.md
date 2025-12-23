# ark_api

My simple unofficial CyberArk API Collection

## Installation

```bash
pip install git+https://github.com/gonatienza/ark_api
```
or
```bash
pip install https://github.com/gonatienza/ark_api/archive/refs/tags/latest.tar.gz
```

## Usage

### Examples:

Listing safes:

```python
from ark_api.utils import Secret
from ark_api.tokens import PlatformToken
from ark_api.authorizations import PlatformBearer
from ark_api.safes import Safes
from getpass import getpass


subdomain = input('Subdomain: ')
username = input('Username: ')
password = Secret(
   getpass(f'{username} Password: ')
)

# Get Platform Token from oath confidential client
token = PlatformToken(subdomain, username, password)

# Create authorization object
auth = PlatformBearer(token)

# Fetch list of safes
safes = Safes(auth)

# List object
safes.response['value']
```

Same example with interactive authentication and MFA

```python
from ark_api.utils import Secret
from ark_api.authentication import Authentication
from ark_api.authorizations import PlatformBearer
from ark_api.safes import Safes
from getpass import getpass
from time import sleep


subdomain = input('Subdomain: ')
username = input('Username: ')
password = Secret(
   getpass(f'{username} Password: ')
)

# Initiate Authentication
authn = Authentication(subdomain, username)

# List Challenges Available
authn.challenges

# List all Challenges and Mechanisms
for i, _ in enumerate(authn.challenges):
    authn.get_mechanisms(i)

# Add in band answer for first challenge and its first mechanism
authn.add_answer(0, 0, password)

# Add out of band second challenge and its third mechanism
authn.add_oob(1, 2)

# Advance the authentication process
authn.advance()

# Check state of out of band acceptance second challenge and its third mechanism
while not authn.terminated:
    authn.poll(1, 2)
    sleep(1)

# Alternatively, you can submit code in band for that second challenge and its third mechanism
# authn.add_answer(1, 2, Secret("123456"))

# Create authorization object with resulting token
authz = PlatformBearer(authn.token)

# Fetch list of safes
safes = Safes(authz)

# List object
safes.response['value']
```

Working with Conjur Cloud:

```python
from ark_api.utils import Secret
from ark_api.tokens import AppToken, ConjurIdToken, ConjurWorkloadToken
from ark_api.authorizations import AppBearer, ConjurBearer, ConjurApiKey
from ark_api.conjur import RotateApiKey, GetSecret, GetSecrets, ListSecrets
from getpass import getpass


subdomain = input('Subdomain: ')
username = input('Username: ')
password = Secret(
    getpass(f'{username} Password: ')
)

# Get Identity App Token and Authorization Object
scope = 'All'
app_id = 'my_app'
app_token = AppToken(app_id, scope, subdomain, username, password)
app_auth = AppBearer(app_token)

# Get Conjur ID Token and get Authorization Object
conjur_id_token = ConjurIdToken(app_auth)
conjur_auth = ConjurBearer(conjur_id_token)

# Rotate API Key for workload
identifier = 'data/workloads/myworkload'
rotate_api_key = RotateApiKey(conjur_auth, identifier)
conjur_api_key_auth = ConjurApiKey(rotate_api_key.response)

# Get Conjur Workload Token and Authorization Object
conjur_workload_token = ConjurWorkloadToken(conjur_api_key_auth, subdomain, identifier)
conjur_workload_auth = ConjurBearer(conjur_workload_token)

# Fetch single secret
secret_path = 'data/vault/mysafe/account/password'
secret = GetSecret(conjur_workload_auth, secret_path)
secret.response.get()

# Fetch multiple secrets
secret_paths = [
    'data/vault/mysafe/account/address',
    'data/vault/mysafe/account/username',
    'data/vault/mysafe/account/password'
]
secrets = GetSecrets(conjur_workload_auth, secret_paths)
secrets.response["conjur:variable:data/vault/mysafe/account/password"].get()

# Fetch list of resources available
secrets_list = ListSecrets(conjur_workload_auth)
for resource in secrets_list.response:
    resource
```

Working with Conjur Cloud JWT Authenticator:

```python
from ark_api.utils import Secret
from ark_api.tokens import JwtToken, AppToken, ConjurWorkloadToken
from ark_api.authorizations import JwtBearer, AppBearer, ConjurBearer
from ark_api.conjur import RotateApiKey, GetSecret, GetSecrets, ListSecrets
from getpass import getpass


subdomain = input('Subdomain: ')
username = input('Username: ')
password = Secret(
    getpass(f'{username} Password: ')
)
token = Secret(
    getpass(f'Token: ')
)

# Use JWT Authenticator
identifier = 'data/workloads/myworkload'
jwt_token = JwtToken.from_string(token.get())
authenticator = 'conjur_authenticator_name'
jwt_auth = JwtBearer(jwt_token)

# Get Conjur Workload Token and Authorization Object
conjur_workload_token = ConjurWorkloadToken(jwt_auth, subdomain, identifier, authenticator)

# Get Conjur Authorization Object
conjur_workload_auth = ConjurBearer(conjur_workload_token)

# Fetch single secret
secret_path = 'data/vault/mysafe/account/password'
secret = GetSecret(conjur_workload_auth, secret_path)
secret.response.get()

# Fetch multiple secrets
secret_paths = [
    'data/vault/mysafe/account/address',
    'data/vault/mysafe/account/username',
    'data/vault/mysafe/account/password'
]
secrets = GetSecrets(conjur_workload_auth, secret_paths)
secrets.response["conjur:variable:data/vault/mysafe/account/password"].get()

# Fetch list of resources available
secrets_list = ListSecrets(conjur_workload_auth)
for resource in secrets_list.response:
    resource
```
