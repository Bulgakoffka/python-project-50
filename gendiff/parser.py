from argparse import ArgumentParser
import json
import os
from pathlib import Path
import yaml

# парсер не может принять null значение, возвращает только None
def load_file(file_name: str):

    base_path = Path(__file__).resolve().parent.parent
    file_name = base_path / "tests" / "test_data" / file_name
    _, file_extension = os.path.splitext(file_name)
    with open(file_name) as file_name:
        if file_extension == ".yaml" or file_extension == ".yml":
            return yaml.safe_load(file_name)
        elif file_extension == ".json":
            return json.load(file_name)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")


def arg_parser():  # pragma: no cover
    parser = ArgumentParser(
        prog="gendiff",
        description="Compares two configuration" " files and shows a difference.",
        usage="gendiff [-h] first_file second_file format_name",
    )
    parser.add_argument("-f", "--format", help="set format of output")
    parser.add_argument("first_file")
    parser.add_argument("second_file")
    parser.add_argument('format_name', nargs='?', default='stylish')
    return parser.parse_args()
