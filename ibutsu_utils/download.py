import json
import os
import sys
from argparse import ArgumentParser
from argparse import Namespace
from pathlib import Path
from typing import Optional
from typing import Tuple
from typing import Union

from ibutsu_client import ApiClient
from ibutsu_client import ApiException
from ibutsu_client import Configuration
from ibutsu_client.api.artifact_api import ArtifactApi

CA_BUNDLE_ENVS = ["REQUESTS_CA_BUNDLE", "IBUTSU_CA_BUNDLE"]


def parse_args() -> Namespace:
    """Parse and return the command line arguments"""
    parser = ArgumentParser(description="A tool to download an artifact from an Ibutsu server")
    parser.add_argument("artifact_id", help="The ID of the artifact to download")
    parser.add_argument(
        "-H",
        "--host",
        required=True,
        help="The Ibutsu instance for uploading, e.g. https://my.ibutsu.com/api",
    )
    parser.add_argument("-t", "--api-token", help="An API token for authentication")
    parser.add_argument(
        "-o",
        "--output",
        help="The destination to save the file. If omitted will "
        "use the current directory and the artifact file name",
    )
    return parser.parse_args()


def get_artifact_api(host: str, token: Optional[str] = None) -> ArtifactApi:
    """Set up an API client that can connect to Ibutsu, then set up and return the Artifact API"""
    config = Configuration(access_token=token)
    config.host = host

    # Only set the SSL CA cert if one of the environment variables is set
    for env_var in CA_BUNDLE_ENVS:
        if os.getenv(env_var, None):
            config.ssl_ca_cert = os.getenv(env_var)

    return ArtifactApi(ApiClient(config))


def get_api_error(api_exception: ApiException) -> str:
    """Analyse the exception and try to get the error message"""
    error = None
    if api_exception.body:
        try:
            data = json.loads(api_exception.body)
            if isinstance(data, dict):
                error = data["detail"]
            else:
                error = data
        except Exception:
            error = api_exception.body
    if not error:
        error = f"Error {api_exception.status}: {api_exception.reason}"
    return error


def download_artifact(
    artifact_api: ArtifactApi, artifact_id: str, destination: Path
) -> Tuple[bool, Union[str, None]]:
    """Download an artifact from Ibutsu"""
    try:
        print("Downloading...")
        api_response = artifact_api.download_artifact(artifact_id)
        if destination.is_dir():
            destination = destination / Path(api_response.name).name
        with destination.open("wb") as dest_file:
            while data := api_response.read(1024):
                dest_file.write(data)
        return True, str(destination)
    except ApiException as api_exception:
        return False, get_api_error(api_exception)
    except FileNotFoundError as fnf_error:
        print(dir(fnf_error))
        return False, str(fnf_error)


def main():
    """Run the script"""
    args = parse_args()
    artifact_api = get_artifact_api(args.host, args.api_token)
    output = Path(args.output) if args.output else Path(".")
    if not output.parent.exists():
        print(f'Error: Path "{output.parent}" does not exist')
        return 1
    is_success, filename_or_error = download_artifact(artifact_api, args.artifact_id, output)
    if is_success:
        print(f"Artifact successfully downloaded to: {filename_or_error}")
    else:
        print(f"Unable to download artifact: {filename_or_error}")
    return 0 if is_success else 1


if __name__ == "__main__":
    sys.exit(main())
