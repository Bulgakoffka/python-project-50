import json


def get_json(file_path: str):
    with open(file_path) as file:
        json_opened = json.load(file)
    return json_opened

def generate_diff(file_path1, file_path2):
    diff_dict = {}
    diff_string = ''
    parsed_file1 = get_json(file_path1)
    parsed_file2 = get_json(file_path2)
    joined_files = {**parsed_file1, **parsed_file2}
    for k, v in joined_files.items():
        match (k in parsed_file1, k in parsed_file2):
            case (True, True):
                if parsed_file1[k] == parsed_file2[k]:
                    diff_dict[f'  {k}'] = v
                else:
                    diff_dict[f'- {k}'] = parsed_file1[k]
                    diff_dict[f'+ {k}'] = parsed_file2[k]
            case (True, False):
                diff_dict[f'- {k}'] = v
            case (False, True):
                diff_dict[f'+ {k}'] = v

    diff_dict = sorted(diff_dict, key=lambda x: )
    diff_gen = {f'{k}: {v}' for k, v in diff_dict.items()}
    diff_string = '{\n' + '\n'.join(diff_gen) + '\n}`'
    return diff_string


if __name__ == "__main__":
    from pathlib import Path

    # Абсолютные пути к JSON-файлам
    base_path = Path(__file__).resolve().parent.parent.parent  # поднимаемся на 3 уровня до корня проекта
    file1 = base_path / "tests" / "test_data" / "file1.json"
    file2 = base_path / "tests" / "test_data" / "file2.json"

    print(generate_diff(str(file1), str(file2)))