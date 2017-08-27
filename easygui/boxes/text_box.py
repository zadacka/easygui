try:
    import tkinter as tk  # python 3
except ImportError:
    import Tkinter as tk  # python 2

from easygui.boxes import to_string, FIXW_FONT_LINE_LENGTH, PROP_FONT_LINE_LENGTH, \
    GLOBAL_WINDOW_POSITION

DEFAULT_PADDING = 2
REGULAR_FONT_WIDTH = 13
FIXED_FONT_WIDTH = 7


def get_width_and_padding(code_box):
    if code_box:
        padding = DEFAULT_PADDING * FIXED_FONT_WIDTH
        width_in_chars = FIXW_FONT_LINE_LENGTH
    else:
        padding = DEFAULT_PADDING * REGULAR_FONT_WIDTH
        width_in_chars = PROP_FONT_LINE_LENGTH
    return padding, width_in_chars


def textbox(msg="", title=" ", text="", codebox=False, callback=None, run=True):
    """ Helper method to pre-configure the class."""
    tb = TextBox(msg=msg, title=title, text=text, codebox=codebox, callback=callback)
    # TODO: confirm behavioural change is okay (always return tb, not sometimes tb sometimes string)
    if run:
        tb.run()
    return tb


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
        self.ui.set_msg_area(self._msg)

    @msg.deleter
    def msg(self):
        self._msg = ""
        self.ui.set_msg_area(self._msg)


class GUItk(object):
    def __init__(self, msg, title, text, code_box, callback):
        self.callback = callback

        self.box_root = self._configure_box_root(title)
        self.message_area = self._configure_message_area(box_root=self.box_root, code_box=code_box)
        self.text_area = self._configure_text_area(box_root=self.box_root, code_box=code_box)
        self._configure_buttons()

        self.set_msg_area("" if msg is None else msg)
        self.set_text(text)

    def _configure_box_root(self, title):
        box_root = tk.Tk()
        box_root.title(title)
        box_root.iconname('Dialog')
        box_root.geometry(GLOBAL_WINDOW_POSITION)
        box_root.protocol('WM_DELETE_WINDOW', self.x_pressed)  # Quit when x button pressed
        box_root.bind("<Escape>", self.cancel_button_pressed)
        return box_root

    @staticmethod
    def _configure_message_area(box_root, code_box):
        padding, width_in_chars = get_width_and_padding(code_box)

        message_frame = tk.Frame(box_root, padx=padding)
        message_frame.pack(side=tk.TOP, expand=1, fill='both')

        message_area = tk.Text(master=message_frame,
                               width=width_in_chars,
                               padx=padding,
                               pady=padding,
                               wrap=tk.WORD)
        message_area.pack(side=tk.TOP, expand=1, fill='both')
        return message_area

    @staticmethod
    def _configure_text_area(box_root, code_box):
        padding, width_in_chars = get_width_and_padding(code_box)

        text_frame = tk.Frame(box_root, padx=padding, )
        text_frame.pack(side=tk.TOP)

        text_area = tk.Text(text_frame, padx=padding, pady=padding, height=25, width=width_in_chars)
        text_area.configure(wrap=tk.NONE if code_box else tk.WORD)

        vertical_scrollbar = tk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_area.yview)
        text_area.configure(yscrollcommand=vertical_scrollbar.set)

        horizontal_scrollbar = tk.Scrollbar(text_frame, orient=tk.HORIZONTAL, command=text_area.xview)
        text_area.configure(xscrollcommand=horizontal_scrollbar.set)

        if code_box:
            # no word-wrapping for code so we need a horizontal scroll bar
            horizontal_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        vertical_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # pack textArea last so bottom scrollbar displays properly
        text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)

        box_root.bind("<Next>", text_area.yview_scroll(1, tk.PAGES))
        box_root.bind("<Prior>", text_area.yview_scroll(-1, tk.PAGES))

        box_root.bind("<Right>", text_area.xview_scroll(1, tk.PAGES))
        box_root.bind("<Left>", text_area.xview_scroll(-1, tk.PAGES))

        box_root.bind("<Down>", text_area.yview_scroll(1, tk.UNITS))
        box_root.bind("<Up>", text_area.yview_scroll(-1, tk.UNITS))

        return text_area

    def _configure_buttons(self):
        buttons_frame = tk.Frame(self.box_root)
        buttons_frame.pack(side=tk.TOP)

        cancel_button = tk.Button(buttons_frame, takefocus=tk.YES, text="Cancel", height=1, width=6)
        cancel_button.pack(expand=tk.NO, side=tk.LEFT, padx='2m', pady='1m', ipady="1m", ipadx="2m")
        cancel_button.bind("<Return>", self.cancel_button_pressed)
        cancel_button.bind("<Button-1>", self.cancel_button_pressed)
        cancel_button.bind("<Escape>", self.cancel_button_pressed)

        ok_button = tk.Button(buttons_frame, takefocus=tk.YES, text="OK", height=1, width=6)
        ok_button.pack(expand=tk.NO, side=tk.LEFT, padx='2m', pady='1m', ipady="1m", ipadx="2m")
        ok_button.bind("<Return>", self.ok_button_pressed)
        ok_button.bind("<Button-1>", self.ok_button_pressed)

    def run(self):
        self.box_root.mainloop()
        self.box_root.destroy()

    def stop(self):
        self.box_root.quit()

    def set_msg_area(self, msg):
        self.message_area.delete(1.0, tk.END)
        self.message_area.insert(tk.END, msg)
        num_lines, _ = self.message_area.index(tk.END).split('.')
        self.message_area.configure(height=int(num_lines))
        self.message_area.update()

    def get_text(self):
        return self.text_area.get(1.0, 'end-1c')

    def set_text(self, text):
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, text, "normal")
        self.text_area.focus()

    # Methods executing when a key is pressed
    def x_pressed(self, _):
        self.callback(self, command='x', text=self.get_text())

    def cancel_button_pressed(self, _):
        self.callback(self, command='cancel', text=self.get_text())

    def ok_button_pressed(self, _):
        self.callback(self, command='update', text=self.get_text())

if __name__ == '__main__':
    tb = textbox(msg='example msg', title='example title', text='example text', codebox=False, callback=None, run=True)
