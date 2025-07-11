import pytest
from gendiff.modules.file_parser import parser


def test_parser():
    # Test the parser function
    assert parser('file1.json') == {'host': 'hexlet.io', 'timeout': 50, 'proxy': '123.234.53.22', 'follow': False}
    with pytest.raises(ValueError):
        parser('file1.txt')
