def diff_unpack(value):
    if isinstance(value, dict):
        return diff_unchanged(next(iter(value)), next(iter(value.values())))
    return value


def diff_unchanged(key, value):
    return {"status": "unchanged", "name": key, "value": value}


def diff_added(key, value):
    return {"status": "added", "name": key, "value": value}


def diff_deleted(key, value):
    return {"status": "deleted", "name": key, "value": value}


def diff_modified(key, value1, value2, func):
    result = dict()
    result = {"status": "modified", "name": key, 'old_value': value1, 'new_value': value2}
    if isinstance(value1, dict) and isinstance(value2, dict):
        result['old_value'] = func(value1, value1)[0]
        result['new_value'] = func(value2, value2)[0]
    else:
        result['old_value'] = value1
        result['new_value'] = value2
    return result
    

def diff_nested(key, file1, file2, func):
    return {
        "status": "nested",
        "name": key,
        "value": None,
        "children": func(file1, file2),
    }
