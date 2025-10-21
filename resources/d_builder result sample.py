difference = [
    {
        'status': 'nested',
        'name': 'common',
        'value': None,
        'children': [
            {'status': 'added', 'name': 'follow', 'value': False},
            {'status': 'unchanged', 'name': 'setting1', 'value': 'Value 1'},
            {'status': 'deleted', 'name': 'setting2', 'value': 200},
            {
                'status': 'modified',
                'name': 'setting3',
                'old_value': True,
                'new_value': None
            },
            {'status': 'added', 'name': 'setting4', 'value': 'blah blah'},
            {'status': 'added', 'name': 'setting5', 'value': {'key5': 'value5'}},
            {
                'status': 'nested',
                'name': 'setting6',
                'value': None,
                'children': [
                    {
                        'status': 'nested',
                        'name': 'doge',
                        'value': None,
                        'children': [
                            {
                                'status': 'modified',
                                'name': 'wow',
                                'old_value': '',
                                'new_value': 'so much'
                            }
                        ]
                    },
                    {'status': 'unchanged', 'name': 'key', 'value': 'value'},
                    {'status': 'added', 'name': 'ops', 'value': 'vops'}
                ]
            }
        ]
    },
    {
        'status': 'nested',
        'name': 'group1',
        'value': None,
        'children': [
            {'status': 'modified', 'name': 'baz', 'old_value': 'bas', 'new_value': 'bars'},
            {'status': 'unchanged', 'name': 'foo', 'value': 'bar'},
            {'status': 'modified', 'name': 'nest', 'old_value': {'key': 'value'}, 'new_value': 'str'}
        ]
    },
    {
        'status': 'deleted',
        'name': 'group2',
        'value': {'abc': 12345, 'deep': {'id': 45}}
    },
    {
        'status': 'added',
        'name': 'group3',
        'value': {
            'deep': {'id': {'number': 45}},
            'fee': 100500
        }
    }
]


# тут надо поставить именованные аргументы чтобы
# можно было поставить
# если че олд велью или типа того

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


def get_json_standarted(node):
    def standart_value(value):
        match value:
            case True:
                value = 'true'
            case False:
                value = 'false'
            case None:
                value = 'null'
        return value
    if isinstance(node, list):
        new_node = []
        for i in node:
            new_node.append(get_json_standarted(i)) 
        return new_node
    if isinstance(node, dict):
        status = node.get('status')
        name = node.get('name')
        if status == 'modified':
            old_value = node.get("old_value")
            new_value = node.get("new_value")
        else:
            value = node.get("value")
        children = node.get('children')
        if not children:
            if status == 'modified':
                return get_node(status, name, standart_value(old_value), standart_value(new_value))
            return get_node(status, name, standart_value(value))
        else:
            new_children = []
            for kid in children:
                new_children.append(get_json_standarted(kid))
            return get_node(status, name, value, children=new_children)
    


print(get_json_standarted(difference))


new_res = [
    {
        'status': 'nested',
        'name': 'common',
        'value': None,
        'children': [
            {'status': 'added', 'name': 'follow', 'value': 'false'},
            {'status': 'unchanged', 'name': 'setting1', 'value': 'Value 1'},
            {'status': 'deleted', 'name': 'setting2', 'value': 200},
            {'status': 'modified', 'name': 'setting3', 'value': 'null'},
            {'status': 'added', 'name': 'setting4', 'value': 'blah blah'},
            {'status': 'added', 'name': 'setting5', 'value': {'key5': 'value5'}},
            {
                'status': 'nested',
                'name': 'setting6',
                'value': None,
                'children': [
                    {
                        'status': 'nested',
                        'name': 'doge',
                        'value': None,
                        'children': [
                            {'status': 'modified', 'name': 'wow', 'value': 'null'}
                        ]
                    },
                    {'status': 'unchanged', 'name': 'key', 'value': 'value'},
                    {'status': 'added', 'name': 'ops', 'value': 'vops'}
                ]
            }
        ]
    },
    {
        'status': 'nested',
        'name': 'group1',
        'value': None,
        'children': [
            {'status': 'modified', 'name': 'baz', 'value': 'null'},
            {'status': 'unchanged', 'name': 'foo', 'value': 'bar'},
            {'status': 'modified', 'name': 'nest', 'value': 'null'}
        ]
    },
    {
        'status': 'deleted',
        'name': 'group2',
        'value': {
            'abc': 12345,
            'deep': {'id': 45}
        }
    },
    {
        'status': 'added',
        'name': 'group3',
        'value': {
            'deep': {'id': {'number': 45}},
            'fee': 100500
        }
    }
]