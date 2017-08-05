def to_string(something):
    if isinstance(something, str):
        return something
    elif isinstance(something, iter):
        return "".join(something)  # raises TypeError on failure
    else:
        "{}".format(something)


boxRoot = None


def bindArrows(widget):
    widget.bind("<Down>", tabRight)
    widget.bind("<Up>", tabLeft)

    widget.bind("<Right>", tabRight)
    widget.bind("<Left>", tabLeft)


def tabRight(event):
    boxRoot.event_generate("<Tab>")


def tabLeft(event):
    boxRoot.event_generate("<Shift-Tab>")
