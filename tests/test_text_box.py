import tkinter as tk
import unittest
from unittest.mock import patch, Mock, ANY

import pytest

from easygui.text_box import TextBox, textbox, codebox
from tests import WAIT_0_MILLISECONDS, WAIT_1_MILLISECONDS

MODBASE = 'easygui.text_box'

TEST_MESSAGE = 'example message'
TEST_TITLE = 'example title'
TEST_TEXT = 'example text'
TEST_MONOSPACE = False
TEST_CALLBACK = Mock()
TEST_ARGS = [TEST_MESSAGE, TEST_TITLE, TEST_TEXT, TEST_MONOSPACE, TEST_CALLBACK]


def test__textbox_method__instantiates_textbox_class_and_runs_it():
    """ Test that the textbox() method calls the underlying TextBox class in the expected way """
    with patch(MODBASE + '.TextBox') as mock_text_box_class:
        mock_text_box_instance = Mock()
        mock_text_box_instance.run = Mock(return_value='return text')
        mock_text_box_class.return_value = mock_text_box_instance

        return_text = textbox(TEST_MESSAGE, TEST_TITLE, TEST_TEXT, TEST_CALLBACK, run=True)

        mock_text_box_class.assert_called_once_with(
            msg=TEST_MESSAGE,
            title=TEST_TITLE,
            text=TEST_TEXT,
            monospace=TEST_MONOSPACE,
            callback=TEST_CALLBACK
        )
        mock_text_box_instance.run.assert_called_once_with()
        assert return_text == 'return text'


@pytest.fixture()
def test_textbox():
    yield TextBox(*TEST_ARGS)


def test_instantiation(test_textbox):
    # Instance attributes should be configured:
    assert test_textbox.text == TEST_TEXT
    assert test_textbox.msg.strip() == TEST_MESSAGE
    assert test_textbox._user_specified_callback == TEST_CALLBACK

    # The following Tk widgets should also have been created:
    assert isinstance(test_textbox.box_root, tk.Tk)
    assert isinstance(test_textbox.msg_widget, tk.Text)
    assert isinstance(test_textbox.text_area, tk.Text)

    # And configured:
    assert test_textbox.msg_widget.get(0.0, 'end-1c') == TEST_MESSAGE
    assert test_textbox.text_area.get(0.0, 'end-1c') == TEST_TEXT


def test_run(test_textbox):
    with unittest.mock.patch.object(test_textbox, 'box_root') as mockroot:
        assert test_textbox.run() is None
        mockroot.mainloop.assert_called_once_with()
        mockroot.destroy.assert_called_once_with()


def test_stop(test_textbox):
    with unittest.mock.patch.object(test_textbox, 'box_root') as mockroot:
        test_textbox.stop()
        mockroot.quit.assert_called_once_with()


def test_set_msg_area(test_textbox):
    new_msg = 'some new text'
    test_textbox.msg = new_msg
    assert test_textbox.msg_widget.get(1.0, 'end-1c') == new_msg


def test_set_text(test_textbox):
    assert test_textbox.text == TEST_TEXT

    new_text = 'some new text'
    test_textbox.text = new_text
    assert test_textbox.text_area.get(1.0, 'end-1c') == new_text


def test_textbox_cancel_button_pressed_results_in_run_returning_None():
    tb = textbox(run=False)

    def simulate_cancel_button_pressed(tb_instance):
        tb_instance.cancel_button_pressed('ignored button handler arg')

    tb.box_root.after(WAIT_0_MILLISECONDS, simulate_cancel_button_pressed, tb)
    assert tb.run() is None


def test_textbox_ok_pressed_calls_user_defined_callback():
    user_defined_callback = Mock()
    tb = textbox(text=TEST_TEXT, callback=user_defined_callback, run=False)

    def simulate_ok_button_pressed(tb_instance):
        tb_instance.ok_button_pressed('ignored button handler arg')

    def stop_running(tb_instance):
        tb_instance.stop()

    tb.box_root.after(WAIT_0_MILLISECONDS, simulate_ok_button_pressed, tb)
    tb.box_root.after(WAIT_1_MILLISECONDS, stop_running, tb)
    assert tb.run() == TEST_TEXT
    user_defined_callback.assert_called_once_with(ANY)


def test_textbox_ok_pressed_with_no_user_defined_callback():
    tb = textbox(msg=TEST_MESSAGE, title=TEST_TITLE, text=TEST_TEXT, run=False)

    def simulate_ok_button_pressed(tb_instance):
        tb_instance.ok_button_pressed('ignored button handler arg')

    tb.box_root.after(WAIT_0_MILLISECONDS, simulate_ok_button_pressed, tb)
    # tb.stop() happens because no user _user_specified_callback is set
    # the initial text value is unchanged, and is returned from run()
    assert tb.run() == TEST_TEXT


def test_instantiation_codebox():
    cb = codebox(msg=TEST_MESSAGE, title=TEST_TITLE, text=TEST_TEXT * 100, callback=TEST_CALLBACK, run=False)

    # cget returns strings so the monospace assertion is a bit messy:
    assert cb.text_area.cget('font') == "font1"  # a monospace font
