import unittest

from mock import mock, patch, Mock, call

from easygui.boxes.text_box import TextBox, textbox, GUItk

try:
    import tkinter as tk  # python 3
except (SystemError, ValueError, ImportError):
    import Tkinter as tk  # python 2


MODBASE = 'easygui.boxes.text_box'

TEST_MESSAGE = 'example message'
TEST_TITLE = 'example title'
TEST_TEXT = 'example text'
TEST_CODEBOX = False
TEST_CALLBACK = Mock()
TEST_ARGS = [TEST_MESSAGE, TEST_TITLE, TEST_TEXT, TEST_CODEBOX, TEST_CALLBACK]


@patch(MODBASE + '.TextBox')
class TestTextBoxUtilities(unittest.TestCase):
    def test_textbox(self, mock_text_box_class):
        text_box = textbox(*TEST_ARGS, run=True)
        mock_text_box_class.assert_called_once_with(
            msg=TEST_MESSAGE,
            title=TEST_TITLE,
            text=TEST_TEXT,
            codebox=TEST_CODEBOX,
            callback=TEST_CALLBACK
        )
        text_box.run.assert_called_once_with()


@patch(MODBASE + '.GUItk')
class TestTextBox(unittest.TestCase):

    def test_instantiation(self, mock_ui_class):
        mock_ui = mock_ui_class.return_value
        text_box = TextBox(*TEST_ARGS)

        self.assertEqual(text_box._text, TEST_TEXT)
        self.assertEqual(text_box.text, TEST_TEXT)  # property
        self.assertEqual(text_box._msg, TEST_MESSAGE)
        self.assertEqual(text_box.msg, TEST_MESSAGE)  # property
        self.assertEqual(text_box.ui, mock_ui)
        self.assertEqual(text_box.callback, TEST_CALLBACK)
        args = [TEST_MESSAGE, TEST_TITLE, TEST_TEXT, TEST_CODEBOX, mock.ANY]
        mock_ui_class.assert_called_once_with(*args)

    def test_run(self, mock_ui_class):
        mock_ui = mock_ui_class.return_value
        text_box = TextBox(*TEST_ARGS)

        return_value = text_box.run()
        self.assertEqual(return_value, TEST_TEXT)
        mock_ui.run.assert_called_once_with()
        self.assertEqual(text_box.ui, None)

    def test_stop(self, mock_ui_class):
        mock_ui = mock_ui_class.return_value
        text_box = TextBox(*TEST_ARGS)
        text_box.stop()
        mock_ui.stop.assert_called_once_with()

    def test_callback_ui(self, mock_ui_class):
        text_box = TextBox(*TEST_ARGS)
        mock_ui = mock_ui_class.return_value

        text_box.callback_ui(ui=None, command='not update, x, or cancel', text='anything')
        self.assertEqual(text_box._text, TEST_TEXT)
        mock_ui.stop.assert_not_called()

        new_text = 'new text'
        text_box.callback_ui(ui=None, command='update', text=new_text)
        self.assertEqual(text_box._text, new_text)
        TEST_CALLBACK.assert_has_calls([call(text_box)])  # TODO: find why called twice

        text_box.callback_ui(ui=None, command='x', text='anything')
        self.assertEqual(text_box._text, None)
        mock_ui.stop.assert_called_once_with()

        text_box.callback_ui(ui=None, command='cancel', text='anything')
        self.assertEqual(text_box._text, None)
        mock_ui.stop.assert_has_calls([call(), call()])

    def test_text_property(self, mock_ui_class):
        text_box = TextBox(*TEST_ARGS)
        mock_ui = mock_ui_class.return_value

        text_from_getter = text_box.text
        self.assertEqual(text_from_getter, TEST_TEXT)

        new_text = 'some new text to test setter'
        text_box.text = new_text
        self.assertEqual(text_box._text, new_text)
        mock_ui.set_text.assert_called_with(new_text)

        del text_box.text
        self.assertEqual(text_box.text, '')
        mock_ui.set_text.assert_has_calls([call(new_text), call('')])

    def test_msg_property(self, mock_ui_class):
        text_box = TextBox(*TEST_ARGS)
        mock_ui = mock_ui_class.return_value

        msg_from_getter = text_box.msg
        self.assertEqual(msg_from_getter, TEST_MESSAGE)

        new_text = 'some new text to test setter'
        text_box.msg = new_text
        self.assertEqual(text_box._msg, new_text)
        mock_ui.set_msg_area.assert_called_with(new_text)

        del text_box.msg
        self.assertEqual(text_box.msg, '')
        mock_ui.set_msg_area.assert_has_calls([call(new_text), call('')])


class TestGUItk(unittest.TestCase):
    def setUp(self):
        self.ui = GUItk(msg=TEST_MESSAGE, title=TEST_TITLE, text=TEST_TEXT, code_box=TEST_CODEBOX, callback=TEST_CALLBACK)

    def test_instantiation(self):
        isinstance(self.ui.box_root, tk.Tk)
        isinstance(self.ui.message_area, tk.Text)
        isinstance(self.ui.text_area, tk.Text)

        self.assertEqual(self.ui.callback, TEST_CALLBACK)
        self.assertEqual(self.ui.message_area.get(0.0, 'end-1c'), TEST_MESSAGE)
        self.assertEqual(self.ui.text_area.get(0.0, 'end-1c'), TEST_TEXT)
        # title has been passed to windowing system

    def test_run(self):
        self.ui.box_root = Mock()
        self.ui.run()
        self.ui.box_root.mainloop.assert_called_once_with()
        self.ui.box_root.destroy.assert_called_once_with()

    def test_stop(self):
        self.ui.box_root = Mock()
        self.ui.stop()
        self.ui.box_root.quit.assert_called_once_with()

    def test_set_msg_area(self):
        new_text = 'some new text'
        self.ui.set_msg_area(msg=new_text)
        self.assertEqual(self.ui.message_area.get(1.0, 'end-1c'), new_text)

    def test_get_text(self):
        actual = self.ui.get_text()
        self.assertEqual(actual, TEST_TEXT)

    def test_set_text(self):
        new_text = 'some new text'
        self.ui.set_text(new_text)
        self.assertEqual(self.ui.text_area.get(1.0, 'end-1c'), new_text)
