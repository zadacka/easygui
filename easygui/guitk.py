import Tkinter as tk
import tkFont as tk_Font

from boxes import global_state


class GUItk(object):

    """ This is the object that contains the tk root object"""

    def __init__(self, msg, title, text, codebox, callback):
        """ Create ui object

        Parameters
        ----------
        msg : string
            text displayed in the message area (instructions...)
        title : str
            the window title
        text: str, list or tuple
            text displayed in textAres (editable)
        codebox: bool
            if True, don't wrap, and width is set to 80 chars
        callback: function
            if set, this function will be called when OK is pressed

        Returns
        -------
        object
            The ui object
        """

        self.callback = callback

        self.boxRoot = tk.Tk()
        # self.boxFont = tk_Font.Font(
        #     family=global_state.PROPORTIONAL_FONT_FAMILY,
        #     size=global_state.PROPORTIONAL_FONT_SIZE)

        wrap_text = not codebox
        if wrap_text:
            self.boxFont = tk_Font.nametofont("TkTextFont")
            self.width_in_chars = global_state.prop_font_line_length
        else:
            self.boxFont = tk_Font.nametofont("TkFixedFont")
            self.width_in_chars = global_state.fixw_font_line_length

        # default_font.configure(size=global_state.PROPORTIONAL_FONT_SIZE)

        self.configure_root(title)

        self.create_msg_widget(msg)

        self.create_text_area(wrap_text)

        self.create_buttons_frame()

        self.create_cancel_button()

        self.create_ok_button()

    # Run and stop methods ---------------------------------------

    def run(self):
        self.boxRoot.mainloop()
        self.boxRoot.destroy()

    def stop(self):
        # Get the current position before quitting
        self.get_pos()
        self.boxRoot.quit()

    # Methods to change content ---------------------------------------

    def set_msg(self, msg):
        self.messageArea.config(state=tk.NORMAL)
        self.messageArea.delete(1.0, tk.END)
        self.messageArea.insert(tk.END, msg)
        self.messageArea.config(state=tk.DISABLED)
        # Adjust msg height
        self.messageArea.update()
        numlines = self.get_num_lines(self.messageArea)
        self.set_msg_height(numlines)
        self.messageArea.update()

    def set_msg_height(self, numlines):
        self.messageArea.configure(height=numlines)

    def get_num_lines(self, widget):
        end_position = widget.index(tk.END)  # '4.0'
        end_line = end_position.split('.')[0]  # 4
        return int(end_line) + 1  # 5

    def set_text(self, text):
        self.textArea.delete(1.0, tk.END)
        self.textArea.insert(tk.END, text, "normal")
        self.textArea.focus()

    def set_pos(self, pos):
        self.boxRoot.geometry(pos)

    def get_pos(self):
        # The geometry() method sets a size for the window and positions it on
        # the screen. The first two parameters are width and height of
        # the window. The last two parameters are x and y screen coordinates.
        # geometry("250x150+300+300")
        geom = self.boxRoot.geometry()  # "628x672+300+200"
        global_state.window_position = '+' + geom.split('+', 1)[1]

    def get_text(self):
        return self.textArea.get(0.0, 'end-1c')

    # Methods executing when a key is pressed -------------------------------
    def x_pressed(self):
        self.callback(self, command='x', text=self.get_text())

    def cancel_pressed(self, event):
        self.callback(self, command='cancel', text=self.get_text())

    def ok_button_pressed(self, event):
        self.callback(self, command='update', text=self.get_text())

    # Auxiliary methods -----------------------------------------------
    def calc_character_width(self):
        char_width = self.boxFont.measure('W')
        return char_width

    # Initial configuration methods ---------------------------------------
    # These ones are just called once, at setting.

    def configure_root(self, title):

        self.boxRoot.title(title)

        self.set_pos(global_state.window_position)

        # Quit when x button pressed
        self.boxRoot.protocol('WM_DELETE_WINDOW', self.x_pressed)
        self.boxRoot.bind("<Escape>", self.cancel_pressed)

        self.boxRoot.iconname('Dialog')

    def create_msg_widget(self, msg):

        if msg is None:
            msg = ""

        self.msgFrame = tk.Frame(
            self.boxRoot,
            padx=2 * self.calc_character_width(),

        )
        self.messageArea = tk.Text(
            self.msgFrame,
            width=self.width_in_chars,
            state=tk.DISABLED,
            padx=(global_state.default_hpad_in_chars) *
            self.calc_character_width(),
            pady=global_state.default_hpad_in_chars *
            self.calc_character_width(),
            wrap=tk.WORD,

        )
        self.set_msg(msg)

        self.msgFrame.pack(side=tk.TOP, expand=1, fill='both')

        self.messageArea.pack(side=tk.TOP, expand=1, fill='both')

    def create_text_area(self, wrap_text):
        """
        Put a textArea in the top frame
        Put and configure scrollbars
        """

        self.textFrame = tk.Frame(
            self.boxRoot,
            padx=2 * self.calc_character_width(),
        )

        self.textFrame.pack(side=tk.TOP)
        # self.textFrame.grid(row=1, column=0, sticky=tk.EW)

        self.textArea = tk.Text(
            self.textFrame,
            padx=global_state.default_hpad_in_chars *
            self.calc_character_width(),
            pady=global_state.default_hpad_in_chars *
            self.calc_character_width(),
            height=25,  # lines
            width=self.width_in_chars,   # chars of the current font
        )

        if wrap_text:
            self.textArea.configure(wrap=tk.WORD)
        else:
            self.textArea.configure(wrap=tk.NONE)

        # some simple keybindings for scrolling
        self.boxRoot.bind("<Next>", self.textArea.yview_scroll(1, tk.PAGES))
        self.boxRoot.bind(
            "<Prior>", self.textArea.yview_scroll(-1, tk.PAGES))

        self.boxRoot.bind("<Right>", self.textArea.xview_scroll(1, tk.PAGES))
        self.boxRoot.bind("<Left>", self.textArea.xview_scroll(-1, tk.PAGES))

        self.boxRoot.bind("<Down>", self.textArea.yview_scroll(1, tk.UNITS))
        self.boxRoot.bind("<Up>", self.textArea.yview_scroll(-1, tk.UNITS))

        # add a vertical scrollbar to the frame
        rightScrollbar = tk.Scrollbar(
            self.textFrame, orient=tk.VERTICAL, command=self.textArea.yview)
        self.textArea.configure(yscrollcommand=rightScrollbar.set)

        # add a horizontal scrollbar to the frame
        bottomScrollbar = tk.Scrollbar(
            self.textFrame, orient=tk.HORIZONTAL, command=self.textArea.xview)
        self.textArea.configure(xscrollcommand=bottomScrollbar.set)

        # pack the textArea and the scrollbars.  Note that although
        # we must define the textArea first, we must pack it last,
        # so that the bottomScrollbar will be located properly.

        # Note that we need a bottom scrollbar only for code.
        # Text will be displayed with wordwrap, so we don't need to have
        # a horizontal scroll for it.

        if not wrap_text:
            bottomScrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        rightScrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.textArea.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)

    def create_buttons_frame(self):

        self.buttonsFrame = tk.Frame(self.boxRoot,
                                     # background="green",

                                     )
        self.buttonsFrame.pack(side=tk.TOP)

    def create_cancel_button(self):
        # put the buttons in the buttonsFrame
        self.cancelButton = tk.Button(
            self.buttonsFrame, takefocus=tk.YES, text="Cancel",
            height=1, width=6)
        self.cancelButton.pack(
            expand=tk.NO, side=tk.LEFT, padx='2m', pady='1m', ipady="1m",
            ipadx="2m")

        # for the commandButton, bind activation events to the activation event
        # handler
        self.cancelButton.bind("<Return>", self.cancel_pressed)
        self.cancelButton.bind("<Button-1>", self.cancel_pressed)
        self.cancelButton.bind("<Escape>", self.cancel_pressed)

    def create_ok_button(self):
        # put the buttons in the buttonsFrame
        self.okButton = tk.Button(
            self.buttonsFrame, takefocus=tk.YES, text="OK", height=1, width=6)
        self.okButton.pack(
            expand=tk.NO, side=tk.LEFT, padx='2m', pady='1m', ipady="1m",
            ipadx="2m")

        # for the commandButton, bind activation events to the activation event
        # handler
        self.okButton.bind("<Return>", self.ok_button_pressed)
        self.okButton.bind("<Button-1>", self.ok_button_pressed)