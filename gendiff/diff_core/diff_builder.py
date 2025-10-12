from gendiff.diff_core.diff_actions import (
    diff_added,
    diff_deleted,
    diff_modified,
    diff_nested,
    diff_unchanged,
)
from gendiff.formatters.stylish import stylish
from gendiff.parser import load_file


# здесь проблема в рекурсии обработки стайлишем
# функция берет и дважды все оборачивает в форматер - исправлено
# нужно сделать обертку и чтобы это все поисходило внутри нее, а стайлишем обрабатывало снаружи
def generate_diff(file1: dict, file2: dict,):
    # здесб в самом начале ошибка где-то, из-за которой 
    # все ключи рекурсивно сбиваются вразнобой. возможно sorted
    print("*" * 10, '\n', 'gen_diff', f'{file1=} \n{file2=}  \n {"*" * 10}')
    result = []
    keys_set1 = set(file1.keys())
    keys_set2 = set(file2.keys())
    united_keys = sorted(keys_set1 | keys_set2) #a = {1, 2, 3} b = {2, 3, 4} c = {1, 2, 3, 4}
    intercepted_keys = sorted(keys_set1 & keys_set2) #a = {1, 2, 3} b = {2, 3, 4} c = {2, 3}
    only_first_keys = sorted(keys_set1 - keys_set2) #a = {1, 2, 3} b = {2, 3, 4} c = {1}
    only_second_keys = sorted(keys_set2 - keys_set1)  #a = {1, 2, 3} b = {2, 3, 4} c = {4}
    for key in united_keys:
        print("*" * 10)
        print('g_diff->for k in u_k')
        print(f',')
        print("*" * 10)
        if key in only_first_keys:
            result.append(diff_deleted(key, file1[key]))
        elif key in only_second_keys:
            result.append(diff_added(key, file2[key]))
        elif key in intercepted_keys:
            if isinstance(file1[key], dict) and isinstance(file2[key], dict):
                result.append(diff_nested(key, file1[key], file2[key], generate_diff))
            # elif not isinstance(file1[key], dict) and isinstance(file2[key], dict):
            #     result.append(diff_added())
            else:
                print("*" * 10)
                print('intercepted but !both_dict')
                print(f'{file1[key]=}')
                print(f'{file2[key]=}')
                print("*" * 10)
                if file1[key] == file2[key]:
                    print("*" * 10)
                    print('values equal', '\n', 'd_unchanged(val1)=', diff_unchanged(key, file1[key]))
                    result.append(diff_unchanged(key, file1[key]))
                    print("*" * 10)
                else:
                    # вот здесь при попадании сюда пары словарь/не-словарь да и в целом
                    # любой по идее не словарь когда попадает, дело уходит в генерейт_диф,
                    # который не умеет с такими данными работать
                    print("*" * 10)
                    print('values !equal')
                    print('d_mod(val1, val2, g_diff)=', diff_modified(key, file1[key], file2[key], generate_diff))
                    result.append(diff_modified(key, file1[key], file2[key], generate_diff))
                    print("*" * 10)
    return result


if __name__ == "__main__":
    from pathlib import Path  # pragma: no cover

    base_path = Path(__file__).resolve().parent.parent.parent
    file1 = "file3.json"
    file2 = "file4.json"

    parsed_file1 = dict(load_file(file1))
    parsed_file2 = dict(load_file(file2))
    sample_dict11 = {"group1": {"nest": {"key": "value"}}, "group2": {"id": 45}}
    sample_dict12 = {"group1": {"nest": "str"}, "group2": {"id": {"number": 45}}}
    
    hehe = stylish(generate_diff(parsed_file1, parsed_file2))
    print('*' * 10)
    print('d_builder__main__', hehe)
    print('*' * 10)
    print('*' * 10)
    print(f'{parsed_file1=}, \n{parsed_file2=}', hehe)
    print('*' * 10)
