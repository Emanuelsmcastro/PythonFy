def comparator(value, type) -> bool:
    result = False
    try:
        if isinstance(value, type):
            result = True
    except TypeError:
        result = False
    return result
        