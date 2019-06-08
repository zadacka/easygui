"""

.. moduleauthor:: easygui developers and Stephen Raymond Ferg
.. default-domain:: py
.. highlight:: python

"""
from easygui.boxes.button_box import msgbox
from easygui.boxes.fillable_box import __fillablebox


# -------------------------------------------------------------------
# integerbox
# -------------------------------------------------------------------
def integerbox(msg="", title=" ", default=None,
               lowerbound=0, upperbound=99, image=None, root=None):
    """
    Show a box in which a user can enter an integer.

    In addition to arguments for msg and title, this function accepts
    integer arguments for "default", "lowerbound", and "upperbound".

    The default, lowerbound, or upperbound may be None.

    When the user enters some text, the text is checked to verify that it
    can be converted to an integer between the lowerbound and upperbound.

    If it can be, the integer (not the text) is returned.

    If it cannot, then an error msg is displayed, and the integerbox is
    redisplayed.

    If the user cancels the operation, None is returned.

    :param str msg: the msg to be displayed
    :param str title: the window title
    :param int default: The default value to return
    :param int lowerbound: The lower-most value allowed
    :param int upperbound: The upper-most value allowed
    :param str image: Filename of image to display
    :param tk_widget root: Top-level Tk widget
    :return: the integer value entered by the user

    """

    if not msg:
        msg = "Enter an integer between {0} and {1}".format(
            lowerbound, upperbound)

    # Validate the arguments for default, lowerbound and upperbound and
    # convert to integers
    default = None if default is None else int(default)
    lowerbound = None if lowerbound is None else int(lowerbound)
    upperbound = None if upperbound is None else int(upperbound)

    while True:
        reply = enterbox(msg, title, default, image=image, root=root)
        if reply is None:
            return None
        try:
            reply = int(reply)
        except ValueError:
            msgbox('The value that you entered:\n\t"{}"\nis not an integer.'.format(reply), "Error")
            continue
        if lowerbound is not None:
            if reply < lowerbound:
                msgbox('The value that you entered is less than the lower bound of {}.'.format(lowerbound), "Error")
                continue
        if upperbound is not None:
            if reply > upperbound:
                msgbox('The value that you entered is greater than the upper bound of {}.'.format(upperbound), "Error")
                continue
        # reply has passed all validation checks.
        # It is an integer between the specified bounds.
        break
    return reply







# -------------------------------------------------------------------
# enterbox
# -------------------------------------------------------------------
def enterbox(msg="Enter something.", title=" ", default="",
             strip=True, image=None, root=None):
    """
    Show a box in which a user can enter some text.

    You may optionally specify some default text, which will appear in the
    enterbox when it is displayed.

    Example::

        reply = enterbox(....)
        if reply:
            ...
        else:
            ...

    :param str msg: the msg to be displayed.
    :param str title: the window title
    :param str default: value returned if user does not change it
    :param bool strip: If True, the return value will have
      its whitespace stripped before being returned
    :return: the text that the user entered, or None if he cancels
      the operation.
    """
    result = __fillablebox(
        msg, title, default=default, mask=None, image=image, root=root)
    if result and strip:
        result = result.strip()
    return result


def passwordbox(msg="Enter your password.", title=" ", default="",
                image=None, root=None):
    """
    Show a box in which a user can enter a password.
    The text is masked with asterisks, so the password is not displayed.

    :param str msg: the msg to be displayed.
    :param str title: the window title
    :param str default: value returned if user does not change it
    :return: the text that the user entered, or None if he cancels
      the operation.
    """
    return __fillablebox(msg, title, default, mask="*",
                         image=image, root=root)
