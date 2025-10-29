from pathlib import Path
import pytest
from gendiff.diff_core.generate_diff import generate_diff


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
    assert generate_diff(file1, file2) == get_answer1


def test_generate_diff_json_recursive(get_json, get_answer2):
    _, _, file3, file4 = get_json
    assert generate_diff(file3, file4) == get_answer2


def test_generate_diff_yaml(get_yaml, get_answer1):
    file1, file2, _, _ = get_yaml
    assert generate_diff(file1, file2) == get_answer1


def test_generate_diff_yaml_recursive(get_yaml, get_answer2):
    _, _, file3, file4 = get_yaml
    assert generate_diff(file3, file4) == get_answer2
