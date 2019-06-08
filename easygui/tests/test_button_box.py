import os
import unittest

from mock import patch, Mock

from easygui import buttonbox, boolbox, ynbox, ccbox, indexbox, msgbox
from easygui.tests import WAIT_0_MILLISECONDS, WAIT_1_MILLISECONDS

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
             TEST_CALLBACK]


@patch(MODBASE + '.ButtonBox')
class TestButtonBoxUtilities(unittest.TestCase):
    def test_buttonbox_instantiatesAndRunsButtonBoxReturningTheReply(self, mock_button_box_class):
        mock_instance = Mock()
        mock_instance.run = Mock(return_value='reply')
        mock_button_box_class.return_value = mock_instance

        reply = buttonbox(*TEST_ARGS)

        mock_button_box_class.assert_called_once_with(
            msg=TEST_MESSAGE,
            title=TEST_TITLE,
            choices=TEST_CHOICES,
            images=TEST_IMAGES,
            default_choice=TEST_DEFAULT_CHOICE,
            cancel_choice=TEST_CANCEL_CHOICE,
            callback=TEST_CALLBACK,
        )
        mock_instance.run.assert_called_once()
        self.assertEqual(reply, 'reply')


@patch(MODBASE + '.ButtonBox')
class TestBoolboxAndVariants(unittest.TestCase):

    def test_returnsTrueWhenFirstChoiceIsSelected(self, mock_button_box_class):
        test_first_choice = 'Yes'
        test_other_choice = 'No'
        mock_button_box_class.return_value.run.return_value = test_first_choice
        for box in (boolbox, ynbox, ccbox):
            self.assertEqual(box(choices=(test_first_choice, test_other_choice)), True)

    def test_returnsFalseWhenSecondChoiceIsSelected(self, mock_button_box_class):
        test_first_choice = 'Yes'
        test_other_choice = 'No'
        mock_button_box_class.return_value.run.return_value = test_other_choice
        for box in (boolbox, ynbox, ccbox):
            self.assertEqual(box(choices=(test_first_choice, test_other_choice)), False)

    def test_raisesIfMoreThanTwoChoicesAreSupplied(self, _):
        for box in (boolbox, ynbox, ccbox):
            self.assertRaises(AssertionError, box, choices=('Yes', 'No', 'Maybe'))


@patch(MODBASE + '.ButtonBox')
class TestIndexbox(unittest.TestCase):
    def test_returnsZeroWhenZerothIndexChoiceIsSelected(self, mock_button_box_class):
        test_choices = ('zeroth', 'first', 'second')
        mock_button_box_class.return_value.run.return_value = test_choices[0]
        self.assertEqual(indexbox(choices=test_choices), 0)

    def test_returnsTwoWhenSecondIndexChoiceIsSelected(self, mock_button_box_class):
        test_choices = ('zeroth', 'first', 'second')
        mock_button_box_class.return_value.run.return_value = test_choices[1]
        self.assertEqual(indexbox(choices=test_choices), 1)

    def test_raisesIfReturnValueNotInChoices(self, mock_button_box_class):
        test_choices = ('zeroth', 'first', 'second')
        mock_button_box_class.return_value.run.return_value = 'nineth'
        self.assertRaises(AssertionError, indexbox, choices=test_choices)


@patch(MODBASE + '.ButtonBox')
class TestMsgbox(unittest.TestCase):
    def test_msgbox_instantiatesAndRunsButtonBoxReturningTheReply(self, mock_button_box_class):
        test_ok_button = 'OK'
        mock_button_box_class.return_value.run.return_value = test_ok_button
        reply = msgbox()

        mock_button_box_class.assert_called_once_with(
            msg='(Your message goes here)',
            title=" ",
            choices=[test_ok_button],
            images=None,
            default_choice=test_ok_button,
            cancel_choice=test_ok_button,
            callback=None,
        )
        mock_button_box_class.return_value.run.assert_called_once()
        self.assertEqual(reply, test_ok_button)


class TestButtonBoxIntegration(unittest.TestCase):
    def test_userPressesButton_buttonValueReturned(self):
        bb = buttonbox(*TEST_ARGS, run=False)

        def simulate_button_pressed(bb_instance):
            bb_instance._button_pressed('ok')

        def stop_running(tb_instance):
            tb_instance.stop()

        bb.box_root.after(WAIT_0_MILLISECONDS, simulate_button_pressed, bb)
        bb.box_root.after(WAIT_1_MILLISECONDS, stop_running, bb)

        actual = bb.run()
        self.assertEqual(actual, 'ok')
        TEST_CALLBACK.assert_called_once_with()

    def test_userPressesCancel_cancelChoiceValueReturned(self):
        bb = buttonbox(*TEST_ARGS, run=False)

        def simulate_cancel_pressed(bb_instance):
            bb_instance._cancel_button_pressed(None)

        bb.box_root.after(WAIT_0_MILLISECONDS, simulate_cancel_pressed, bb)

        actual = bb.run()
        self.assertEqual(actual, 'cancel', msg="'{}' returned, 'cancel' expected".format(actual))
