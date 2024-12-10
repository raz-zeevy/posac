import pytest

# Mark this module to be skipped by pytest
pytestmark = pytest.mark.skip("GUI tests should not run with pytest")

from lib.controller.controller import Controller


class WindowsTest(Controller):
    def __init__(self):
        super().__init__()
        self.notebook = self.gui.notebook

    def test_options(self):
        self.gui.show_options_window()
        self.gui.technical_options.notebook.select(2)
        self.gui.technical_options.notebook.select(1)
        print("done")


# Rename to not start with "test_" to avoid pytest picking it up
def run_posac_ls_graphs():
    from tests.scenarios_test import ScenTest
    a = ScenTest()
    a.simple_test()
    a.show_diagram_window()
    a.run_process()


def run_posacsep_graphs():
    from tests.scenarios_test import ScenTest
    a = ScenTest()
    a.simple_test()
    for i in range(1, 8):
        a.show_posacsep_diagram_window(i)
        a.gui.diagram_window.destroy()
    a.run_process()


def find_menu_index(menu, label):
    for index in range(menu.index('end') + 1):
        if menu.entrycget(index, 'label') == label:
            return index
    return None


if __name__ == '__main__':
    # a = WindowsTest()
    # a.test_options()
    # a.run_process()
    run_posacsep_graphs()
