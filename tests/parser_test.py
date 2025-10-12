import pytest

from gendiff.parser import load_file


def test_parser():
    # Test the parser function
    assert load_file("file1.json") == {
        "host": "hexlet.io",
        "timeout": 50,
        "proxy": "123.234.53.22",
        "follow": False,
    }
    with pytest.raises(ValueError):
        load_file("file1.txt")
