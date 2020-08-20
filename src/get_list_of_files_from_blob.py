import os, json
from azure.storage.blob import BlobServiceClient

CONTAINER_NAME = 'tb-ride-files'

connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
service_client = BlobServiceClient.from_connection_string(connect_str)
container_client = service_client.get_container_client(container=CONTAINER_NAME)

filenames = {}

for n, blob in enumerate(container_client.list_blobs()):
    filenames[f'file{n}'] = {'filename', blob.name}

print(f"##vso[task.setVariable variable=files;isOutput=true]{json.dumps(filenames)}")