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

# Get Platform Token
token = PlatformToken(subdomain, username, password)

# Create Authorization Object
auth = PlatformBearer(token)

# Fetch list of safes
safes = Safes(auth)

# List object
safes.value
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

# Get Conjur JWT ID Token and get Authorization Object
conjur_id_token = ConjurIdToken(app_auth)
conjur_auth = ConjurBearer(conjur_id_token)

# Rotate API Key for workload
identifier = 'data/workloads/myworkload'
rotate_api_key = RotateApiKey(conjur_auth, identifier)
conjur_api_key_auth = ConjurApiKey(Secret(rotate_api_key.api_key))

# Get Workload Token and Authorization Object
conjur_workload_token = ConjurWorkloadToken(conjur_api_key_auth, subdomain, identifier)
conjur_workload_auth = ConjurBearer(conjur_workload_token)

# Fetch single secret
secret_path = 'data/vault/mysafe/secretuser/password'
secret = GetSecret(conjur_workload_auth, secret_path)
secret.secret.get()

# Fetch multiple secrets
secret_paths = [
    'data/vault/mysafe/secretuser/address',
    'data/vault/mysafe/secretuser/username',
    'data/vault/mysafe/secretuser/password'
]
secrets = GetSecrets(conjur_workload_auth, secret_paths)
secrets.secrets.conjur_variable_data_vault_mysafe_secretuser_password.get()

# Fetch list of resources available
secrets_list = ListSecrets(conjur_workload_auth)
for secret in secrets_list.secrets:
    print(secret.__dict__)
```
