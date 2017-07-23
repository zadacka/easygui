"""

.. moduleauthor:: easygui developers and Stephen Raymond Ferg
.. default-domain:: py
.. highlight:: python

Version |release|

ABOUT EASYGUI
=============

EasyGui provides an easy-to-use interface for simple GUI interaction
with a user.  It does not require the programmer to know anything about
tkinter, frames, widgets, callbacks or lambda.  All GUI interactions are
invoked by simple function calls that return results.

.. warning:: Using EasyGui with IDLE

    You may encounter problems using IDLE to run programs that use EasyGui. Try it
    and find out.  EasyGui is a collection of Tkinter routines that run their own
    event loops.  IDLE is also a Tkinter application, with its own event loop.  The
    two may conflict, with unpredictable results. If you find that you have
    problems, try running your EasyGui program outside of IDLE.

.. note:: EasyGui requires Tk release 8.0 or greater.

API
===
"""


if __name__ == '__main__':
    from boxes.demo import easygui_demo
    easygui_demo()

    # from boxes.alt_text_box import demo_textbox
    # demo_textbox()
