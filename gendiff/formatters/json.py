import json as _json

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


def json(diff, depth=0):
    return _json.dumps(diff, indent=4)


