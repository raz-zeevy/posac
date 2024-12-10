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
from lib.gui.tabs.internal_recoding_tab import InternalRecodingTab
import tkinter.messagebox as messagebox

class GenericCommand():
    def __init__(self, name, execute_fn, undo_fn, notebook, callback=None,
                 *args, **kwargs):
        self.name = name
        self.execute_fn = execute_fn
        self.undo_fn = undo_fn
        self.notebook = notebook  # Reference to the notebook instance
        self.args = args
        self.kwargs = kwargs
        if callback:
            self.command_exe_callback = callback

    def execute(self):
        self.execute_fn(*self.args, **self.kwargs)
        self.notebook.undo_stack.append(self)
        self.command_exe_callback()

    def undo(self):
        self.undo_fn()
        self.notebook.redo_stack.append(self)
        self.command_exe_callback()

    def print_stacks(self):
        print("Undo Stack:", self.notebook.undo_stack)
        print("Redo Stack:", self.notebook.redo_stack)

    def command_exe_callback(self):
        pass

    def __repr__(self):
        return self.name
def undoable(method):
    def wrapper(self, *args, **kwargs):
        # Define the undo actions based on method names
        undo_actions = {
            "add_internal_variable": self._remove_internal_variable,
            "remove_internal_variable": lambda:
            self._add_internal_variable(*args, **kwargs),
            "add_external_variable": self._remove_external_variable,
            "remove_external_variable": lambda :
            self._add_external_variable(*args, **kwargs),
        }
        # Get the function name
        func_name = method.__name__

        # Retrieve the corresponding undo function from the dictionary
        undo_fn = undo_actions.get(func_name)

        # Create the command
        command = GenericCommand(
            name=func_name,
            execute_fn=lambda *args, **kwargs: method(self, *args, **kwargs),
            undo_fn=undo_fn,
            notebook=self, # Pass the notebook instance
            callback = self.undoable_command_callback,
            *args, **kwargs
        )
        # Execute the command and add it to the undo stack
        command.execute()
    return wrapper

class PosacNotebook(tkinter.ttk.Notebook):
    def __init__(self, root, parent):
        self.parent = parent
        super().__init__(root)
        #
        self.undo_stack = []
        self.redo_stack = []
        #
        self.general_tab = GeneralTab(self)
        self.add(self.general_tab, text='General')
        self.zero_option_tab = ZeroOptionTab(self)
        self.add(self.zero_option_tab, text='Zero(0) option')
        self.internal_variables_tab = IVariablesTab(self)
        self.add(self.internal_variables_tab, text='Internal variables')
        self.internal_recoding_tab = InternalRecodingTab(self)
        self.add(self.internal_recoding_tab, text='Internal Recoding')
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
        self.internal_variables_tab._on_toggle_row = \
            self.update_posacsep_vars
        #
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
        # Bind lines per case changes
        self.general_tab.lines_per_case_entry.config(
            validate='focusout',
            validatecommand=(self.register(self._validate_lines_per_case), '%P')
        )

    ################
    # Flow Control #
    ################

    def undo(self):
        print("Undo")
        if self.undo_stack:
            command = self.undo_stack.pop()
            command.undo()

    def redo(self):
        if self.redo_stack:
            command = self.redo_stack.pop()
            command.execute()

    def undoable_command_callback(self):
        if self.undo_stack:
            self.parent.icon_menu.m_button_undo.config(state='normal')
        else:
            self.parent.icon_menu.m_button_undo.config(state='disabled')
        if self.redo_stack:
            self.parent.icon_menu.m_button_redo.config(state='normal')
        else:
            self.parent.icon_menu.m_button_redo.config(state='disabled')

    #################
    # POSAC Methods #
    #################

    # Internal Variables
    @undoable
    def add_internal_variable(self, values_: list = [], check=True):
        self._add_internal_variable(values_, check)

    def _add_internal_variable(self, values_: list = [], check=True):
        self.internal_variables_tab.add_variable(values_, check)
        self.update_posacsep_vars()

    @undoable
    def remove_internal_variable(self):
        self._remove_internal_variable()

    def _remove_internal_variable(self):
        self.internal_variables_tab.remove_variable()
        self.update_posacsep_vars()

    def clear_internal_variables(self):
        self.internal_variables_tab.clear_variables()
        self.posacsep_tab.clear_internal_variables()

    # External Variables

    @undoable
    def add_external_variable(self, values_: list = [], check=True):
        self._add_external_variable(values_,check)

    def _add_external_variable(self, values_: list = [], check=True):
        self.external_variables_tab.add_variable(values_, check)
        self.external_variables_ranges_tab.add_range()
        self.traits_tab.add_external_variable()

    @undoable
    def remove_external_variable(self):
        self._remove_external_variable()

    def _remove_external_variable(self):
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

    def update_posacsep_vars(self):
        """
        Called when selection is changed on internal vars page
        :return:
        """
        self.posacsep_tab.clear_internal_variables()
        for var in self.internal_variables_tab.get_selected_variables_nums():
            self.posacsep_tab.add_internal_variable(var)
    def toggle_zero_option(self, value):
        if not value:
            self.internal_variables_tab.show_low_high()
            self.external_variables_tab.show_low_high()
        else:
            self.internal_variables_tab.hide_low_high()
            self.external_variables_tab.hide_low_high()

    #########
    # State #
    #########

    def reset_to_default(self):
        self.clear_internal_variables()
        self.clear_external_variables()
        self.general_tab.set_default()
        self.output_files_tab.reset_default()
        self.posacsep_tab.set_to_default()
        self.traits_tab.reset_default()
        self.zero_option_tab.reset_default()
        self.internal_recoding_tab.reset_default()

    def get_state(self):
        return {
            'general': self.general_tab.get_all(),
            'zero_option': self.zero_option_tab.get_all(),
            'internal_variables': self.internal_variables_tab.get_all_variables(),
            'external_variables': self.external_variables_tab.get_all_variables(),
            'external_variables_ranges':
                self.external_variables_ranges_tab.get_all(),
            'traits': self.traits_tab.get_traits(),
            'internal_recoding': self.internal_recoding_tab.get_operations_values(),
            'posacsep': self.posacsep_tab.get_all(),
            'output_files': self.output_files_tab.get_all()
        }

    def set_state(self, state: dict):
        self.general_tab.set(**state['general'])
        self.zero_option_tab.set(**state['zero_option'])
        for var in state['internal_variables']:
            self.add_internal_variable(var, True)
        for var in state['external_variables']:
            self.add_external_variable(var, True)
        self.external_variables_ranges_tab.set_all(**state['external_variables_ranges'])
        self.traits_tab.set_traits(state['traits'])
        self.internal_recoding_tab.set_operations(state['internal_recoding'])
        self.posacsep_tab.set_all(**state['posacsep'])
        self.output_files_tab.set_all(**state['output_files'])

    def get_lines_per_case(self):
        return self.general_tab.get_lines_per_case()

    def _validate_lines_per_case(self, new_value):
        try:
            new_lines = int(new_value)
            if new_lines < 1:
                return False
                
            # Check if new value is less than any existing line numbers
            max_internal = max([int(row[1]) for row in self.internal_variables_tab.get_all_variables()] or [0])
            max_external = max([int(row[1]) for row in self.external_variables_tab.get_all_variables()] or [0])
            
            if new_lines < max(max_internal, max_external):
                messagebox.showwarning(
                    "Invalid Input",
                    f"Lines per case cannot be less than existing line numbers (max: {max(max_internal, max_external)})"
                )
                return False
            return True
        except ValueError:
            return False

