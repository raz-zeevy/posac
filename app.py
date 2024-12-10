from dotenv import load_dotenv
load_dotenv()

from lib.controller.controller import Controller
from lib.utils import *

SET_MODE_PRODUCTION()
if __name__ == '__main__':
    a = Controller()
    a.run_process()