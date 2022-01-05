import json
import os
from importlib import import_module

from cryptography.fernet import InvalidToken
from django.conf import settings

from .encrypted_file import get_decrypted_file, random_key

env_key_name = 'SETTINGS_KEY'
python_settings = 'PRIVATE_settings'
json_settings_file = 'settings.json'
env_key_file_name = 'PRIVATE_KEY.env'

default_module_file = '''
# DO NOT CHECK INTO REPOSITORY
# Check in file {}.enc instead
# put private settings in key value pairs in private_settings 

private_settings = {{}} 
'''


class MissingCredentials(Exception):
    pass


class EncryptedSettingsError(Exception):
    pass


def create_key(key_file):
    f = open(key_file, 'w')
    f.write('# This file can be deleted if {} is set in the environment\n\n'.format(env_key_name))
    f.write(f'{env_key_name}={random_key()}\n')
    f.close()


def get_or_create_key_file(path):
    key_file = os.path.join(path, env_key_file_name)
    if not os.path.isfile(key_file):
        create_key(key_file)
    f = open(key_file, 'r')
    for line in f.readlines():
        if line[:line.find('=')] == env_key_name:
            return line[line.find('=') + 1:]


def module_json(module):
    try:
        urlconf_module = import_module(module)
    except ModuleNotFoundError:
        return None, None
    private_settings = getattr(urlconf_module, 'private_settings', {})
    return json.dumps(private_settings), urlconf_module.__file__[:-3]


def add_encrypted_settings(module_globals, settings_file=None, settings_module=None, key=None):

    settings_path = os.path.dirname(module_globals['__file__'])
    if settings_file is None and settings_module is None:
        settings_file = os.path.join(settings_path, json_settings_file)
        settings_module = module_globals['__package__'] + '.' + python_settings

    if env_key_name not in os.environ:
        os.environ[env_key_name] = get_or_create_key_file(settings_path)

    if settings_module:
        json_settings, module_file = module_json(settings_module)
        if json_settings:
            try:
                module_globals.update(json.loads(get_decrypted_file(module_file, key, initial_data=json_settings)))
            except InvalidToken:
                raise EncryptedSettingsError(f'Unable to decrypt {settings_module}. Maybe due to incorrect key')
            except json.JSONDecodeError:
                raise EncryptedSettingsError(f'Unable to decode JSON from {settings_module}')
            return
    if settings_file:
        if os.path.isfile(settings_file):
            try:
                module_globals.update(json.loads(get_decrypted_file(settings_file, key)))
            except InvalidToken:
                raise EncryptedSettingsError(f'Unable to decrypt {settings_file}. Maybe due to incorrect key')
            except json.JSONDecodeError:
                raise EncryptedSettingsError(f'Unable to decode JSON from {settings_file}')
            return
    if settings_module == module_globals['__package__'] + '.' + python_settings:
        module_file = os.path.join(settings_path, python_settings + '.py')
        if not os.path.isfile(module_file):
            m = open(module_file, 'w')
            m.write(default_module_file.format(python_settings))
            m.close()


def get_credentials(credential_name, key=None):
    credential_file = settings.CREDENTIAL_FILES.get(credential_name)
    if not credential_name:
        raise MissingCredentials(f"Cannot find '{credential_name}' in CREDENTIAL_FILES")
    return get_decrypted_file(os.path.join(settings.CREDENTIAL_FOLDER, credential_file), key)
