import sys

from easygui.guitk import GUItk

try:
    import tkinter as tk  # python 3
    import tkinter.font as tk_Font
except ImportError:
    import Tkinter as tk  # python 2
    import tkFont as tk_Font


def textbox(msg="", title=" ", text="", codebox=False, callback=None, run=True):
    """ Helper method to pre-configure the class."""
    tb = TextBox(msg=msg, title=title, text=text, codebox=codebox, callback=callback)
    return tb.run() if run else tb


class TextBox(object):
    """ Display a message and a editable text field pre-populated with 'text'.
        Separate user from UI implementation and make agnostic to underlying library (TK)
            so that other libraries (WX, QT) could be used without negative user impact.
     """

    def __init__(self, msg, title, text, codebox, callback=lambda *args, **kwargs: True):
        """
        :param msg: str displayed in the message area (instructions...)
        :param title: str used as the window title
        :param text: str displayed in textArea (editable)
        :param codebox: bool (if true) don't wrap and width set to 80 chars
        :param callback: optional function to be called when OK is pressed
        """
        self.callback = callback
        self.ui = GUItk(msg, title, text, codebox, self.callback_ui)
        self._text = text
        self._msg = msg

    def run(self):
        """ Start the ui.
            Returns None if cancel is pressed, else returns the contents of textArea
        """
        self.ui.run()
        self.ui = None
        return self._text

    def stop(self):
        self.ui.stop()

    def callback_ui(self, ui, command, text):
        """ This method is executed when ok, cancel, or x is pressed in the ui. """
        if command == 'update':  # OK was pressed
            self._text = text
            if self.callback:
                # If a callback was set, call main process
                self.callback(self)
            else:
                self.stop()
        elif command in ('x', 'cancel'):
            self.stop()
            self._text = None

    @property
    def text(self):
        """Text in text Area"""
        return self._text

    @text.setter
    def text(self, text):
        self._text = to_string(text)
        self.ui.set_text(self._text)

    @text.deleter
    def text(self):
        self._text = ""
        self.ui.set_text(self._text)

    @property
    def msg(self):
        """Text in msg Area"""
        return self._msg

    @msg.setter
    def msg(self, msg):
        self._msg = to_string(msg)
        self.ui.set_msg(self._msg)

    @msg.deleter
    def msg(self):
        self._msg = ""
        self.ui.set_msg(self._msg)


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