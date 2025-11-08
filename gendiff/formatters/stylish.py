from gendiff.diff_core.diff_actions import diff_unchanged

REPLACER = " "
SPACES_COUNT = 4


def get_node(status, name, value, value2=None, children=None):
    node = {'status': status, 'name': name}
    if children is not None:
        node['children'] = children
    if status == 'modified':
        node['old_value'] = value
        node['new_value'] = value2
    else:
        node['value'] = value
    return node


def format_value(f_value, f_depth):  # noqa: C901
    if isinstance(f_value, (str, int)):
        return f_value
    if f_value.get("status") == "modified":
        return {
            "old_value": format_value(f_value["old_value"], f_depth),
            "new_value": format_value(f_value["new_value"], f_depth),
        }
    elif f_value.get("children"):
        return stylish(f_value["children"], f_depth + 1)
    if isinstance(f_value.get("value"), dict):
        result = []
        for inner_k, inner_v in f_value["value"].items():
            new_val = diff_unchanged(inner_k, inner_v)
            result.append(new_val)  
        formatted_result = stylish(result, f_depth + 1)
        str_result = formatted_result
        return str_result
    elif f_value.get('status'):
        return f_value['value']
    if len(f_value) > 1:
        result = []
        for k, v in f_value.items():
            result.append(get_node('unchanged', k, v))
        return result
    for k, v in f_value.items():
        return stylish(get_node('unchanged',
                                        k, v), f_depth + 1)


def stylish(diff, depth=0):  # noqa: C901
    indent = REPLACER * (depth * SPACES_COUNT)
    closing_brace_indent = (
        REPLACER * ((depth) * SPACES_COUNT) if depth > 0 else ""
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
            case "added":
                lines.append(f"{indent}  + {name}: {formatted_value}")
            case "deleted":
                lines.append(f"{indent}  - {name}: {formatted_value}")
            case "modified":
                old_value = formatted_value['old_value']
                new_value = formatted_value['new_value']
                lines.append(f"{indent}  - {name}: {old_value}")
                lines.append(f"{indent}  + {name}: {new_value}")
            case _:
                lines.append(f"{indent}    {name}: {formatted_value}")

    if not isinstance(diff, list):
        if isinstance(diff, str):
            return f"{{\n{indent}   {diff}\n{closing_brace_indent}}}"
        wrapper(diff, depth)
    else:
        for d in diff:
            wrapper(d, depth)

    result = "" + f"\n{''}".join(lines)
    return f"{{\n{result}\n{closing_brace_indent}}}"
