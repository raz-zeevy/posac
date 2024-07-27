from lib.controller.controller import Controller


class WindowsTest(Controller):
    def __init__(self):
        super().__init__()
        self.notebook = self.gui.notebook

    def test_options(self):
        self.gui.show_options_window()
        self.gui.technical_options.notebook.select(2)
        self.gui.technical_options.notebook.select(1)
        # self.gui.technical_options.on_closing()
        print("done")

    def test_about(self):
        pass

if __name__ == '__main__':
    a = WindowsTest()
    a.test_options()
    a.run_process()
