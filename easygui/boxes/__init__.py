try:
    import tkinter as tk  # python 3
except ImportError:
    import Tkinter as tk  # python 2


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


GLOBAL_WINDOW_POSITION = "+300+200"
PROPORTIONAL_FONT_FAMILY = ("MS", "Sans", "Serif")
MONOSPACE_FONT_FAMILY = "Courier"
PROPORTIONAL_FONT_SIZE = 10
MONOSPACE_FONT_SIZE = 9
TEXT_ENTRY_FONT_SIZE = 12  # a little larger makes it easier to see
STANDARD_SELECTION_EVENTS = ["Return", "Button-1", "space"]
PROP_FONT_LINE_LENGTH = 62
FIXW_FONT_LINE_LENGTH = 80
num_lines_displayed = 50

DEFAULT_PADDING = 2
REGULAR_FONT_WIDTH = 13
FIXED_FONT_WIDTH = 7


def get_width_and_padding(monospace):
    if monospace:
        padding = DEFAULT_PADDING * FIXED_FONT_WIDTH
        width_in_chars = FIXW_FONT_LINE_LENGTH
    else:
        padding = DEFAULT_PADDING * REGULAR_FONT_WIDTH
        width_in_chars = PROP_FONT_LINE_LENGTH
    return padding, width_in_chars


def get_num_lines(message_area):
    num_lines, _ = message_area.index(tk.END).split('.')
    return num_lines