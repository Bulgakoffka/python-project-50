from pathlib import Path
from gendiff.parser import load_file
from gendiff.diff_core.diff_builder import generate_diff


def test_generate_diff():
    base_path = Path(__file__).resolve().parent.parent
    file1 = base_path / "tests" / "test_data" / "file1.yaml"
    file2 = base_path / "tests" / "test_data" / "file2.yaml"
    parsed_file1 = dict(load_file(file1))
    parsed_file2 = dict(load_file(file2))
    assert (
        generate_diff(parsed_file1, parsed_file2)
        == """{
  - follow: false
    host: hexlet.io
  - proxy: 123.234.53.22
  - timeout: 50
  + timeout: 20
  + verbose: true
}"""
    )
