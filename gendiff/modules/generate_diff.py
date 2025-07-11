from gendiff.modules.file_parser import parser


def generate_diff(file1, file2):
    diff_dict = {}
    diff_string = ''
    parsed_file1 = parser(file1)
    parsed_file2 = parser(file2)
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

    def keyorder(tpl):
        key = tpl[0]
        name = key[2:]
        order = ['  ', '- ', '+ ']
        for index, order_prefix in enumerate(order):
            if key.startswith(order_prefix):
                return (name, index)

    diff_dict = dict(sorted(diff_dict.items(), key=keyorder))
    diff_gen = [f'{k}: {v}' for k, v in diff_dict.items()]
    diff_string = '{\n' + '\n'.join(diff_gen) + '\n}'
    return diff_string


if __name__ == "__main__":
    from pathlib import Path  # pragma: no cover

    base_path = Path(__file__).resolve().parent.parent.parent
    file1 = base_path / "tests" / "test_data" / "file1.json"
    file2 = base_path / "tests" / "test_data" / "file2.json"

    print(generate_diff(str(file1), str(file2)))