import sys

from easygui.boxes.text_box import textbox


def to_string(something):
    try:
        basestring  # python 2
    except NameError:
        basestring = str  # Python 3

    if isinstance(something, basestring):
        return something
    try:
        text = "".join(something)  # convert a list or a tuple to a string
    except:
        textbox(
            "Exception when trying to convert {} to text in self.textArea"
            .format(type(something)))
        sys.exit(16)
    return text