import jsonpickle
import pandas as pd
from lib.utils import *

class Session:
    def __init__(self, controller=None, path=None):
        if controller:
            controller = controller
            self.state = self._attributes_from_controller(controller)
        elif path:
            self.state = self._attributes_from_save(path)
        else:
            raise ValueError('Either controller or path must be provided')

    def _attributes_from_controller(self, controller):
        controller.init_fss_attributes()
        controller_dict = controller.__dict__.copy()
        for key in ['gui', 'keyboard', ]:
            controller_dict.pop(key, None)
        controller_dict['navigator'] = controller_dict['navigator'].__dict__.copy()
        for key in ['gui']:
            controller_dict['navigator'].pop(key, None)
        return controller_dict

    def _attributes_from_save(self, path):
        with open(path, 'r') as file:
            attributes = jsonpickle.decode(file.read())
        return attributes

    def save(self, path):
        json_string = jsonpickle.encode(self.state, indent=2)
        with open(path, 'w') as file:
            file.write(json_string)

    def load_to_controller(self, controller):
        pass



