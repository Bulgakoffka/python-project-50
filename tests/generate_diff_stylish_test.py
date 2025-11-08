from pathlib import Path

import pytest

from gendiff.diff_core.diff_builder import generate_diff
from gendiff.parser import load_file


@pytest.fixture
def get_json():
    base_path = Path(__file__).resolve().parent.parent
    file1 = base_path / "tests" / "test_data" / "file1.json"
    file2 = base_path / "tests" / "test_data" / "file2.json"
    file3 = base_path / "tests" / "test_data" / "file3.json"
    file4 = base_path / "tests" / "test_data" / "file4.json"
    return file1, file2, file3, file4


@pytest.fixture
def get_yaml():
    base_path = Path(__file__).resolve().parent.parent
    file1 = base_path / "tests" / "test_data" / "file1.yaml"
    file2 = base_path / "tests" / "test_data" / "file2.yaml"
    file3 = base_path / "tests" / "test_data" / "file3.yaml"
    file4 = base_path / "tests" / "test_data" / "file4.yaml"
    return file1, file2, file3, file4


@pytest.fixture
def get_answer1():
    return """{
- follow: False
  host: hexlet.io
- proxy: 123.234.53.22
- timeout: 50
+ timeout: 20
+ verbose: True
}"""


@pytest.fixture
def get_answer2():
    return """{
    common: {
      + follow: false 
        setting1: Value 1
      - setting2: 200 
      - setting3: true 
      + setting3: null 
      + setting4: blah blah
      + setting5: {
            key5: value5
        }
        setting6: {
            doge: {
              - wow: 
              + wow: so much
            }
            key: value
          + ops: vops
        }
    }
    group1: {
      - baz: bas
      + baz: bars
        foo: bar
      - nest: {
            key: value
        }
      + nest: str
    }
  - group2: {
        abc: 12345
        deep: {
            id: 45
        }
    }
  + group3: {
        deep: {
            id: {
                number: 45
            }
        }
        fee: 100500
    }
}"""


def test_generate_diff_json(get_json, get_answer1):
    file1, file2, _, _ = get_json
    parsed_file1 = dict(load_file(file1))
    parsed_file2 = dict(load_file(file2))
    assert generate_diff(parsed_file1, parsed_file2, 'stylish') == get_answer1


def test_generate_diff_json_recursive(get_json, get_answer2):
    _, _, file3, file4 = get_json
    parsed_file3 = dict(load_file(file3))
    parsed_file4 = dict(load_file(file4))
    assert generate_diff(parsed_file3, parsed_file4, 'stylish') == get_answer2


def test_generate_diff_yaml(get_yaml, get_answer1):
    file1, file2, _, _ = get_yaml
    parsed_file1 = dict(load_file(file1))
    parsed_file2 = dict(load_file(file2))
    assert generate_diff(parsed_file1, parsed_file2, 'stylish') == get_answer1


def test_generate_diff_yaml_recursive(get_yaml, get_answer2):
    _, _, file3, file4 = get_yaml
    parsed_file3 = dict(load_file(file3))
    parsed_file4 = dict(load_file(file4))
    assert generate_diff(parsed_file3, parsed_file4, 'stylish') == get_answer2

