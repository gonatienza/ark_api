from ark_api.utils import SecretStr


def mask_secrets_from_dict(d):
    return {
        key: "*****"
        if isinstance(value, SecretStr) else value
        for key, value in d.items()
    }
