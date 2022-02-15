[![PyPI version](https://badge.fury.io/py/encrypted-credentials.svg)](https://badge.fury.io/py/encrypted-credentials)

**encrypted-credentials** encrypts credentials to allow them to be securely added to git repositories.

It can import encrypted settings into Django defined in a python module and or a json file. 
Encrypted files are automatically generated.


### Django settings

_example_


**PRIVATE_settings.py**

File stored in folder with django settings.py file

    private_settings = {
      "AWS_ACCESS_KEY_ID":"ABCDEFGHIJKLMNOP",
      "AWS_SECRET_ACCESS_KEY":"ABCDEFGHIJKLMNOP"
    }

**settings.json** 

File stored in folder with django settings.py file

    {
      "AWS_ACCESS_KEY_ID":"ABCDEFGHIJKLMNOP",
      "AWS_SECRET_ACCESS_KEY":"ABCDEFGHIJKLMNOP"
    }
    

**settings.py**

    from encrypted_credentials.django_credentials import add_encrypted_settings
    
    add_encrypted_settings(globals())


Upon first execution a PRIVATE_KEY.env file will be generated with a random encryption key. DO NOT check this into repository.
if PRIVATE_settings.py does not exist it will generate a template module.

        
**set environment variable**

    export SETTINGS_KEY=FQQcgYWCBPE8l8IbHdcNie0WARbYHeFwCl4hIL3ecF0=

   
1. If the `settings.json` file exists and `settings.json.enc` does not exist then `settings.json.enc` will be created.**(development)**
2. If `settings.json` and `settings.json.enc` exist then they will be compared and if different `settings.json.enc` will be overwritten.**(development)**
3. If `settings.json` does not exist then `settings.json.enc` will be used **(production)**

settings.json.enc and or PRIVATE_settings.enc can be checked into git as it is encrypted with Fernet AES128 encryption 

 
## Credential files

`get_decrypted_file` will automatically encrypt the original file and supply the decrypted data

    from encrypted_credentials.encrypted_file import get_decrypted_file
    
    get_decrypted_file('full_path/orginal.pem')

original.pem.enc can be checked into a repository


## Credential files with Django

By default environment variable SETTINGS_KEY will be used as key

**settings.py**

    CREDENTIAL_FOLDER = os.path.join(BASE_DIR, 'credentials')
    CREDENTIAL_FILES = {
        'gmail': 'service-account-abcd.json',
        'drive': 'service-account-efgh.json',
    }


service-account-abcd.json.enc

usage

    from encrypted_credentials.django_credentials import get_credentials
    
    
    credentials = get_credentials('gmail')
    
    

     
