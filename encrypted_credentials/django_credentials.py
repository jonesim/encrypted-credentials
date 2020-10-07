import os
import json
from .encrypted_file import get_decrypted_file
from django.conf import settings


class MissingCredentials(Exception):
    pass


def add_encrypted_settings(module_globals=None, settings_file=None, key=None):
    if not settings_file:
        settings_file = os.path.join(os.path.dirname(module_globals['__file__']), 'settings.json')
    module_globals.update(json.loads(get_decrypted_file(settings_file, key)))


def get_credentials(credential_name, key=None):
    credential_file = settings.CREDENTIAL_FILES.get(credential_name)
    if not credential_name:
        raise MissingCredentials(f"Cannot find '{credential_name}' in CREDENTIAL_FILES")
    return get_decrypted_file(os.path.join(settings.CREDENTIAL_FOLDER, credential_file), key)
