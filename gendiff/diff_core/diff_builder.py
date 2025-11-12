from gendiff.diff_core.diff_actions import (
    diff_added,
    diff_deleted,
    diff_modified,
    diff_nested,
    diff_unchanged,
)
from gendiff.formatters.json import json
from gendiff.formatters.plain import plain
from gendiff.formatters.stylish import stylish
from gendiff.parser import load_file


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


def standart_value(value):
    match value:
        case True:
            value = 'true'
        case False:
            value = 'false'
        case None:
            value = 'null'
    return value


def get_json_standarted(node):
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
                return get_node(status, name, standart_value(old_value),
                                 standart_value(new_value))
            return get_node(status, name, standart_value(value))
        new_children = []
        for kid in children:
            new_children.append(get_json_standarted(kid))
        return get_node(status, name, value, children=new_children)


def is_both_dict(node1, node2):
    return isinstance(node1, dict) and isinstance(node2, dict)            


def generate_diff(file1: dict, file2: dict, format_name='None'):  # noqa: C901
    loaded_file1 = load_file(file1)
    loaded_file2 = load_file(file2)

    def wrapper(inner_file1: dict, inner_file2: dict):
        result = []
        keys_set1 = set(inner_file1.keys())
        keys_set2 = set(inner_file2.keys())
        united_keys = sorted(keys_set1 | keys_set2) 
        intercepted_keys = sorted(keys_set1 & keys_set2) 
        only_first_keys = sorted(keys_set1 - keys_set2) 
        only_second_keys = sorted(keys_set2 - keys_set1)  
        for key in united_keys:
            if key in only_first_keys:
                result.append(diff_deleted(key, inner_file1[key]))
            elif key in only_second_keys:
                result.append(diff_added(key, inner_file2[key]))
            elif key in intercepted_keys:
                if is_both_dict(inner_file1[key], inner_file2[key]):
                    result.append(diff_nested(key,
                                               inner_file1[key],
                                                 inner_file2[key], wrapper))
                elif inner_file1[key] == inner_file2[key]:
                    result.append(diff_unchanged(key, inner_file1[key]))
                else:
                    result.append(diff_modified(key,
                                                     inner_file1[key],
                                                       inner_file2[key],
                                                         wrapper))
        return result
    final_diff = get_json_standarted(wrapper(loaded_file1, loaded_file2))
    match format_name:
        case _:
            diff = stylish(final_diff)
        case 'plain':
            diff = plain(final_diff)
        case 'json':
            diff = json(final_diff)
        case 'lala':
            diff = 'incorrect formatter name'
    return diff
