from storages.backends.azure_storage import AzureStorage
import os

class AzureMediaStorage(AzureStorage):
    account_name = os.environ.get('AZURE_ACCOUNT_NAME', None)
    account_key = os.environ.get('AZURE_KEY', None)
    azure_container = 'media'
    expiration_secs = None