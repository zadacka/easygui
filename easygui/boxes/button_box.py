import re

import easygui.boxes
from easygui.boxes import utils as ut
from easygui.boxes.base_box import BaseBox

try:
    import tkinter as tk  # python 3
    import tkinter.font as tk_Font
except (SystemError, ValueError, ImportError):
    import Tkinter as tk  # python 2
    import tkFont as tk_Font

# REF: http://stackoverflow.com/questions/1835018/python-check-if-an-object-is-a-list-or-tuple-but-not-string
def is_sequence(arg):
    return hasattr(arg, "__getitem__") or hasattr(arg, "__iter__")

def is_string(arg):
    ret_val = None
    try:
        ret_val = isinstance(arg, basestring) #Python 2
    except:
        ret_val = isinstance(arg, str) #Python 3
    return ret_val


def buttonbox(msg="", title=" ", choices=("Button[1]", "Button[2]", "Button[3]"),
              image=None, images=None, default_choice=None, cancel_choice=None,
              callback=None, run=True):

    # TODO: add deprecation warning for
    # * the handling of 'image' and 'images' ... confusing to have multiple, simplify down to one
    # * the function call should always run the method... if you just want an instance, use the constructor
    if image and images:
        raise ValueError("Specify 'images' parameter only for buttonbox.")
    if image:
        images = image
    bb = ButtonBox(
        msg=msg,
        title=title,
        choices=choices,
        images=images,
        default_choice=default_choice,
        cancel_choice=cancel_choice,
        callback=callback)
    if not run:
        return bb
    else:
        reply = bb.run()
        return reply


class ButtonBox(BaseBox):

    def __init__(self, msg, title, choices, images, default_choice, cancel_choice, callback):
        self.callback = callback
        self.ui = GUItk(msg, title, choices, images, default_choice, cancel_choice, self.callback_ui)

    def callback_ui(self, ui, command):
        """ This method is executed when buttons or x is pressed in the ui.
        """
        if command == 'update':  # Any button was pressed
            self._text = ui.choice
            self._choice_rc = ui.choice_rc
            if self.callback:
                # If a callback was set, call main process
                self.callback(self)
            else:
                self.stop()
        elif command in ('x', 'cancel'):
            self.stop()
            self._text = None

    @property
    def choice(self):
        """ Name of button selected """
        return self._text

    @property
    def choice_rc(self):
        """ The row/column of the selected button (as a tuple) """
        return self._choice_rc


class GUItk(object):
    """ This is the object that contains the tk root object"""

    def __init__(self, msg, title, choices, images, default_choice, cancel_choice, callback):
        """ Create ui object

        Parameters
        ----------
        msg : string
            text displayed in the message area (instructions...)
        title : str
            the window title
        choices : iterable of strings
            build a button for each string in choices
        images : iterable of filenames, or an iterable of iterables of filenames
            displays each image
        default_choice : string
            one of the strings in choices to be the default selection
        cancel_choice : string
            if X or <esc> is pressed, it appears as if this button was pressed.
        callback: function
            if set, this function will be called when any button is pressed.

        """
        self.callback = callback

        self._title = title
        self._msg = msg
        self._choices = choices
        self._default_choice = default_choice
        self._cancel_choice = cancel_choice
        self._choice_text = None
        self._choice_rc = None
        self._images = list()

        self.boxRoot = tk.Tk()
        # self.boxFont = tk_Font.Font(
        #     family=global_state.PROPORTIONAL_FONT_FAMILY,
        #     size=global_state.PROPORTIONAL_FONT_SIZE)

        self.boxFont = tk_Font.nametofont("TkFixedFont")
        self.width_in_chars = easygui.boxes.FIXW_FONT_LINE_LENGTH

        # default_font.configure(size=global_state.PROPORTIONAL_FONT_SIZE)

        self.configure_root(title)

        self.create_msg_widget(msg)

        self.create_images_frame()

        self.create_images(images)

        self.create_buttons_frame()

        self.create_buttons(choices, default_choice)


    @property
    def choice(self):
        return self._choice_text

    @property
    def choice_rc(self):
        return self._choice_rc

    # Run and stop methods ---------------------------------------

    def run(self):
        self.boxRoot.mainloop()
        self.boxRoot.destroy()

    def stop(self):
        # Get the current position before quitting
        #self.get_pos()
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

    def set_pos(self, pos):
        self.boxRoot.geometry(pos)

    def get_pos(self):
        # The geometry() method sets a size for the window and positions it on
        # the screen. The first two parameters are width and height of
        # the window. The last two parameters are x and y screen coordinates.
        # geometry("250x150+300+300")
        geom = self.boxRoot.geometry()  # "628x672+300+200"
        easygui.boxes.GLOBAL_WINDOW_POSITION = '+' + geom.split('+', 1)[1]

    # Methods executing when a key is pressed -------------------------------
    def x_pressed(self):
        self._choice_text = self._cancel_choice
        self.callback(self, command='x')

    def cancel_pressed(self, event):
        self._choice_text = self._cancel_choice
        self.callback(self, command='cancel')

    def button_pressed(self, button_text, button_rc):
        self._choice_text = button_text
        self._choice_rc = button_rc
        self.callback(self, command='update')

    def hotkey_pressed(self, event=None):
        """
        Handle an event that is generated by a person interacting with a button.  It may be a button press
        or a key press.

        TODO: Enhancement: Allow hotkey to be specified in filename of image as a shortcut too!!!
        """

        # Determine window location and save to global
        # TODO: Not sure where this goes, but move it out of here!
        m = re.match("(\d+)x(\d+)([-+]\d+)([-+]\d+)", self.boxRoot.geometry())
        if not m:
            raise ValueError(
                "failed to parse geometry string: {}".format(self.boxRoot.geometry()))
        width, height, xoffset, yoffset = [int(s) for s in m.groups()]
        easygui.boxes.GLOBAL_WINDOW_POSITION = '{0:+g}{1:+g}'.format(xoffset, yoffset)

        # Hotkeys
        if self._buttons:
            for button_name, button in self._buttons.items():
                hotkey_pressed = event.keysym
                if event.keysym != event.char:  # A special character
                    hotkey_pressed = '<{}>'.format(event.keysym)
                if button['hotkey'] == hotkey_pressed:
                    self._choice_text = button_name
                    self.callback(self, command='update')
                    return
        print("Event not understood")

    # Auxiliary methods -----------------------------------------------
    def calc_character_width(self):
        char_width = self.boxFont.measure('W')
        return char_width

    # Initial configuration methods ---------------------------------------
    # These ones are just called once, at setting.

    def configure_root(self, title):
        self.boxRoot.title(title)

        self.set_pos(easygui.boxes.GLOBAL_WINDOW_POSITION)

        # Resize setup
        self.boxRoot.columnconfigure(0, weight=10)
        self.boxRoot.minsize(100, 200)
        # Quit when x button pressed
        self.boxRoot.protocol('WM_DELETE_WINDOW', self.x_pressed)
        self.boxRoot.bind("<Escape>", self.cancel_pressed)
        self.boxRoot.iconname('Dialog')

    def create_msg_widget(self, msg):

        if msg is None:
            msg = ""

        self.messageArea = tk.Text(
            self.boxRoot,
            width=self.width_in_chars,
            state=tk.DISABLED,
            padx=(easygui.boxes.DEFAULT_PADDING) *
                 self.calc_character_width(),
            relief="flat",
            background=self.boxRoot.config()["background"][-1],
            pady=easygui.boxes.DEFAULT_PADDING *
                 self.calc_character_width(),
            wrap=tk.WORD,
        )
        self.set_msg(msg)
        self.messageArea.grid(row=0)
        self.boxRoot.rowconfigure(0, weight=10, minsize='10m')

    def create_images_frame(self):
        self.imagesFrame = tk.Frame(self.boxRoot)
        row = 1
        self.imagesFrame.grid(row=row)
        self.boxRoot.rowconfigure(row, weight=10, minsize='10m')

    def create_images(self, filenames):
        """
        Create one or more images in the dialog.
        :param filenames:
        May be a filename (which will generate a single image), a list of filenames (which will generate
        a row of images), or a list of list of filename (which will create a 2D array of buttons.
        :return:
        """
        if filenames is None:
            return
        # Convert to a list of lists of filenames regardless of input
        if is_string(filenames):
            filenames = [[filenames,],]
        elif is_sequence(filenames) and is_string(filenames[0]):
            filenames = [filenames,]
        elif is_sequence(filenames) and is_sequence(filenames[0]) and is_string(filenames[0][0]):
            pass
        else:
            raise ValueError("Incorrect images argument.")

        images = list()
        for _r, images_row in enumerate(filenames):
            row_number = len(filenames) - _r
            for column_number, filename in enumerate(images_row):
                this_image = dict()
                try:
                    this_image['tk_image'] = ut.load_tk_image(filename)
                except Exception as e:
                    print(e)
                    this_image['tk_image'] = None
                this_image['widget'] = tk.Button(
                    self.imagesFrame,
                    takefocus=1,
                    compound=tk.TOP)
                if this_image['widget'] is not None:
                    this_image['widget'].configure(image=this_image['tk_image'])
                fn = lambda text=filename, row=_r, column=column_number: self.button_pressed(text, (row, column))
                this_image['widget'].configure(command=fn)
                sticky_dir = tk.N+tk.S+tk.E+tk.W
                this_image['widget'].grid(row=row_number, column=column_number, sticky=sticky_dir, padx='1m', pady='1m', ipadx='2m', ipady='1m')
                self.imagesFrame.rowconfigure(row_number, weight=10, minsize='10m')
                self.imagesFrame.columnconfigure(column_number, weight=10)
                images.append(this_image)
        self._images = images  # Image objects must live, so place them in self.  Otherwise, they will be deleted.

    def create_buttons_frame(self):
        self.buttonsFrame = tk.Frame(self.boxRoot)
        self.buttonsFrame.grid(row=2, column=0)

    def create_buttons(self, choices, default_choice):
        unique_choices = ut.uniquify_list_of_strings(choices)
        # Create buttons dictionary and Tkinter widgets
        buttons = dict()
        i_hack = 0
        for row, (button_text, unique_button_text) in enumerate(zip(choices, unique_choices)):
            this_button = dict()
            this_button['original_text'] = button_text
            this_button['clean_text'], this_button['hotkey'], hotkey_position = ut.parse_hotkey(button_text)
            this_button['widget'] = tk.Button(
                    self.buttonsFrame,
                    takefocus=1,
                    text=this_button['clean_text'],
                    underline=hotkey_position)
            fn = lambda text=button_text, row=row, column=0: self.button_pressed(text, (row, column))
            this_button['widget'].configure(command=fn)
            this_button['widget'].grid(row=0, column=i_hack, padx='1m', pady='1m', ipadx='2m', ipady='1m')
            self.buttonsFrame.columnconfigure(i_hack, weight=10)
            i_hack += 1
            buttons[unique_button_text] = this_button
        self._buttons = buttons
        if default_choice in buttons:
            buttons[default_choice]['widget'].focus_force()
        # Bind hotkeys
        for hk in [button['hotkey'] for button in buttons.values() if button['hotkey']]:
            self.boxRoot.bind_all(hk, lambda e: self.hotkey_pressed(e), add=True)
