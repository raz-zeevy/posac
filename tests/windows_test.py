import pytest

# Mark this module to be skipped by pytest
pytestmark = pytest.mark.skip("GUI tests should not run with pytest")

from lib.controller.controller import Controller


class WindowsTest(Controller):
    def __init__(self):
        super().__init__()
        self.notebook = self.gui.notebook

    def test_options(self):
        # Test default settings
        self.gui.show_options_window()
        settings = self.gui.technical_options.get_settings()
        assert settings['posac_axes'] == 'No'
        assert settings['ascii_output'] == 'No'
        
        # Test setting and getting values
        test_settings = {
            'posac_axes': 'Yes',
            'set_selection': 'B',
            'record_length': 100,
            'output_file': 'test.pax',
            'ascii_output': 'Yes',
            'special_graphic_char': '*',
            'form_feed': '#',
            'power_weights_low': 5,
            'power_weights_high': 6,
            'max_iterations': 20
        }
        
        self.gui.technical_options.set_settings(**test_settings)
        current_settings = self.gui.technical_options.get_settings()
        
        # Verify all settings were applied correctly
        for key, value in test_settings.items():
            assert str(current_settings[key]) == str(value), f"Setting {key} was not applied correctly"
        
        # Test tab navigation
        self.gui.technical_options.notebook.select(2)  # Technical tab
        self.gui.technical_options.notebook.select(1)  # ASCII Output tab
        self.gui.technical_options.notebook.select(0)  # Posac-Axes tab
        
        # Test that posac axes frame shows/hides correctly
        self.gui.technical_options.posac_axes_frame.save_axes_var.set('No')
        assert not self.gui.technical_options.posac_axes_frame.recoding_frame.winfo_viewable()
        
        self.gui.technical_options.posac_axes_frame.save_axes_var.set('Yes')

        # Test apply and cancel
        self.gui.technical_options.cancel_settings()
        
        # Show window again and verify defaults were restored
        self.gui.show_options_window()
        settings = self.gui.technical_options.get_settings()
        assert settings['posac_axes'] == 'No'
        assert settings['ascii_output'] == 'No'
        
        print("Options window tests passed successfully!")


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
    a = WindowsTest()
    a.test_options()
    a.run_process()
