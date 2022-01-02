import json
from pathlib import Path
import os
from .enumCollection import JsonKeys


def read_file(file_name):
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, file_name)

    try:
        with open(file_path, 'r') as f:
            return f.read()
    except Exception as e:
        return json.dumps({JsonKeys.error.value: "File reading failed ".format(e)})
