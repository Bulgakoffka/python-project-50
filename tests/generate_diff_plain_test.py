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
def get_answer():
    return """Property 'common.follow' was added with value: false
Property 'common.setting2' was removed
Property 'common.setting3' was updated. From true to null
Property 'common.setting4' was added with value: 'blah blah'
Property 'common.setting5' was added with value: [complex value]
Property 'common.setting6.doge.wow' was updated. From '' to 'so much'
Property 'common.setting6.ops' was added with value: 'vops'
Property 'group1.baz' was updated. From 'bas' to 'bars'
Property 'group1.nest' was updated. From [complex value] to 'str'
Property 'group2' was removed
Property 'group3' was added with value: [complex value]"""


def test_generate_diff_json(get_json, get_answer):
    _, _, file3, file4 = get_json
    assert generate_diff(file3, file4) == get_answer


def test_generate_diff_yaml(get_yaml, get_answer):
    _, _, file3, file4 = get_yaml
    assert generate_diff(file3, file4) == get_answer
