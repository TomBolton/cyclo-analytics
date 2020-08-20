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
        '--connection-string-file',
        dest='connection_string_file',
        type=str,
        required=True,
        help='The file path of the text file containing the Azure storage connection string.'
    )
    
    return parser.parse_args()


def read_connection_string_from_file(text_file_path: str):
    """
    Read the text file containing the Azure storage account connection string.

    :param text_file_path: Path of the text file.
    :return: Storage account connection string.
    """

    with open(text_file_path, 'r') as file:
        text_from_file = file.read()

    return text_from_file



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
        filenames['file' + str(n)] = {'filename': blob.name}
        print(n, ' ', blob.name)

    json_string = json.dumps(filenames)

    # This sets the variable 'files' in Azure DevOps to be a matrix of values,
    # defined by the json string of file names. The 'files' variable can then
    # be passed onto subsequent jobs.
    print("##vso[task.setVariable variable=files;isOutput=true]{}".format(json_string))


#
# Main
#


if __name__ == "__main__":
    args = parse_inputs()

    connection_string = read_connection_string_from_file(args.connection_string_file)

    list_filenames(args.container_name, connection_string)