from os.path import basename, join, exists
from os import makedirs
import sys
from urllib.request import urlretrieve
import gzip
from time import sleep


def _file_name(data_id):
    return f"{data_id}.csv.gz"


def _data_url(data_id, project_name):
    return f"https://rebench.dev/{project_name}/data/{_file_name(data_id)}"


def is_valid_gzip(path: str) -> bool:
    try:
        with gzip.open(path, "rb") as f:
            # Read a bit to force decompression and CRC/header checks.
            while f.read(1024 * 1024):
                pass
        return True
    except OSError:
        return False


def download_to_cache(data_id, project_name, cache_dir="cache"):
    makedirs(cache_dir, exist_ok=True)

    file_name = basename(_file_name(data_id))
    if not file_name:
        raise ValueError(f"Could not determine file name from {file_name}")

    target_path = join(cache_dir, file_name)
    url = _data_url(data_id, project_name)
    if exists(target_path) and is_valid_gzip(target_path):
        return target_path

    try:
        print(f"Downloading {url} -> {target_path}")
        urlretrieve(url, target_path)

        retry = 3
        while retry > 0 and not is_valid_gzip(target_path):
            print(
                f"Downloaded file {target_path} is not a valid gzip file. Retrying... in 10 sec."
            )
            urlretrieve(url, target_path)
            retry -= 1
            sleep(10)
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        sys.exit(1)

    return target_path
