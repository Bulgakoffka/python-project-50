
import pytest

from gendiff.diff_core.diff_builder import generate_diff


@pytest.fixture
def get_json():
    file1 = "file1.json"
    file2 = "file2.json"
    file3 = "file3.json"
    file4 = "file4.json"
    return file1, file2, file3, file4


@pytest.fixture
def get_yaml():
    file1 = "file1.yaml"
    file2 = "file2.yaml"
    file3 = "file3.yaml"
    file4 = "file4.yaml"
    return file1, file2, file3, file4


@pytest.fixture
def get_answer1():
    return """[
    {
        "status": "deleted",
        "name": "follow",
        "value": "false"
    },
    {
        "status": "unchanged",
        "name": "host",
        "value": "hexlet.io"
    },
    {
        "status": "deleted",
        "name": "proxy",
        "value": "123.234.53.22"
    },
    {
        "status": "modified",
        "name": "timeout",
        "old_value": 50,
        "new_value": 20
    },
    {
        "status": "added",
        "name": "verbose",
        "value": "true"
    }
]"""


@pytest.fixture
def get_answer2():
    return """[
    {
        "status": "nested",
        "name": "common",
        "children": [
            {
                "status": "added",
                "name": "follow",
                "value": "false"
            },
            {
                "status": "unchanged",
                "name": "setting1",
                "value": "Value 1"
            },
            {
                "status": "deleted",
                "name": "setting2",
                "value": 200
            },
            {
                "status": "modified",
                "name": "setting3",
                "old_value": "true",
                "new_value": "null"
            },
            {
                "status": "added",
                "name": "setting4",
                "value": "blah blah"
            },
            {
                "status": "added",
                "name": "setting5",
                "value": {
                    "key5": "value5"
                }
            },
            {
                "status": "nested",
                "name": "setting6",
                "children": [
                    {
                        "status": "nested",
                        "name": "doge",
                        "children": [
                            {
                                "status": "modified",
                                "name": "wow",
                                "old_value": "",
                                "new_value": "so much"
                            }
                        ],
                        "value": null
                    },
                    {
                        "status": "unchanged",
                        "name": "key",
                        "value": "value"
                    },
                    {
                        "status": "added",
                        "name": "ops",
                        "value": "vops"
                    }
                ],
                "value": null
            }
        ],
        "value": null
    },
    {
        "status": "nested",
        "name": "group1",
        "children": [
            {
                "status": "modified",
                "name": "baz",
                "old_value": "bas",
                "new_value": "bars"
            },
            {
                "status": "unchanged",
                "name": "foo",
                "value": "bar"
            },
            {
                "status": "modified",
                "name": "nest",
                "old_value": {
                    "key": "value"
                },
                "new_value": "str"
            }
        ],
        "value": null
    },
    {
        "status": "deleted",
        "name": "group2",
        "value": {
            "abc": 12345,
            "deep": {
                "id": 45
            }
        }
    },
    {
        "status": "added",
        "name": "group3",
        "value": {
            "deep": {
                "id": {
                    "number": 45
                }
            },
            "fee": 100500
        }
    }
]"""


def test_generate_diff_json(get_json, get_answer1):
    file1, file2, _, _ = get_json
    assert generate_diff(file1, file2, 'json') == get_answer1


def test_generate_diff_json_recursive(get_json, get_answer2):
    _, _, file3, file4 = get_json
    assert generate_diff(file3, file4, 'json') == get_answer2


def test_generate_diff_yaml(get_yaml, get_answer1):
    file1, file2, _, _ = get_yaml
    assert generate_diff(file1, file2, 'json') == get_answer1


def test_generate_diff_yaml_recursive(get_yaml, get_answer2):
    _, _, file3, file4 = get_yaml
    assert generate_diff(file3, file4, 'json') == get_answer2

