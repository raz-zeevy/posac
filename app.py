import os
from lib.__version__ import VERSION
os.environ['VERSION'] = VERSION

from lib.controller.controller import Controller
from lib.utils import *
SET_MODE_PRODUCTION()
if __name__ == '__main__':
    a = Controller() 
    a.run_process()