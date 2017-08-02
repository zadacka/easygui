def to_string(something):
    if isinstance(something, str):
        return something
    elif isinstance(something, iter):
        return "".join(something)  # raises TypeError on failure
    else:
        "{}".format(something)
