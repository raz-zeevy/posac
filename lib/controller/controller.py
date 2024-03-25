from lib.gui.gui import GUI

class Controller:
    def __init__(self):
        self.gui = GUI()

    def run_process(self):
        self.gui.run_process()



if __name__ == '__main__':
    a = Controller()
    a.run_process()