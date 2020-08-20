import os, json, argparse
from azure.storage.blob import BlobServiceClient


def parse_inputs():
    """ 
    This Pythons script expects exactly two arguments: the name of
    the Azure blob container and the corresponding connection string.

    :return: The parser arguments.
    """

    parser = argparse.ArgumentParser(
        description="Connect to an Azure blob container and use the filenames as DevOps variables."
    )

    parser.add_argument(
        '--container-name',
        type=str,
        dest='container_name',
        required=True,
        help="Name of the Azure blob container."
    )

    parser.add_argument(
        '--blob-connection-string',
        dest='connection_string',
        type=str,
        required=True,
        help='The connection string from the Azure storage account.'
    )
    
    return parser.parse_args()


def list_filenames(container_name: str, connection_string: str):
    """
    Connect to the Azure blob container containing the ride files
    and list them. Create a dictionary of the file names, to be
    used as the output.

    :param container_name: Name of the Azure blob container.
    :param connection_string: Azure storage account connection string.
    """
    
    # Connect to the Azure blob container.
    service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = service_client.get_container_client(container=container_name)

    # Create a dictionary of the file names.
    filenames = {}

    for n, blob in enumerate(container_client.list_blobs()):
        filenames['file' + str(n)] = {'filename', blob.name}
        print(n, ' ', blob.name)

    # This sets the variable 'files' in Azure DevOps to be a matrix of values,
    # defined by the json string of file names. The 'files' variable can then
    # be passed onto subsequent jobs.
    print("##vso[task.setVariable variable=files;isOutput=true]{}".format(json.dumps(filenames)))


if __name__ == "__main__":
    args = parse_inputs()
    list_filenames(args.container_name, args.connection_string)