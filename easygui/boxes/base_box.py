from easygui.boxes import to_string


class BaseBox(object):
    """ The BaseBox class is an abstract class """

    def run(self):
        self.ui.run()
        self.ui = None
        # TODO: confirm this behaviour: why return text?
        # Answer: because this is a TEXT BOX, and the return behaviour is to give
        # you the thing-of-interest. Must be different for every box class...
        return self._text

    def stop(self):
        self.ui.stop()

    def callback_ui(self, ui, command, text):
        """ This method is executed when ok, cancel, or x is pressed in the ui. """
        if command == 'update':  # OK was pressed
            self._text = text
            if self.callback:
                # If a callback was set, call main process
                self.callback(self)
            else:
                self.stop()
        elif command in ('x', 'cancel'):
            self.stop()
            self._text = None

    @property
    def msg(self):
        """Text in msg Area"""
        return self._msg

    @msg.setter
    def msg(self, msg):
        self._msg = to_string(msg)
        self.ui._set_msg_area(self._msg)

    @msg.deleter
    def msg(self):
        self._msg = ""
        self.ui._set_msg_area(self._msg)