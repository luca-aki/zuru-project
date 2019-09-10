from storages.backends.azure_storage import AzureStorage

class AzureMediaStorage(AzureStorage):
    account_name = 'zurustorage' # Must be replaced by your <storage_account_name>
    account_key = "sOky/2tPga2cFjGSoMKZ7BF8gZL8roAn3dzSyDksJRXOkH30hzZDC8iDrbCu4sp7zsk1l26p1nP2lekS941GlQ==" # Must be replaced by your <storage_account_key>
    azure_container = 'media'
    expiration_secs = None