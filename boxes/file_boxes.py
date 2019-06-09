from os.path import normpath

from boxes import tk_FileDialog


def diropenbox(title='Open', default_directory=None):
    """ A dialog to get a directory name. Returns the name of a directory, or None if user chose to cancel """
    directory_path = tk_FileDialog.askdirectory(title=title, initialdir=default_directory)
    return None if directory_path is None else normpath(directory_path)


def filesavebox(title='Save As', default_directory="", filetypes=None):
    """A dialog box to get the name of a file. Return the name of a file, or None if user chose to cancel """
    file_path = tk_FileDialog.asksaveasfilename(title=title, initialdir=default_directory, filetypes=filetypes)
    return None if file_path is None else normpath(file_path)


def fileopenbox(title='Open', default_directory='*', filetypes=None, multiple=False):
    """ A dialog to get a file name.
    fileopenbox automatically changes the path separator to backslash on Windows.

    :param str title: the window title
    :param str default_directory: filepath to search, may contain wildcards, defaults to all files in current directory
    :param object filetypes: a file pattern OR a list of file patterns and a file type description
                            eg. ["*.css", ["*.htm", "*.html", "HTML files"]  ]
                            If the filetypes list does not contain ("All files","*"), it will be added.
    :param bool multiple: allow selection of more than one file
    :return: the name of a file, or None if user chose to cancel
    """
    kwargs = dict(title=title, initialdir=default_directory, filetypes=filetypes)

    if multiple:
        filenames = tk_FileDialog.askopenfilenames(kwargs)
        return None if filenames is None else [normpath(x) for x in filenames]

    else:
        filename = tk_FileDialog.askopenfilename(kwargs)
        return None if filename is None else normpath(filename)
