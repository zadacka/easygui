import easygui.boxes
from easygui.boxes.button_box import msgbox
from easygui.boxes import bindArrows, GLOBAL_WINDOW_POSITION, STANDARD_SELECTION_EVENTS, \
    TEXT_ENTRY_FONT_SIZE, PROPORTIONAL_FONT_FAMILY, PROPORTIONAL_FONT_SIZE

try:
    import tkinter as tk  # python 3
    import tkinter.font as tk_Font
except:
    import Tkinter as tk  # python 2
    import tkFont as tk_Font


def integerbox(msg=None, title=" ", default=None, lowerbound=0, upperbound=99, image=None, root=None):
    """
    Show a box into which a user can enter an integer.
    Validate with respect to the upper/lower bounds if supplied.
    Notify and get user to re-try input if validation fails.
    :return: the integer value input or None if the user cancels the operation
    """
    msg = "Enter an integer between {0} and {1}".format(lowerbound, upperbound) if msg is None else msg

    while True:
        result = FillableBox(msg, title, default, image=image, root=root).run()
        if result is None:
            return None

        try:
            result = int(result)
        except ValueError:
            msgbox('The value that you entered:\n\t"{}"\nis not an integer.'.format(result), "Error")
            continue

        if lowerbound and result < int(lowerbound):
            msgbox('The value that you entered is less than the lower bound of {}.'.format(lowerbound), "Error")
        elif upperbound and result > int(upperbound):
            msgbox('The value that you entered is greater than the upper bound of {}.'.format(upperbound), "Error")
        else:
            return result  # validation passed!


def enterbox(msg="Enter something.", title=" ", default="", strip=True, image=None, root=None):
    """Show a box in which a user can enter some text. """
    result = FillableBox(msg, title, default, image=image, root=root).run()
    if result and strip:
        result = result.strip()
    return result


def passwordbox(msg="Enter your password.", title=" ", default="", image=None, root=None):
    """ Show a box in which a user can enter a password. Mask the password with asterisks so it is hidden. """
    return FillableBox(msg, title, default, mask="*", image=image, root=root).run()


def fillablebox(msg, title="", default=None, mask=None, image=None, root=None):
    """
    Show a box in which a user can enter some text.
    :param str msg: the msg to be displayed.
    :param str title: the window title
    :param str default: default value populated, returned if user does not change it
    :return: the text that the user entered, or None if he cancels the operation.
    """
    return FillableBox(msg, title, default, mask, image, root).run()


class FillableBox(object):
    def __init__(self, msg, default, title, mask=None, image=None, root=None):
        self.return_value = '' if default is None else default
        self.pre_existing_root = root
        self.box_root = None
        self.entry_widget = None

        if root:
            root.withdraw()
            self.box_root = tk.Toplevel(master=root)
            self.box_root.withdraw()
        else:
            self.box_root = tk.Tk()
            self.box_root.withdraw()

        self.box_root.protocol('WM_DELETE_WINDOW', self._set_result_to_none_and_quit)
        self.box_root.title(title)
        self.box_root.iconname('Dialog')
        self.box_root.geometry(GLOBAL_WINDOW_POSITION)
        self.box_root.bind("<Escape>", self._set_result_to_none_and_quit)

        message_frame = tk.Frame(master=self.box_root)
        message_frame.pack(side=tk.TOP, fill=tk.BOTH)

        try:
            tk_image = easygui.boxes.load_tk_image(image)
        except Exception as inst:
            print(inst)
            tk_image = None
        if tk_image:
            image_frame = tk.Frame(master=self.box_root)
            image_frame.pack(side=tk.TOP, fill=tk.BOTH)
            label = tk.Label(image_frame, image=tk_image)
            label.image = tk_image  # keep a reference!
            label.pack(side=tk.TOP, expand=tk.YES, fill=tk.X, padx='1m', pady='1m')

        buttons_frame = tk.Frame(master=self.box_root)
        buttons_frame.pack(side=tk.TOP, fill=tk.BOTH)

        entry_frame = tk.Frame(master=self.box_root)
        entry_frame.pack(side=tk.TOP, fill=tk.BOTH)

        buttons_frame = tk.Frame(master=self.box_root)
        buttons_frame.pack(side=tk.TOP, fill=tk.BOTH)

        message_widget = tk.Message(message_frame, width="4.5i", text=msg)
        message_widget.configure(font=(PROPORTIONAL_FONT_FAMILY, PROPORTIONAL_FONT_SIZE))
        message_widget.pack(side=tk.RIGHT, expand=1, fill=tk.BOTH, padx='3m', pady='3m')

        entry_widget = tk.Entry(entry_frame, width=40)
        bindArrows(entry_widget)
        entry_widget.configure(font=(PROPORTIONAL_FONT_FAMILY, TEXT_ENTRY_FONT_SIZE))
        if mask:
            entry_widget.configure(show=mask)
        entry_widget.pack(side=tk.LEFT, padx="3m")
        entry_widget.bind("<Return>", self._set_result_to_entered_text_and_quit)
        entry_widget.bind("<Escape>", self._set_result_to_none_and_quit)
        entry_widget.insert(0, self.return_value)  # put text into the entry_widget
        self.entry_widget = entry_widget  # save a reference - we need to get text from this widget later

        ok_button = tk.Button(buttons_frame, takefocus=1, text="OK")
        bindArrows(ok_button)
        ok_button.pack(expand=1, side=tk.LEFT, padx='3m', pady='3m', ipadx='2m', ipady='1m')
        for selectionEvent in STANDARD_SELECTION_EVENTS:
            ok_button.bind("<{}>".format(selectionEvent), self._set_result_to_entered_text_and_quit)

        cancel_button = tk.Button(buttons_frame, takefocus=1, text="Cancel")
        bindArrows(cancel_button)
        cancel_button.pack(expand=1, side=tk.RIGHT, padx='3m', pady='3m', ipadx='2m', ipady='1m')
        for selectionEvent in STANDARD_SELECTION_EVENTS:
            cancel_button.bind("<{}>".format(selectionEvent), self._set_result_to_none_and_quit)

        self.entry_widget.focus_force()  # put the focus on the self.entry_widget
        self.box_root.deiconify()

    def _set_result_to_none_and_quit(self, *args):
        self.return_value = None
        self.box_root.quit()

    def _set_result_to_entered_text_and_quit(self, *args):
        self.return_value = self.entry_widget.get()
        self.box_root.quit()

    def run(self):
        self.box_root.mainloop()  # run it!

        # -------- after the run has completed ----------------------------------
        if self.pre_existing_root:
            self.pre_existing_root.deiconify()
        self.box_root.destroy()  # button_click didn't destroy self.boxRoot, so we do it now
        return self.return_value
