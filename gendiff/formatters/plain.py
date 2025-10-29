def plain(diff):
    result = [] 
    
    def format_value(value):
        if isinstance(value, (dict, list)):
            return '[complex value]'
        if value == 'true' or value == 'false' or value == 'null':
            return value
        elif isinstance(value, str) and not len(value):
            return "''"
        else:
            return f"'{value}'"
        
    def make_line(node_path, status, value1=None, value2=None):
        addition = '\n'
        formatted_value1 = format_value(value1)
        if value2:
            formatted_value2 = format_value(value2)
        match status:
            case 'modified':
                status = 'updated'
                addition = f'. From {formatted_value1} to {formatted_value2}\n'
            case 'deleted':
                status = 'removed'
                addition = '\n'
            case 'added':
                status = 'addded'
                addition = f' with value: {formatted_value1}\n'
        line = f"Property '{node_path}' was {status}{addition}"
        return line

    iterator = iter(range(1, 999))
    path = []
    def wrapper(inner_diff, path):
        
        if isinstance(inner_diff, list):
            for node in inner_diff:
                result.append(wrapper(node, path))
            return result
        name = inner_diff.get('name')
        if name not in path:
            path.append(name)
        inner_path = '.'.join(path)
        status = inner_diff.get('status')
        if status == 'modified':
            old_value = inner_diff['old_value']
            new_value = inner_diff['new_value']
        else:
            value = inner_diff.get('value')
        children = inner_diff.get('children')
        match status:
            case 'nested':
                nested_result = []
                for item in children:
                    nested_result.append(wrapper(item, path))
                path.pop(-1)
                return ''.join(nested_result)
            case 'modified':
                path.pop(-1)
                return make_line(inner_path, status, old_value, new_value)
            case 'unchanged':
                path.pop(-1)
                return ''
            case _:
                path.pop(-1)
                return make_line(inner_path, status, value)
    return "".join(wrapper(diff, path))