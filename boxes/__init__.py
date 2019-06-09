import os
import sys

if not 0x020700F0 <= sys.hexversion <= 0x030000F0 and not 0x030400F0 <= sys.hexversion <= 0x040000F0:
    raise Exception("You must run on Python 2.7+ or Python 3.4+")

try:
    import tkinter as tk  # python 3
    import tkinter.filedialog as tk_FileDialog
    import tkinter.font as tk_Font
except ImportError:
    import Tkinter as tk  # python 2
    import tkFileDialog as tk_FileDialog
    import tkFont as tk_Font

if tk.TkVersion < 8.0:
    raise ImportError("You must use python-tk (tkinter) version 8.0 or higher")


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


def load_tk_image(filename, tk_master=None):
    """
    Load in an image file and return as a tk Image.

    Loads an image.  If the PIL library is available use it.  otherwise use the tk method.

    NOTE: tk_master is required if there are more than one Tk() instances, which there are very often.
      REF: http://stackoverflow.com/a/23229091/2184122

    :param filename: image filename to load
    :param tk_master: root object (Tk())
    :return: tk Image object
    """
    try:
        # Try to import the Python Image Library.  If it doesn't exist, only .gif images are supported.
        from PIL import Image as PILImage
        from PIL import ImageTk as PILImageTk
    except ImportError:
        pass

    if filename is None:
        return None

    if not os.path.isfile(filename):
        raise ValueError(
            'Image file {} does not exist.'.format(filename))

    filename = os.path.normpath(filename)
    _, ext = os.path.splitext(filename)

    try:
        pil_image = PILImage.open(filename)
        tk_image = PILImageTk.PhotoImage(pil_image, master=tk_master)
    except:
        try:
            # Fallback if PIL isn't available
            tk_image = tk.PhotoImage(file=filename, master=tk_master)
        except:
            msg = "Cannot load {}.  Check to make sure it is an image file.".format(
                filename)
            try:
                _ = PILImage
            except:
                msg += "\nPIL library isn't installed.  If it isn't installed, only .gif files can be used."
            raise ValueError(msg)
    return tk_image
