import json
from pathlib import Path
import os
from .enumCollection import JsonKeys


def read_file(file_name: str)-> str :
    """Takes a file name and reads it.

    Args:
        file_name (str): Path of file from the main directory

    Returns:
        str: Returns a JSON of the contents of the file
    """
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, file_name)

    try:
        with open(file_path, 'r') as f:
            return f.read()
    except Exception as e:
        return json.dumps({JsonKeys.error.value: "File reading failed ".format(e)})
