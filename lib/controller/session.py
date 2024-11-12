import os

import jsonpickle


class Session:
    def __init__(self, controller=None, path=None):
        if controller:
            controller = controller
            self._attributes_from_controller(controller)
        elif path:
            self._attributes_from_save(path)
        else:
            raise ValueError('Either controller or path must be provided')

    def _attributes_from_controller(self, controller):
        self.state = controller.gui.get_state()
        self.state.update(controller.get_state())

    def _attributes_from_save(self, path):
        with open(path, 'r') as file:
            attributes = jsonpickle.decode(file.read())
        self.state = attributes

    def save(self, path):
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        json_string = jsonpickle.encode(self.state, indent=2)
        with open(path, 'w') as file:
            file.write(json_string)

    def load(self, controller):
        state = self.state
        controller.gui.load_state(state)
        controller.load_state(state)

    @staticmethod
    def reset(controller):
        controller.gui.reset()
        controller.reset_state()
