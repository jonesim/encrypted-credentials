
**encrypted-credentials** encrypts credentials to allow them to be securely added to git repositories.

It can import encrypted settings into Django defined in a json file. 
Encrypted files are automatically generated.


### Django settings

_example_

**settings.json** 

    {
      "AWS_ACCESS_KEY_ID":"ABCDEFGHIJKLMNOP",
      "AWS_SECRET_ACCESS_KEY":"ABCDEFGHIJKLMNOP"
    }
    

**settings.py**

    from encrypted_credentials.django_credentials import add_encrypted_settings
    
    add_encrypted_settings(globals())

Upon first execution an example key will be displayed

    No SETTINGS_KEY set in Environment for secure settings
        A new project can use: SETTINGS_KEY=FQQcgYWCBPE8l8IbHdcNie0WARbYHeFwCl4hIL3ecF0=
        
**set environment variable**

    export SETTINGS_KEY=FQQcgYWCBPE8l8IbHdcNie0WARbYHeFwCl4hIL3ecF0=

   
1. If the `settings.json` file exists and `settings.json.enc` does not exist then `settings.json.enc` will be created.**(development)**
2. If `settings.json` and `settings.json.enc` exist then they will be compared and if different `settings.json.enc` will be overwritten.**(development)**
3. If `settings.json` does not exist then `settings.json.enc` will be used **(production)**

settings.json.enc can be checked into git as it is encrypted with Fernet AES128 encryption 

 
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
    
    

     