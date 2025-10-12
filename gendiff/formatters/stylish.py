from gendiff.diff_core.diff_actions import diff_unchanged


REPLACER = " "
SPACES_COUNT = 4


def stylish(diff, depth=0):
    result = ""
    # возможно, формат вель. должен быть в дифф билдере

    # здесь мы пригоняем в нужный вид value из диффа
    # (либо возвращаем в нужном состоянии либо запускаем рекурсию для разворота вложенности)
    def format_value(f_value, f_depth):
        if isinstance(f_value, dict):
            if f_value.get("status") == "modified":
                return {
                    "old_value": format_value(f_value["old_value"], f_depth),
                    "new_value": format_value(f_value["new_value"], f_depth),
                }
            elif f_value.get("children"):
                return main_format(f_value["children"], f_depth + 1)
            elif not f_value.get("children"):
                # 9/10 здесь весь блок неправильный
                # ретерн в лупе фор внутри итерации
                # рандомные условия
                # дубли ретернов в разных условиях
                if isinstance(f_value.get("value"), dict):
                    # здесь попытка решить проблему привела к отсутствию
                    # сортировки у ключей
                    for inner_k, inner_v in f_value["value"].items():
                        result = []
                        k, v = inner_k, inner_v
                        new_val = diff_unchanged(k, v)
                        result.append(main_format(new_val, f_depth + 1))
                        str_result = '\n'.join(result)
                        print("*" * 10)
                        print('format_value->value isdict')
                        print(f'itemsitems {f_value["value"].items()=}')
                        print('AAAAAA', str_result)
                        print(f'{new_val=}')
                        print(f'{k=}, {v=}')
                        print(f'{str_result=}')
                        print("*" * 10)
                        return str_result
                elif not f_value.get('value') and not isinstance(f_value, dict):
                    print("*" * 10)
                    print('stylish->!value')
                    print(f', {f_value=}')
                    print("*" * 10)
                    return f_value
                # тут проблема с раскрытием вложенности
                elif f_value.get('status'):
                    print("*" * 10)
                    print('stylish->value')
                    print(f'{f_value['value']=}, {f_value=}')
                    print("*" * 10)
                    return f_value['value']
                
                return f_value.get("value")
        elif isinstance(f_value, (str, int)):
            return f_value
        elif not f_value.get('children'):
            value = f_value.get("value")
            print("*" * 10)
            print('stylish->match')
            print(f'old_{value=}')
            match value:
                case True:
                    if isinstance(value, bool):
                        value = 'true'
                case False:
                    value = 'false'
                case None:
                    value = 'null'
                    print("*" * 10)
                    print('stylish->match')
                    print(f'new_{value=}')
                    print("*" * 10)
                    return value
        

    def main_format(m_diff, m_depth):
        print("*" * 10)
        print('stylish->main_format')
        print(f'{m_diff=}')
        print("*" * 10)
        # indent и closing_brace_indent я украл из решения предыдущего наставника
        # Отступ для текущего уровня вложенности
        indent = REPLACER * (m_depth * SPACES_COUNT)
        # Отступ для закрывающей скобки (на уровень выше)
        closing_brace_indent = (
            REPLACER * ((m_depth) * SPACES_COUNT) if m_depth > 0 else ""
        )
        lines = []

        def wrapper(inner_diff, inner_depth):
            name = inner_diff.get("name")
            difference = inner_diff.get("status")
            nestness = inner_diff.get('children')
            print("*" * 10)
            print('stylish->main_format->wrapper1')
            print(f'{name=}')
            print("*" * 10)
            if not isinstance(inner_diff, dict):
                formatted_value = inner_diff
                print("*" * 10)
                print('wrapper !dict')
                print('formatted_value = inner_diff')
                print(f'{formatted_value=}, isdict={isinstance(formatted_value, dict)}')
                print("*" * 10)
            elif nestness:
                formatted_value = format_value(inner_diff, inner_depth)
                print("*" * 10)
                print('wrapper nestness')
                print(f'{formatted_value=}')
                print("*" * 10)
            else:
                formatted_value = format_value(inner_diff, inner_depth)
                print("*" * 10)
                print('wrapper else')
                print(f'{inner_diff=}, {type(inner_diff)}')
                print(f'{formatted_value=}')
                print("*" * 10)
                #  тут начинается рекурсивный луп
            # 8/10 тут я остановился на отладке
            print("*" * 10)
            print('stylish->main_format->wrapper2')
            print(f'{formatted_value=}')
            print("*" * 10)
            match difference:
                # 9/10
                # каждый раз тут начинается проблема:
                # форматтед велью делает что?? он то приносит готовый велью то
                # приносит необработанную структуру
                case "unchanged":
                    print("*" * 10)
                    print('match_unchanged')
                    print(f'line= f"{indent}    {name}: {formatted_value}"')
                    print("*" * 10)
                    lines.append(f"{indent}    {name}: {formatted_value}")
                case "added":
                    print("*" * 10)
                    print('match_added')
                    print(f'line= f"{indent}    {name}: {formatted_value}"')
                    print("*" * 10)
                    lines.append(f"{indent}  + {name}: {formatted_value}")
                case "deleted":
                    print("*" * 10)
                    print('match_deleted')
                    print(f'line= f"{indent}    {name}: {formatted_value}"')
                    print("*" * 10)
                    lines.append(f"{indent}  - {name}: {formatted_value}")
                case "modified":
                    # блок 17-24 привел к неверной обработке форматтед велью,
                    # из-за чего перестал работать блок с modified
                    print("*" * 10)
                    print('match_modified')
                    print(f'line= f"{indent}  - {name}: {formatted_value['old_value']}"')
                    print(f'line= f"{indent}  + {name}: {formatted_value['new_value']}"')
                    print("*" * 10)
                    lines.append(f"{indent}  - {name}: {formatted_value['old_value']}")
                    lines.append(f"{indent}  + {name}: {formatted_value['new_value']}")
                case "nested":
                    print("*" * 10)
                    print('match_nested')
                    print(f'line= f"{indent}    {name}: {formatted_value}"')
                    print("*" * 10)
                    lines.append(f"{indent}    {name}: {formatted_value}")
                case _:
                    print("*" * 10)
                    print('match_else')
                    print(f'line= f"{indent}    {name}: {formatted_value}"')
                    print("*" * 10)
                    lines.append(f"{indent}    {name}: {formatted_value}")

        if not isinstance(m_diff, list):
            if isinstance(m_diff, str):
                return f"{{\n{indent}   {m_diff}\n{closing_brace_indent}}}"
            wrapper(m_diff, m_depth)
        else:
            for d in m_diff:
                wrapper(d, m_depth)

        result = "" + f"\n{''}".join(lines)

        return f"{{\n{result}\n{closing_brace_indent}}}"

    return main_format(diff, depth)
