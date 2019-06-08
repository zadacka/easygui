import unittest

from mock import patch, call

from easygui import integerbox

MODBASE = 'easygui.boxes.fillable_box'


class TestIntegerbox(unittest.TestCase):
    def test_integerBoxValidatesUserInput_msgboxNotifiesAndLoopContinues(self):
        lower_bound = 2
        upper_bound = 4
        user_value_above_upper_bound = 7
        user_value_below_lower_bound = 1
        user_value_between_bounds = 3

        user_input_values = ["not a number",
                             user_value_above_upper_bound,
                             user_value_below_lower_bound,
                             user_value_between_bounds]

        with patch(MODBASE + '.msgbox') as mock_msgbox:
            with patch(MODBASE + '.FillableBox') as mockFillableBox_class:
                mockFillableBox_class.return_value.run.side_effect = user_input_values
                result = integerbox(lowerbound=lower_bound, upperbound=upper_bound)

        mock_msgbox.assert_has_calls([
            call('The value that you entered:\n\t"not a number"\nis not an integer.', 'Error'),
            call('The value that you entered is greater than the upper bound of 4.', 'Error'),
            call('The value that you entered is less than the lower bound of 2.', 'Error')]
        )
        self.assertEquals(result, user_value_between_bounds)

