import unittest

import os

from mock import patch, Mock

from easygui import buttonbox

MODBASE = 'easygui.boxes.button_box'

package_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))  # My parent's directory
image=os.path.join(package_dir, 'python_and_check_logo.gif')
images = [image, image, image]

TEST_MESSAGE = 'example message'
TEST_TITLE = 'example title'
TEST_CHOICES = ['ok', 'cancel']
TEST_IMAGE = None
TEST_IMAGES = [images, images, images, images]
TEST_DEFAULT_CHOICE = 'ok'
TEST_CANCEL_CHOICE = 'cancel'
TEST_CALLBACK = Mock()
TEST_RUN = True

TEST_ARGS = [TEST_MESSAGE, TEST_TITLE, TEST_CHOICES, TEST_IMAGE, TEST_IMAGES, TEST_DEFAULT_CHOICE, TEST_CANCEL_CHOICE,
             TEST_CALLBACK, TEST_RUN]


@patch(MODBASE + '.ButtonBox')
class TestTextBoxUtilities(unittest.TestCase):
    pass
    # def test_textbox(self, mock_button_box_class):
    #     mock_instance = Mock()
    #     mock_instance.run = Mock(return_value='reply')
    #     mock_button_box_class.return_value = mock_instance
    #
    #     reply = buttonbox(*TEST_ARGS)
    #
    #     mock_button_box_class.assert_called_once_with(
    #         msg=TEST_MESSAGE,
    #         title=TEST_TITLE,
    #         choices=TEST_CHOICES,
    #         images=TEST_IMAGES,
    #         default_choice=TEST_DEFAULT_CHOICE,
    #         cancel_choice=TEST_CANCEL_CHOICE,
    #         callback=TEST_CALLBACK,
    #     )
    #     mock_instance.run.assert_called_once()
    #     self.assertEqual(reply, 'reply')


class TestButtonBox(unittest.TestCase):
    pass

    # def test_button_box_demo1(self):
    #     value = buttonbox(
    #         title="First demo",
    #         msg="bonjour",
    #         choices=["Button[1]", "Button[2]", "Button[3]"],
    #         default_choice="Button[2]")
    #     print("Return: {}".format(value))
    #
    # def test_button_box_demo2(self):
    #     package_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)));  # My parent's directory
    #     images = list()
    #     images.append(os.path.join(package_dir, "python_and_check_logo.gif"))
    #     images.append(os.path.join(package_dir, "zzzzz.gif"))
    #     images.append(os.path.join(package_dir, "python_and_check_logo.gif"))
    #     images = [images, images, images, images, ]
    #     value = buttonbox(
    #         title="Second demo",
    #         msg="Now is a good time to press buttons and show images",
    #         choices=['ok', 'cancel'],
    #         images=images)
    #     print("Return: {}".format(value))

