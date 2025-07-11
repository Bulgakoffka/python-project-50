import json
import os

import yaml


def parser(file: str):
    from pathlib import Path
    base_path = Path(__file__).resolve().parent.parent.parent
    file = base_path / "tests" / "test_data" / file
    _, file_extension = os.path.splitext(file)
    with open(file) as file:
        if file_extension == '.yaml' or file_extension == '.yml':
            return yaml.safe_load(file)
        elif file_extension == '.json':
            return json.load(file)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")