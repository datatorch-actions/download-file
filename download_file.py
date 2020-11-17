""""
Downloads a file given the DataTorch ID.

Since we may not know the name of the file, a temp file is created using the
file id. If this temp file exists and the overwrite option is false, the file
will not be redownloaded. Instead the file path from inside the file will be
returned.
"""

import datatorch, os

from datatorch import ApiClient
from datatorch.utils.files import mkdir_exists


inputs = datatorch.get_inputs()
file_id = inputs.get("fileId", "")
directory = inputs.get("directory", "")
name = inputs.get("name", "")
overwrite = inputs.get("overwrite", False)

id_file = os.path.join(directory, f"{file_id}.txt")


def create_id_file(abs_file_path: str):
    file = open(id_file, "wt")
    file.write(abs_file_path)
    file.close()


def read_id_file():
    file = open(id_file, "r")
    path = file.read().replace("\n", "")
    file.close()
    return path


def has_id_file():
    return os.path.exists(id_file)


def download_file():
    print("Downloading file...")
    file_path, _ = ApiClient().download_file(file_id, directory=directory, name=name)
    if not overwrite:
        create_id_file(file_path)
    print("File downloaded.")
    return file_path


if __name__ == "__main__":

    mkdir_exists(directory)
    if overwrite or not has_id_file():
        file_path = download_file()
    else:
        file_path = read_id_file()
        if os.path.isfile(file_path):
            print("Return file path from cache.")
        else:
            file_path = download_file()

    datatorch.set_output("path", file_path)
