import Tkinter as tk
import tkFont as tk_Font

import easygui.boxes
from easygui.boxes import to_string


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
        self.ui.set_msg_area(self._msg)

    @msg.deleter
    def msg(self):
        self._msg = ""
        self.ui.set_msg_area(self._msg)


class GUItk(object):
    def __init__(self, msg, title, text, code_box, callback):
        self.callback = callback

        self.boxRoot = tk.Tk()

        if code_box:
            self.boxFont = tk_Font.nametofont("TkFixedFont")
            self.width_in_chars = easygui.boxes.fixw_font_line_length
        else:
            self.boxFont = tk_Font.nametofont("TkTextFont")
            self.width_in_chars = easygui.boxes.prop_font_line_length

        # configure root
        self.boxRoot.title(title)
        self.boxRoot.iconname('Dialog')
        self.boxRoot.geometry(easygui.boxes.window_position)

        # Quit when x button pressed
        self.boxRoot.protocol('WM_DELETE_WINDOW', self.x_pressed)
        self.boxRoot.bind("<Escape>", self.cancel_pressed)

        self.msgFrame = tk.Frame(self.boxRoot, padx=2 * self.boxFont.measure('W'),)
        self.msgFrame.pack(side=tk.TOP, expand=1, fill='both')

        self.messageArea = tk.Text(
            self.msgFrame,
            width=self.width_in_chars,
            state=tk.DISABLED,
            padx=easygui.boxes.default_hpad_in_chars * self.boxFont.measure('W'),
            pady=easygui.boxes.default_hpad_in_chars * self.boxFont.measure('W'),
            wrap=tk.WORD,)
        self.set_msg_area("" if msg is None else msg)
        self.messageArea.pack(side=tk.TOP, expand=1, fill='both')

        self.textFrame = tk.Frame(self.boxRoot, padx=2 * self.boxFont.measure('W'),)
        self.textFrame.pack(side=tk.TOP)

        self.textArea = tk.Text(self.textFrame,
                                padx=easygui.boxes.default_hpad_in_chars * self.boxFont.measure('W'),
                                pady=easygui.boxes.default_hpad_in_chars * self.boxFont.measure('W'),
                                height=25,  # lines
                                width=self.width_in_chars,  # chars of the current font
                                )

        self.textArea.configure(wrap=tk.NONE if code_box else tk.WORD)

        # some simple keybindings for scrolling
        self.boxRoot.bind("<Next>", self.textArea.yview_scroll(1, tk.PAGES))
        self.boxRoot.bind("<Prior>", self.textArea.yview_scroll(-1, tk.PAGES))

        self.boxRoot.bind("<Right>", self.textArea.xview_scroll(1, tk.PAGES))
        self.boxRoot.bind("<Left>", self.textArea.xview_scroll(-1, tk.PAGES))

        self.boxRoot.bind("<Down>", self.textArea.yview_scroll(1, tk.UNITS))
        self.boxRoot.bind("<Up>", self.textArea.yview_scroll(-1, tk.UNITS))

        vertical_scrollbar = tk.Scrollbar(self.textFrame, orient=tk.VERTICAL, command=self.textArea.yview)
        self.textArea.configure(yscrollcommand=vertical_scrollbar.set)

        horizontal_scrollbar = tk.Scrollbar(self.textFrame, orient=tk.HORIZONTAL, command=self.textArea.xview)
        self.textArea.configure(xscrollcommand=horizontal_scrollbar.set)

        if code_box:
            # no word-wrapping for code so we need a horizontal scroll bar
            horizontal_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        vertical_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # pack textArea last so bottom scrollbar displays properly
        self.textArea.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)
        
        self.set_text(text)
        self.buttonsFrame = tk.Frame(self.boxRoot)
        self.buttonsFrame.pack(side=tk.TOP)
        
        # put the buttons in the buttonsFrame
        self.cancelButton = tk.Button(self.buttonsFrame, takefocus=tk.YES, text="Cancel", height=1, width=6)
        self.cancelButton.pack(expand=tk.NO, side=tk.LEFT, padx='2m', pady='1m', ipady="1m", ipadx="2m")

        # for the commandButton, bind activation events to the activation event handler
        self.cancelButton.bind("<Return>", self.cancel_pressed)
        self.cancelButton.bind("<Button-1>", self.cancel_pressed)
        self.cancelButton.bind("<Escape>", self.cancel_pressed)

        self.okButton = tk.Button(
            self.buttonsFrame, takefocus=tk.YES, text="OK", height=1, width=6)
        self.okButton.pack(
            expand=tk.NO, side=tk.LEFT, padx='2m', pady='1m', ipady="1m",
            ipadx="2m")

        # for the commandButton, bind activation events to the activation event handler
        self.okButton.bind("<Return>", self.ok_button_pressed)
        self.okButton.bind("<Button-1>", self.ok_button_pressed)

    def run(self):
        self.boxRoot.mainloop()
        self.boxRoot.destroy()

    def stop(self):
        self.get_pos()
        self.boxRoot.quit()

    def set_msg_area(self, msg):
        self.messageArea.config(state=tk.NORMAL)
        self.messageArea.delete(1.0, tk.END)
        self.messageArea.insert(tk.END, msg)
        self.messageArea.config(state=tk.DISABLED)
        # Adjust msg height
        self.messageArea.update()
        numlines = self.get_num_lines(self.messageArea)
        self.messageArea.configure(height=numlines)
        self.messageArea.update()

    def get_num_lines(self, widget):
        end_position = widget.index(tk.END)  # '4.0'
        end_line = end_position.split('.')[0]  # 4
        return int(end_line) + 1  # 5

    def get_text(self):
        return self.textArea.get(0.0, 'end-1c')

    def set_text(self, text):
        self.textArea.delete(1.0, tk.END)
        self.textArea.insert(tk.END, text, "normal")
        self.textArea.focus()

    def get_pos(self):
        # The geometry() method sets a size for the window and positions it on
        # the screen. The first two parameters are width and height of
        # the window. The last two parameters are x and y screen coordinates.
        # geometry("250x150+300+300")
        # TODO: Fix so that get_post does not set a global value!!
        geom = self.boxRoot.geometry()  # "628x672+300+200"
        easygui.boxes.window_position = '+' + geom.split('+', 1)[1]

    # Methods executing when a key is pressed -------------------------------
    def x_pressed(self, event):
        self.callback(self, command='x', text=self.get_text())

    def cancel_pressed(self, event):
        self.callback(self, command='cancel', text=self.get_text())

    def ok_button_pressed(self, event):
        self.callback(self, command='update', text=self.get_text())
