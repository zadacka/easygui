"""

.. moduleauthor:: easygui developers and Stephen Raymond Ferg
.. default-domain:: py
.. highlight:: python

"""
from easygui.boxes.button_box import msgbox
from easygui.boxes.fillable_box import __fillablebox


def convert_to_type(input_value, new_type, input_value_name=None):
    """
    Attempts to convert input_value to type new_type and throws error if it can't.

    If input_value is None, None is returned
    If new_type is None, input_value is returned unchanged
    :param input_value: Value to be converted
    :param new_type: Type to convert to
    :param input_value_name: If not None, used in error message if input_value cannot be converted
    :return: input_value converted to new_type, or None
    """
    if input_value is None or new_type is None:
        return input_value

    exception_string = (
        'value {0}:{1} must be of type {2}.')
    ret_value = new_type(input_value)
#        except ValueError:
#            raise ValueError(
#                exception_string.format('default', default, type(default)))
    return ret_value


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
    default = convert_to_type(default, int, "default")
    lowerbound = convert_to_type(lowerbound, int, "lowerbound")
    upperbound = convert_to_type(upperbound, int, "upperbound")

    while True:
        reply = enterbox(msg, title, default, image=image, root=root)
        if reply is None:
            return None
        try:
            reply = convert_to_type(reply, int)
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
