from easygui.boxes import utils, get_width_and_padding

try:
    import tkinter as tk  # python 3
except ImportError:
    import Tkinter as tk  # python 2


def buttonbox(msg="", title=" ", choices=("Button[1]", "Button[2]", "Button[3]"),
              image=None, images=None, default_choice=None, cancel_choice=None,
              callback=None, run=True):

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


class ButtonBox(object):
    def __init__(self, msg, title, choices, images, default_choice, cancel_choice, callback):
        self._user_specified_callback = callback
        self._text_to_return_on_cancel = cancel_choice

        self.choice_text = None

        self._images = []
        self._buttons = []

        self.box_root = self._configure_box_root(title)
        self.message_area = self._configure_message_area(box_root=self.box_root)
        self._set_msg_area('' if msg is None else msg)
        self.images_frame = self._create_images_frame(images)
        self.buttons_frame = self._create_buttons_frame(choices, default_choice)

    def _configure_box_root(self, title):
        box_root = tk.Tk()
        box_root.title(title)
        box_root.iconname('Dialog')
        box_root.geometry('600x400+100+100')
        # TODO: find out why using GLOBAL_WINDOW_POSITION results in flicker
        box_root.protocol('WM_DELETE_WINDOW', self._x_pressed)  # Quit when x button pressed
        box_root.bind("<Escape>", self._cancel_button_pressed)
        return box_root

    @staticmethod
    def _configure_message_area(box_root):
        padding, width_in_chars = get_width_and_padding(monospace=False)
        message_frame = tk.Frame(box_root, padx=padding)
        message_frame.grid()
        message_area = tk.Text(master=message_frame, width=width_in_chars,
                               padx=padding, pady=padding, wrap=tk.WORD)
        message_area.grid()
        return message_area

    def _set_msg_area(self, msg):
        self.message_area.delete(1.0, tk.END)
        self.message_area.insert(tk.END, msg)
        num_lines, _ = self.message_area.index(tk.END).split('.')
        self.message_area.configure(height=int(num_lines))
        self.message_area.update()

    @staticmethod
    def _convert_to_a_list_of_lists(filenames):
        """ return a list of lists, handling all of the different allowed types of 'filenames' input """
        if type(filenames) is str:
            return [[filenames, ], ]
        elif type(filenames[0]) is str:
            return [filenames, ]
        elif type(filenames[0][0]) is str:
            return filenames
        raise ValueError("Incorrect images argument.")

    def _create_images_frame(self, filenames):
        images_frame = tk.Frame(self.box_root)
        row = 1
        images_frame.grid(row=row)
        self.box_root.rowconfigure(row, weight=10, minsize='10m')

        if filenames is None:
            return

        filename_array = self._convert_to_a_list_of_lists(filenames)
        for row, list_of_filenames in enumerate(filename_array):
            for column, filename in enumerate(list_of_filenames):
                tk_image = utils.load_tk_image(filename, tk_master=images_frame)
                widget = tk.Button(
                    master=images_frame,
                    takefocus=1,
                    compound=tk.TOP,
                    image=tk_image,
                    command=lambda text=filename: self._button_pressed(text)
                )
                widget.grid(row=row, column=column, sticky=tk.NSEW, padx='1m', pady='1m', ipadx='2m', ipady='1m')

                image = {'tk_image': tk_image, 'widget': widget}
                images_frame.rowconfigure(row, weight=10, minsize='10m')
                images_frame.columnconfigure(column, weight=10)
                self._images.append(image)  # Prevent image deletion by keeping them on self
        return images_frame

    def _create_buttons_frame(self, choices, default_choice):
        buttons_frame = tk.Frame(self.box_root)
        buttons_frame.grid(row=2)

        for column, button_text in enumerate(choices):
            clean_text, hotkey, hotkey_position = utils.parse_hotkey(button_text)
            widget = tk.Button(
                master=buttons_frame,
                takefocus=1,
                text=clean_text,
                underline=hotkey_position,
                command=lambda text=button_text: self._button_pressed(text)
            )
            widget.grid(row=0, column=column, padx='1m', pady='1m', ipadx='2m', ipady='1m')
            button = {
                'original_text': button_text,
                'clean_text': clean_text,
                'hotkey': hotkey,
                'widget': widget
            }
            buttons_frame.columnconfigure(column, weight=10)
            self._buttons.append(button)

            for button in self._buttons:
                if button['original_text'] == default_choice:
                    button['widget'].focus_force()

                if button['hotkey'] is not None:
                    self.box_root.bind_all(button['hotkey'], lambda e: self._hotkey_pressed(e), add=True)

        return buttons_frame

    def _callback(self, command):
        if command == 'update':  # OK was pressed
            if self._user_specified_callback:
                # If a callback was set, call main process
                self._user_specified_callback()
            else:
                self.stop()
        elif command in ('x', 'cancel'):
            self.stop()

    def run(self):
        self.box_root.mainloop()
        self.box_root.destroy()
        return self.choice_text

    def stop(self):
        self.box_root.quit()

    # Methods executing when a key is pressed
    def _x_pressed(self):
        self._callback(command='x')
        self.choice_text = self._text_to_return_on_cancel

    def _cancel_button_pressed(self, _):
        self._callback(command='cancel')
        self.choice_text = self._text_to_return_on_cancel

    def _button_pressed(self, button_text):
        self._callback(command='update')
        self.choice_text = button_text

    def _hotkey_pressed(self, event=None):
        """ Handle an event that is generated by a person interacting with a button """
        if event.keysym != event.char:  # A special character
            hotkey_pressed = '<{}>'.format(event.keysym)
        else:
            hotkey_pressed = event.keysym

        for button in self._buttons:
            if button['hotkey'] == hotkey_pressed:
                self._callback(command='update')
                self.choice_text = button['original_text']

        return  # some key was pressed, but no hotkey registered to it
