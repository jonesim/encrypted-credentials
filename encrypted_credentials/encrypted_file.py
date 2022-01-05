import os
from cryptography.fernet import Fernet


class NoEncryptedData(Exception):
    pass


def get_decrypted_file(original_filename, settings_key=None, encrypted_filename=None, initial_data=None):
    if isinstance(initial_data, str):
        initial_data = initial_data.encode('utf-8')
    if not settings_key:
        settings_key = get_key()
        if not settings_key:
            return
    encryption = Fernet(settings_key)
    if not encrypted_filename:
        encrypted_filename = f'{original_filename}.enc'
    encrypted_data = None
    if os.path.isfile(encrypted_filename):
        with open(encrypted_filename, 'rb') as f:
            encrypted_data = encryption.decrypt(f.read())

    if not initial_data and os.path.isfile(original_filename):
        with open(original_filename, 'rb') as f:
            initial_data = f.read()

    if not initial_data:
        if encrypted_data is None:
            raise NoEncryptedData(f'Cannot find data for {original_filename}')
        return encrypted_data
    elif initial_data != encrypted_data:
        encrypted_data = encryption.encrypt(initial_data)
        with open(encrypted_filename, 'wb') as f:
            f.write(encrypted_data)
    return initial_data


def get_key():
    key = os.environ.get('SETTINGS_KEY', None)
    if not key:
        print(f'No SETTINGS_KEY set in Environment for secure settings\n'
              f'  A new project can use: SETTINGS_KEY={random_key()}')
        return
    return key


def random_key():
    return Fernet.generate_key().decode("utf-8")
