import tkinter.ttk
from ttkbootstrap import ttk
from lib.gui.tabs.general_tab import GeneralTab
from lib.gui.tabs.external_variables_ranges_tab import EVRangesTab
from lib.gui.tabs.external_variables_tab import EVariablesTab
from lib.gui.tabs.internal_variables_tab import IVariablesTab
from lib.gui.tabs.output_files_tab import OFilesTab
from lib.gui.tabs.posacsep_tab import PosacsepTab
from lib.gui.tabs.traits_tab import TraitsTab
from lib.gui.tabs.zero_option_tab import ZeroOptionTab


class PosacNotebook(tkinter.ttk.Notebook):
    def __init__(self, root):
        super().__init__(root)
        self.general_tab = GeneralTab(self)
        self.add(self.general_tab, text='General')
        self.zero_option_tab = ZeroOptionTab(self)
        self.add(self.zero_option_tab, text='Zero(0) option')
        self.internal_variables_tab = IVariablesTab(self)
        self.add(self.internal_variables_tab, text='Internal variables')
        self.external_variables_tab = EVariablesTab(self)
        self.add(self.external_variables_tab, text='External variables')
        self.external_variables_ranges_tab = EVRangesTab(self)
        self.add(self.external_variables_ranges_tab,
                 text='External variables ranges')
        self.traits_tab = TraitsTab(self)
        self.add(self.traits_tab, text='Traits')
        self.posacsep_tab = PosacsepTab(self)
        self.add(self.posacsep_tab, text='Posacsep')
        self.output_files_tab = OFilesTab(self)
        self.add(self.output_files_tab, text='Output Files')
        #
        self.bind_notebook_widgets()

    def bind_notebook_widgets(self):
        # Data Buttons
        self.internal_variables_tab.add_button.config(
            command=self.add_internal_variable
        )
        self.internal_variables_tab.remove_button.config(
            command=self.remove_internal_variable
        )
        self.internal_variables_tab.clear_button.config(
            command=self.clear_internal_variables
        )
        self.external_variables_tab.add_button.config(
            command=self.add_external_variable
        )
        self.external_variables_tab.remove_button.config(
            command=self.remove_external_variable
        )
        self.external_variables_tab.clear_button.config(
            command=self.clear_external_variables
        )
        # Traits number
        self.external_variables_ranges_tab.on_change_traits_num = \
            self.on_traits_num_change
        self.external_variables_ranges_tab.traits_num_spinbox.config(
            command=self.on_traits_num_change
        )
        # missing values
        self.zero_option_tab._on_change = lambda: self.toggle_zero_option(
                self.zero_option_tab._zero_option_combo.get() == 'Yes')

    # Internal Variables
    def add_internal_variable(self, values_: list = [], check=True):
        self.internal_variables_tab.add_variable(values_, check)
        self.posacsep_tab.add_internal_variable()

    def remove_internal_variable(self):
        self.internal_variables_tab.remove_variable()
        self.posacsep_tab.remove_internal_variable()

    def clear_internal_variables(self):
        self.internal_variables_tab.clear_variables()
        self.posacsep_tab.clear_internal_variables()

    # External Variables

    def add_external_variable(self, values_: list = [], check=True):
        self.external_variables_tab.add_variable(values_, check)
        self.external_variables_ranges_tab.add_range()
        self.traits_tab.add_external_variable()

    def remove_external_variable(self):
        self.external_variables_tab.remove_variable()
        self.external_variables_ranges_tab.remove_range()
        self.traits_tab.remove_external_variable()

    def clear_external_variables(self):
        self.external_variables_tab.clear_variables()
        self.external_variables_ranges_tab.clear_ranges()
        self.traits_tab.clear_external_variables()

    def exist_external_variables(self):
        return self.external_variables_tab.get_vars_num() > 0

    # External Traits
    def on_traits_num_change(self):
        traits_num = self.external_variables_ranges_tab.get_external_traits_num()
        self.traits_tab.update_traits_num(
            traits_num,
            self.external_variables_tab.get_vars_num())

    def toggle_zero_option(self, value):
        print(f'TOGGLED, {value}')
        if not value:
            self.internal_variables_tab.show_low_high()
            self.external_variables_tab.show_low_high()
        else:
            self.internal_variables_tab.hide_low_high()
            self.external_variables_tab.hide_low_high()

    def reset_to_default(self):
        self.clear_internal_variables()
        self.clear_external_variables()
        self.general_tab.set_default()
        self.output_files_tab.reset_default()
        self.posacsep_tab.reset_to_default()
        self.traits_tab.reset_default()
        self.zero_option_tab.reset_default()

    def get_state(self):
        return {
            'general': self.general_tab.get_all(),
            'zero_option': self.zero_option_tab.get_all(),
            'internal_variables': self.internal_variables_tab.get_all_variables(),
            'external_variables': self.external_variables_tab.get_all_variables(),
            'external_variables_ranges':
                self.external_variables_ranges_tab.get_all(),
            'traits': self.traits_tab.get_traits(),
            'posacsep': self.posacsep_tab.get_all(),
            'output_files': self.output_files_tab.get_all()
        }

    def set_state(self, state : dict):
        self.general_tab.set(**state['general'])
        self.zero_option_tab.set(**state['zero_option'])
        for var in state['internal_variables']:
            self.add_internal_variable(var, True)
        for var in state['external_variables']:
            self.add_external_variable(var, True)
        self.external_variables_ranges_tab.set_all(**state[
            'external_variables_ranges'])
        self.traits_tab.set_traits(state['traits'])
        self.posacsep_tab.set_all(**state['posacsep'])
        self.output_files_tab.set_all(**state['output_files'])