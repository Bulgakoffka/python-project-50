from pathlib import Path
from gendiff.modules.generate_diff import generate_diff

def test_generate_diff():
    base_path = Path(__file__).resolve().parent.parent
    file1 = base_path / "tests" / "test_data" / "file1.json"
    file2 = base_path / "tests" / "test_data" / "file2.json"
    assert generate_diff(file1, file2) == '''{
- follow: False
  host: hexlet.io
- proxy: 123.234.53.22
- timeout: 50
+ timeout: 20
+ verbose: True
}'''