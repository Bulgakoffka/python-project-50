# тут на 200 строчек база для тестов и абстракция действий


sample_dict = {
    "name": "etc",
    "status": "add",
    "value": None,
    "children": {
        "name": "bashrc",
        "value2": None,
        "children": [],
    },
}

sample_dict2 = {
    "name": "et",
    "sttus": "add",
    "value": None,
    "children": {
        "nae": "bshrc",
        "value2": None,
        "children": [],
    },
}

sample_dict3 = {
    "hui": "15sm",
    "pochemy": "hui",
}

sample_dict4 = {
    "hui": "15sm",
    "pp": None,
    "pochemy": "grustnyi",
}

sample_dict5 = {
    "common": {
        "setting1": "Value 1",
        "setting2": 200,
        "setting3": True,
        "setting6": {"key": "value", "doge": {"wow": ""}},
    },
    "group1": {"baz": "bas", "foo": "bar", "nest": {"key": "value"}},
    "group2": {"abc": 12345, "deep": {"id": 45}},
}

sample_dict6 = {
    "common": {
        "follow": True,
        "setting1": "Value 1",
        "setting3": None,
        "setting4": "blah blah",
        "setting5": {"key5": "value5"},
        "setting6": {"key": "value", "ops": "vops", "doge": {"wow": "so much"}},
    },
    "group1": {"foo": "bar", "baz": "bars", "nest": "str"},
    "group3": {"deep": {"id": {"number": 45}}, "fee": 100500},
}

sample_dict7 = {
    "block1": {"param1": "one", "param2": "two"},
    "block2": {"item1": 111, "item2": 222},
}

sample_dict8 = {
    "block1": {"param1": "one", "param2": None},
    "block3": {"item1": {"deep1": "nested"}, "item2": 999},
}

sample_dict9 = {"block1": {"param1": "one"}, "block2": {"item1": 111}}

sample_dict10 = {"block1": {"param1": "one"}, "block3": {"item1": {"deep1": "nested"}}}

sample_dict11 = {"group1": {"nest": {"key": "value"}}, "group2": {"id": 45}}

sample_dict12 = {"group1": {"nest": "str"}, "group2": {"id": {"number": 45}}}


def diff_unchanged(key, value):
    return {"status": "unchanged", "name": key, "value": value}


def diff_added(key, value):
    return {"status": "added", "name": key, "value": value}


def diff_deleted(key, value):
    return {"status": "deleted", "name": key, "value": value}


def diff_modified(key, value1, value2):
    return {"status": "modified", "name": key, "old_value": value1, "new_value": value2}


def diff_nested(key, file1, file2):
    return {"status": "nested", "name": key, "children": generate_diff(file1, file2)}


def generate_diff(file1, file2):
    result = []
    united_keys = sorted(file1.keys() | file2.keys())
    intercepted_keys = file1.keys() & file2.keys()
    only_first_keys = file1.keys() - file2.keys()
    only_second_keys = file2.keys() - file1.keys()
    for i in united_keys:
        if i in only_first_keys:
            result.append(diff_deleted(i, file1[i]))
        elif i in only_second_keys:
            result.append(diff_added(i, file2[i]))
        elif i in intercepted_keys:
            if isinstance(file1[i], dict) and isinstance(file2[i], dict):
                result.append(diff_nested(i, file1[i], file2[i]))
            else:
                if file1[i] == file2[i]:
                    result.append(diff_unchanged(i, file1[i]))
                else:
                    result.append(diff_modified(i, file1[i], file2[i]))
    return result


# константы тоже украл из решения другой задачи от наставника
# наставник: Вместо магических чисел, лучше задать константы
REPLACER = " "
SPACES_COUNT = 4


# основная проблема, с которой я столкнулся, это неправильный разворот вложенности,
# если она статична, а не изменена, например
def stylish(diff, depth=0):
    result = ""

    # здесь мы пригоняем в нужный вид value из диффа
    # (либо возвращаем в нужном состоянии либо запускаем рекурсию для разворота вложенности)
    def format_value(f_value, f_depth):
        if isinstance(f_value, (str, int)):
            return f_value
        if isinstance(f_value, dict):
            if f_value.get("status") == "modified":
                return {
                    "old_value": format_value(f_value["old_value"], f_depth + 1),
                    "new_value": format_value(f_value["new_value"], f_depth + 1),
                }
            elif f_value.get("children"):
                return main_format(f_value["children"], f_depth + 1)
            elif not f_value.get("children"):
                # здесь костыль, потому что абстракция не понимает, что перед ней вложенность
                # если она не является различием
                # мы собираем для вложенного словаря в дифе структуру для основной машины заново
                if isinstance(f_value.get("value"), dict):
                    for inner_k, inner_v in f_value["value"].items():
                        k, v = inner_k, inner_v
                        new_val = diff_unchanged(k, v)
                        return main_format(new_val, f_depth + 1)
                else:
                    for inner_k, inner_v in f_value.items():
                        k, v = inner_k, format_value(inner_v, f_depth)
                    return main_format(f"{k}: {v}", f_depth)

                return f_value["value"]

    def main_format(m_diff, m_depth):
        # indent и closing_brace_indent я украл из решения предыдущего наставника
        # Отступ для текущего уровня вложенности
        indent = REPLACER * (m_depth * SPACES_COUNT)
        # Отступ для закрывающей скобки (на уровень выше)
        closing_brace_indent = (
            REPLACER * ((m_depth) * SPACES_COUNT) if m_depth > 0 else ""
        )
        lines = []

        def wrapper(inner_diff, inner_depth):
            name = inner_diff["name"]
            difference = inner_diff.get("status")
            if isinstance(inner_diff, str):
                formatted_value = inner_diff
            else:
                formatted_value = format_value(inner_diff, inner_depth)
                # тут у меня проблема с краденными отступами
                # закрытие просто не работает, а открытие работает некорректно
            match difference:
                case "unchanged":
                    lines.append(f"{indent}    {name}: {formatted_value}")
                case "added":
                    lines.append(f"{indent}  + {name}: {formatted_value}")
                case "deleted":
                    lines.append(f"{indent}  - {name}: {formatted_value}")
                case "modified":
                    lines.append(f"{indent}  - {name}: {formatted_value['old_value']}")
                    lines.append(f"{indent}  + {name}: {formatted_value['new_value']}")
                case "nested":
                    lines.append(f"{indent}    {name}: {formatted_value}")
                case _:
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


# это собственно решение наставника старое. причем он сам не помнил задачу корректно
# по идее это испытание json stringify
# кстати работает вроде не особо корректно, уже не помню
def stringify_dict(node, depth=0):

    # Отступ для текущего уровня вложенности
    indent = REPLACER * (depth * SPACES_COUNT)
    # Отступ для закрывающей скобки (на уровень выше)
    closing_brace_indent = REPLACER * ((depth - 1) * SPACES_COUNT) if depth > 0 else ""

    lines = []
    for key, value in node.items():
        # Для каждого значения вызываем наш хелпер
        formatted_value = format_value(value, depth)
        lines.append(f"{indent}    {key}: {formatted_value}")

    result = "\n".join(lines)

    return f"{{\n{result}\n{closing_brace_indent}}}"


print(stylish(generate_diff(sample_dict11, sample_dict12)))
print("-------------------------------")
print("-------------------------------")
print("-------------------------------")
# print(generate_diff(sample_dict11, sample_dict12))
