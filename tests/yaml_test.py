
from gendiff.diff_core.diff_builder import generate_diff


def test_generate_diff():
    assert (
        generate_diff('file1.yaml', 'file2.yaml')
        == """{
  - follow: false
    host: hexlet.io
  - proxy: 123.234.53.22
  - timeout: 50
  + timeout: 20
  + verbose: true
}"""
    )
