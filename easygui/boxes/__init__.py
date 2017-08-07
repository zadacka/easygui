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


window_position = "+300+200"
PROPORTIONAL_FONT_FAMILY = ("MS", "Sans", "Serif")
MONOSPACE_FONT_FAMILY = "Courier"
PROPORTIONAL_FONT_SIZE = 10
MONOSPACE_FONT_SIZE = 9
TEXT_ENTRY_FONT_SIZE = 12  # a little larger makes it easier to see
STANDARD_SELECTION_EVENTS = ["Return", "Button-1", "space"]
prop_font_line_length = 62
fixw_font_line_length = 80
num_lines_displayed = 50
default_hpad_in_chars = 2
runningPython27 = False
runningPython34 = False
