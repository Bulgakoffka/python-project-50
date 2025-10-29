from gendiff.diff_core.diff_actions import diff_unchanged


REPLACER = " "
SPACES_COUNT = 4

def get_node(status, name, value, value2=None, children=None):
    node = {'status': status, 'name': name}
    if children != None:
        node['children'] = children
    if status == 'modified':
        node['old_value'] = value
        node['new_value'] = value2
    else:
        node['value'] = value
    return node




def stylish(diff, depth=0):
    result = ""

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
                if isinstance(f_value.get("value"), dict):
                    result = []
                    # 21/10 луп почему-то берет побуквенно ключи и значения
                    for inner_k, inner_v in f_value["value"].items():
                        new_val = diff_unchanged(inner_k, inner_v)
                        result.append(new_val)
                        
                    formatted_result = main_format(result, f_depth + 1)
                    str_result = formatted_result
                    return str_result
                elif not f_value.get('value') and not isinstance(f_value, dict):
                    return f_value
                elif f_value.get('status'):
                    return f_value['value']
                
                else:
                    if len(f_value) > 1:
                        result = []
                        for k, v in f_value.items():
                            result.append(get_node('unchanged', k, v))
                        return result
                    else:
                        for k, v in f_value.items():
                            return main_format(get_node('unchanged', k, v), f_depth)
        elif isinstance(f_value, (str, int)):
            return f_value
            
        

    def main_format(m_diff, m_depth):
        indent = REPLACER * (m_depth * SPACES_COUNT)
        closing_brace_indent = (
            REPLACER * ((m_depth) * SPACES_COUNT) if m_depth > 0 else ""
        )
        lines = []

        def wrapper(inner_diff, inner_depth):
            name = inner_diff.get("name")
            status = inner_diff.get("status")
            if not isinstance(inner_diff, dict):
                # убрать
                formatted_value = inner_diff
            else:
                formatted_value = format_value(inner_diff, inner_depth)
                
            match status:
                # 9/10
                # каждый раз тут начинается проблема:
                # форматтед велью делает что?? он то
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
