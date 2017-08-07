import unittest

from mock import mock

from easygui.boxes.text_box import TextBox, textbox


class TestTextBox(unittest.TestCase):

    def test_init(self):
        mock_guitk_instance = mock.MagicMock()
        with mock.patch('easygui.boxes.text_box.GUItk', mock.MagicMock(return_value=mock_guitk_instance)) as mock_guitk_class:

            test_message = 'example message'
            test_title = 'example title'
            test_text = 'example text'
            test_codebox = False

            # Init and test state
            text_box = TextBox(msg=test_message, title=test_title, text=test_text, codebox=test_codebox)
            self.assertEqual(text_box._text, test_text)
            self.assertEqual(text_box.text, test_text)  # property
            self.assertEqual(text_box._msg, test_message)
            self.assertEqual(text_box.msg, test_message)  # property
            self.assertEqual(text_box.ui, mock_guitk_instance)
            mock_guitk_class.assert_called_once_with(
                test_message, test_title, test_text, test_codebox, mock.ANY
            )

            # Run and test state
            return_value = text_box.run()
            self.assertEqual(return_value, test_text)
            mock_guitk_instance.run.assert_called_once_with()
            self.assertEqual(text_box.ui, None)

    def test_text_box_interactive(self):
        tb = textbox(msg='msg', title='title', text='text', codebox=False, callback=None, run=True)
