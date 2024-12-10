import tkinter as tk
from typing import List
import ttkbootstrap as ttk
from lib.gui.components.form import Label, BoldLabel, SpinBox, SelectionBox
from lib.utils import real_size, rreal_size

class RecodingOperation:
    def __init__(self):
        self.selected_variables = []
        self.recoding_pairs = []
        self.invert = False

class InternalRecodingTab(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self._parent = parent
        self._recoding_operations : List[RecodingOperation] = []
        self._current_operation = 0
        self.num_recoding_operations = 0
        self._create_widgets()
        self._switch_frames('no_recodings')

    def _create_widgets(self):
        # Main Frame
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill='both', expand=True)
        
        # Operation Buttons Frame - Always visible
        operation_buttons_frame = tk.Frame(self.main_frame)
        operation_buttons_frame.pack(fill='x', padx=10, pady=real_size(5))
        
        self.add_operation_button = ttk.Button(
            operation_buttons_frame, 
            text="New Subset of Variables",
            command=self._add_operation
        )
        self.add_operation_button.pack(side='left', padx=5)
        
        self.remove_operation_button = ttk.Button(
            operation_buttons_frame, 
            text="Remove Current Subset",
            command=self._remove_current_operation,
            state='disabled'
        )
        self.remove_operation_button.pack(side='left', padx=5)
        
        # Message Frame - Shown only when no operations
        self.message_frame = tk.Frame(self.main_frame)
        self.message_label = Label(
            self.message_frame,
            text="To recode variables, click 'New Subset of Variables'. If you don't need to recode any variables, proceed to the next tab.",
            wraplength=rreal_size(450),
            justify="left"
        )
        self.message_label.pack(pady=real_size(10))
        
        # Recoding Content Frame - Hidden when no operations
        self.recoding_content = tk.Frame(self.main_frame)
        
        # Operation Selection and Variable Selection in same frame
        selection_frame = tk.Frame(self.recoding_content)
        selection_frame.pack(fill='x', padx=10, pady=real_size(5))
        
        # Operation Number (Left side)
        operation_label = Label(selection_frame, text='Subset of variables to recode')
        operation_label.pack(side='left', padx=(0, 10))
        
        self.operation_box = SelectionBox(selection_frame, values=['1'])
        self.operation_box.bind('<<ComboboxSelected>>', self._on_operation_change)
        self.operation_box.pack(side='left', padx=(0, 20))
        
        # Variable Selection (Right side)
        Label(selection_frame, text="Variable Indices:").pack(side='left', padx=(0, 5))
        self.var_index_entry = ttk.Entry(selection_frame, width=20)
        self.var_index_entry.pack(side='left')

        # Manual Recoding Frame
        manual_recoding_frame = ttk.LabelFrame(self.recoding_content, text="Manual Recoding")
        manual_recoding_frame.pack(fill='both', expand=True, padx=10, pady=(10, 10))

        # Input Frame for Old and New Values
        input_frame = ttk.Frame(manual_recoding_frame)
        input_frame.pack(fill='x', padx=10, pady=real_size(5))

        # Old Values Entry
        old_values_frame = ttk.LabelFrame(input_frame, text="Old Values")
        old_values_frame.pack(side='left', fill='x', expand=True, padx=(0, 5))
        self.old_values_entry = ttk.Entry(old_values_frame)
        self.old_values_entry.pack(fill='x', padx=5, pady=5)

        # New Value Entry
        new_value_frame = ttk.LabelFrame(input_frame, text="New Value")
        new_value_frame.pack(side='left', fill='x', expand=True, padx=(5, 0))
        self.new_value_entry = ttk.Entry(new_value_frame)
        self.new_value_entry.pack(fill='x', padx=5, pady=5)

        # Treeview Frame
        self._create_treeview(manual_recoding_frame)

        # Inversion Frame
        self._create_inversion_option()

    def _create_treeview(self, parent_frame):
        tree_frame = ttk.Frame(parent_frame)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))

        # Buttons Frame
        button_frame = ttk.Frame(tree_frame)
        button_frame.pack(side='left', fill='y', padx=(0, 5))

        self.add_button = ttk.Button(button_frame, text="Add", command=self._add_pair)
        self.add_button.pack(fill='x', pady=(0, 5))

        self.remove_button = ttk.Button(button_frame, text="Remove", command=self._remove_pair)
        self.remove_button.pack(fill='x')

        # Treeview
        columns = ('Old Values', 'New Value')
        self.pair_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=7)
        self.pair_tree.heading('Old Values', text='Old Values')
        self.pair_tree.heading('New Value', text='New Value')
        self.pair_tree.column('Old Values', anchor='center')
        self.pair_tree.column('New Value', anchor='center')
        self.pair_tree.pack(side='left', fill='both', expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.pair_tree.yview)
        self.pair_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side='right', fill='y')

    def _create_inversion_option(self):
        inversion_frame = ttk.LabelFrame(self.recoding_content, text="Inversion")
        inversion_frame.pack(fill='x', padx=10, pady=(0, 10))

        invert_label = Label(
            inversion_frame,
            text="Select to reverse the values after recoding. If no recoding pairs are defined, the inversion will apply to the original values.",
            wraplength=rreal_size(450),
            justify="left"
        )
        invert_label.pack(side='left', padx=real_size(10), pady=real_size(3))

        self.invert_var = tk.BooleanVar()
        self.invert_var.trace_add('write', lambda *args: self._update_current_operation())
        invert_check = ttk.Checkbutton(inversion_frame, variable=self.invert_var, bootstyle="round-toggle")
        invert_check.pack(side='right', padx=real_size((0, 40)))

    def _switch_frames(self, context: str):
        """Modified to show/hide only the recoding content"""
        if context == 'no_recodings':
            self.recoding_content.pack_forget()
            self.message_frame.pack(fill='x', padx=10)
            self.remove_operation_button.config(state='disabled')
            self.operation_box.config(state='disabled')
        else:
            self.message_frame.pack_forget()
            self.recoding_content.pack(fill='both', expand=True)
            self.remove_operation_button.config(state='normal')
            self.operation_box.config(state='readonly')

    def _on_operation_change(self, event):
        # Save current operation's state including pairs
        if self._recoding_operations and 0 < self._current_operation <= len(self._recoding_operations):
            current_op = self._recoding_operations[self._current_operation - 1]
            current_op.recoding_pairs = self.get_recoding_pairs()
        
        # Switch to new operation
        self.select_operation(int(event.widget.get()))

    def _update_current_operation(self):
        """Save the current operation's state"""
        if self._recoding_operations and 0 < self._current_operation <= len(self._recoding_operations):
            current_op = self._recoding_operations[self._current_operation - 1]
            var_input = self.var_index_entry.get().strip()
            if var_input:  # Only update if we have input
                current_op.selected_variables = [v.strip() for v in var_input.split(',') if v.strip()]
            current_op.recoding_pairs = self.get_recoding_pairs()
            current_op.invert = self.invert_var.get()

    def _add_pair(self):
        old_values = self.old_values_entry.get().strip()
        new_value = self.new_value_entry.get().strip()

        if not old_values or not new_value:
            return

        self.pair_tree.insert('', 'end', values=(old_values, new_value))
        self.old_values_entry.delete(0, 'end')
        self.new_value_entry.delete(0, 'end')

    def _remove_pair(self):
        selected_items = self.pair_tree.selection()
        for item in selected_items:
            self.pair_tree.delete(item)

    def get_recoding_pairs(self):
        return [(str(self.pair_tree.item(item)['values'][0]),
                str(self.pair_tree.item(item)['values'][1]))
                for item in self.pair_tree.get_children()]

    def _save_current_operation(self):
        """Save ALL current operation state including variables and pairs.
        This method is called before any operation switch or when explicitly 
        needing to save the current operation's state.
        
        The state includes:
        - Selected variables
        - Recoding pairs
        - Inversion state
        """
        if self._recoding_operations and 0 < self._current_operation <= len(self._recoding_operations):
            current_op = self._recoding_operations[self._current_operation - 1]
            # Save variables
            var_input = self.var_index_entry.get().strip()
            if var_input:
                current_op.selected_variables = [v.strip() for v in var_input.split(',') if v.strip()]
            # Save pairs and invert state
            current_op.recoding_pairs = self.get_recoding_pairs()
            current_op.invert = self.invert_var.get()

    def _switch_to_operation(self, operation_num):
        """Switch to the specified operation without saving current state.
        This is an internal method used when we want to change operations without saving the current state,
        such as after removing an operation or when the state has already been saved.
        
        Args:
            operation_num: The 1-based index of the operation to switch to
        """
        operation = self._recoding_operations[operation_num - 1]
        self._current_operation = operation_num
        # Update UI with operation data
        self.var_index_entry.delete(0, tk.END)
        self.var_index_entry.insert(0, ','.join(map(str, operation.selected_variables)))
        
        self.pair_tree.delete(*self.pair_tree.get_children())
        for old_val, new_val in operation.recoding_pairs:
            self.pair_tree.insert('', 'end', values=(old_val, new_val))
        
        self.invert_var.set(operation.invert)
        self.operation_box.set(str(operation_num))
    
    def select_operation(self, operation_num):
        """Public method to switch operations, saving the current state first.
        Use this method when switching operations through user interaction,
        ensuring that any changes to the current operation are saved before switching.
        
        Args:
            operation_num: The 1-based index of the operation to switch to
        """
        if 1 <= operation_num <= len(self._recoding_operations):
            self._save_current_operation()
            self._switch_to_operation(operation_num)

    def update_operations_num(self, num_operations):
        """Update the number of recoding operations"""
        # Save current operation state before any changes
        self._save_current_operation()
        
        while len(self._recoding_operations) < num_operations:
            self._recoding_operations.append(RecodingOperation())
        while len(self._recoding_operations) > num_operations:
            self._recoding_operations.pop()
        
        if num_operations == 0:
            self._current_operation = 0
            self._switch_frames('no_recodings')
        else:
            self._current_operation = 1
            self._switch_frames('recodings')
            self.operation_box.config(values=[str(i + 1) for i in range(num_operations)])
            self.select_operation(1)  # This will show the first operation's data

    def get_operations(self):
        """Similar to get_traits in TraitsTab"""
        return self._recoding_operations

    def get_operations_values(self):
        """Similar to get_traits_values in TraitsTab"""
        operations = []
        for op in self._recoding_operations:
            operation_value = {
                'selected_variables': op.selected_variables,
                'recoding_pairs': op.recoding_pairs,
                'invert': op.invert
            }
            operations.append(operation_value)
        return operations

    def set_operations(self, operations):
        """Similar to set_traits in TraitsTab"""
        # Save current state before making changes
        self._update_current_operation()
        
        # First update all operations
        for i, operation in enumerate(operations):
            if i < len(self._recoding_operations):
                op = self._recoding_operations[i]
                # Create a fresh copy of the operation data
                op.selected_variables = operation['selected_variables'].copy()
                op.recoding_pairs = operation['recoding_pairs'].copy()
                op.invert = operation['invert']
        
        # Then make sure we're showing the first operation
        if self._recoding_operations:
            self._current_operation = 1  # Reset to first operation
            self.operation_box.set('1')  # Update UI selection
            
            # Update UI with first operation's data
            first_op = self._recoding_operations[0]
            self.var_index_entry.delete(0, tk.END)
            self.var_index_entry.insert(0, ','.join(first_op.selected_variables))
            
            self.pair_tree.delete(*self.pair_tree.get_children())
            for old_val, new_val in first_op.recoding_pairs:
                self.pair_tree.insert('', 'end', values=(old_val, new_val))
            
            self.invert_var.set(first_op.invert)

    def set_variables(self, variables):
        """Set the variable indices for the current operation"""
        if isinstance(variables, (list, tuple)):
            variables = ','.join(map(str, variables))
        elif not isinstance(variables, str):
            variables = str(variables)
        
        # Clean up empty strings and whitespace
        variables = ','.join(v.strip() for v in variables.split(',') if v.strip())
        
        # Update UI
        self.var_index_entry.delete(0, tk.END)
        self.var_index_entry.insert(0, variables)
        
        # Directly update current operation
        if self._current_operation > 0 and len(self._recoding_operations) >= self._current_operation:
            current_op = self._recoding_operations[self._current_operation - 1]
            current_op.selected_variables = [v.strip() for v in variables.split(',') if v.strip()]

    def add_pair(self, old_values, new_value):
        """Add a recoding pair to the current operation"""
        if not old_values or not new_value:
            return

        self.pair_tree.insert('', 'end', values=(old_values, new_value))
        
        current_op = self._recoding_operations[self._current_operation - 1]
        current_op.recoding_pairs = self.get_recoding_pairs()

    def _add_operation(self):
        """Add a new recoding operation and switch to it.
        This method:
        1. Saves current operation state
        2. Adds new operation at the end
        3. Updates operation numbering
        4. Switches to the newly created operation
        """
        # Save current state before adding new operation
        self._save_current_operation()
        
        # Add new operation
        self._recoding_operations.append(RecodingOperation)
        num_operations = len(self._recoding_operations)
        
        # Update UI - values should be 1 to num_operations
        self.operation_box.config(values=[str(i) for i in range(1, num_operations + 1)])
        
        # Switch to new operation
        self.select_operation(num_operations)
        
        # Show recoding content if this is first operation
        if num_operations == 1:
            self._switch_frames('recodings')

    def _remove_current_operation(self):
        """Remove the currently selected operation and update numbering.
        This method:
        1. Removes the current operation
        2. Renumbers remaining operations (operations after the removed one get their numbers decreased by 1)
        3. Switches to the previous operation (or to no-operations state if none remain)
        
        Note: No need to save state since we're removing the current operation
        """
        if self._current_operation > 0:
            # Get the operation to be removed
            removed_index = self._current_operation - 1
            
            # Remove the current operation
            self._recoding_operations.pop(removed_index)
            
            # Update total number of operations
            num_operations = len(self._recoding_operations)
            
            # Update operation box values (1 to num_operations)
            self.operation_box.config(values=[str(i) for i in range(1, num_operations + 1)])
            
            if num_operations > 0:
                # Switch to previous operation if exists, otherwise stay at current position
                new_operation = max(1, self._current_operation - 1)
                self._switch_to_operation(new_operation)
            else:
                self._switch_frames('no_recodings')

    def set_recoding_num(self, num_operations):
        """Set the number of recoding operations"""
        self.update_operations_num(num_operations)
        
    
    def reset_default(self):
        """Reset the internal recoding tab to default state"""
        self._recoding_operations = []
        self._current_operation = 0
        self.pair_tree.delete(*self.pair_tree.get_children())
        self._switch_frames('no_recodings')

