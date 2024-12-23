import tkinter as tk
from typing import List

import ttkbootstrap as ttk

from lib.gui.components.editable_tree_view import EditableTreeView
from lib.gui.components.form import Label, SelectionBox,\
    BoldLabel, Entry
from lib.gui.components.ranges_table import RangesTable

from lib.help.posac_help import Help
from lib.utils import real_size

px_TOP_INPUTS = 50
py_TOP_INPUTS = 10
px_TOP_INPUTS_INNER = 10


class TraitsTab(tk.Frame):
    class TabContext:
        NO_TRAITS = 'no_traits'
        TRAITS = 'traits'

    class TraitData:
        def __init__(self, label: str, data: List[List]):
            self.label : str = label
            self.data : List[List] = data

        def __str__(self):
            return f'{self.label}: {self.data}'

        def __repr__(self):
            return str(self)

        def __eq__(self, other):
            return self.label == other.label and self.data == other.data

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.notebook = parent
        self._traits = []
        self.main_frame = None
        self._current_trait = 1
        self._create_widgets()
        self._context: str = ''
        self._update_frames(self.TabContext.NO_TRAITS)

    def _create_widgets(self):
        self._create_table()
        self._create_no_traits_label()

    def _update_frames(self, context):
        """
        this function updates the frames according to the context,
        it updates the frame content according to the number of traits
        and doesn't update the table itself (it's done by set_trait)
        :param context:
        :return:
        """
        if context == self.TabContext.NO_TRAITS:
            self.main_frame.pack_forget()
            self.not_traits_frame.pack(fill='both', expand=True, padx=0,
                                       pady=0)
        elif context == self.TabContext.TRAITS:
            self.not_traits_frame.pack_forget()
            self.main_frame.pack(fill='both', expand=True, padx=0, pady=0)
            self.traits_num_box.config(
                dict(values=[str(i + 1) for i in
                             range(len(self._traits))])
            )
            self.select_trait(self._current_trait)
        self._context = context

    def _create_no_traits_label(self):
        self.not_traits_frame = tk.Frame(self)
        label = BoldLabel(self.not_traits_frame,
                          text='You must define the number of traits in the previous '
                               'screen', size=11)
        label.pack(pady=real_size(py_TOP_INPUTS))

    def _create_table(self):
        self.main_frame = tk.Frame(self)
        # Upper Frame
        upper_frame = tk.Frame(self.main_frame)
        upper_frame.pack(fill='x', padx=0, pady=real_size(py_TOP_INPUTS))
        # Traits Selection
        traits_num_frame = tk.Frame(upper_frame)
        trait_num_label = Label(traits_num_frame, text='Number of Traits')
        trait_num_label.pack(side='left')
        self.traits_num_box = SelectionBox(traits_num_frame,
                                           values=[str(i + 1) for i in
                                                   range(len(
                                                       self._traits))])
        self.traits_num_box.bind('<<ComboboxSelected>>',
                                 self._on_trait_num_change)
        self.traits_num_box.pack(side='right', padx=real_size(
            px_TOP_INPUTS_INNER))
        traits_num_frame.pack(side='left', padx=(real_size(px_TOP_INPUTS), 0),
                              pady=real_size(2))
        # Trait Label
        trait_label_frame = tk.Frame(upper_frame)
        trait_label = Label(trait_label_frame, text='Trait Label')
        trait_label.pack(side='left')
        self.trait_entry = Entry(trait_label_frame)
        self.trait_entry.pack(side='right', padx=real_size(
            px_TOP_INPUTS_INNER))
        trait_label_frame.pack(side='right',
                               padx=(0, real_size(px_TOP_INPUTS)),
                               pady=real_size(2))
        # Traits Table
        self.ranges_table_frame = tk.Frame(self.main_frame)
        self.traits_table = RangesTable(self.ranges_table_frame,
                                        help=Help.EXTERNAL_TRAITS)
        self.ranges_table_frame.pack(fill='both', expand=True, padx=10,
                                     pady=(0, 0))
        # Bottom Label
        bottom_frame = tk.Frame(self.main_frame)
        bottom_frame.pack(fill='x', padx=0, pady=real_size(py_TOP_INPUTS))
        self.bottom_label = BoldLabel(bottom_frame, text='',
                                      size=11)
        self.bottom_label.pack(padx=real_size(px_TOP_INPUTS))

    def _on_trait_num_change(self, event):
        self._update_traits_from_table()
        self.select_trait(int(event.widget.get()))

    def _update_traits_from_table(self):
        if self._context == self.TabContext.TRAITS:
            self._traits[
                self._current_trait - 1].label = self.trait_entry.get()
            self._traits[self._current_trait - 1].data = self.traits_table. \
                get_all_values()

    #######
    # Get #
    #######

    def get_current_trait(self):
        return self._current_trait

    def get_traits(self):
        return self._traits

    def get_traits_values(self) -> List[dict]:
        """
        This function returns the traits values in the format that is 
        expected by the POSAC input writer
        the data is the ranges for traits without the first two columns
        (external variable index and number of ranges)
        """
        traits = []
        for trait in self._traits:
            trait_value = {}
            trait_value['data'] = [var[2:] for var in trait.data]
            trait_value['label'] = trait.label
            traits.append(trait_value)
        return traits

    def get_traits_num(self):
        return len(self._traits)

    #######
    # Set #
    #######

    def select_trait(self, i):
        """
        Set the current trait to the (i)-th trait
        :param i: 1..len(traits)
        :return:
        """
        self.trait_entry.delete(0, tk.END)
        self.trait_entry.insert(0, self._traits[i - 1].label)
        self.traits_num_box.set(i)
        self.traits_table.clear_rows()
        self.bottom_label.config(text=f'This is trait No. {i} of '
                                      f'{len(self._traits)} traits')
        for ranges_row in self._traits[i - 1].data:
            self.traits_table.add_row(ranges_row)
        self._current_trait = i

    def set_trait(self, i, label=None, data: List[List] = None):
        if label is not None:
            self._traits[i - 1].label = label
        if data is not None:
            self._traits[i - 1].data = data
        if self._current_trait == i:
            self.select_trait(i)

    def set_traits(self, traits):
        for i, trait in enumerate(traits):
            self.set_trait(i+1, label=trait.label,
                           data=trait.data)

    #######
    # API #
    #######

    def update_traits_num(self, traits_num, var_num):
        self._update_traits_from_table()
        while len(self._traits) < traits_num:
            ranges = [RangesTable.DEFAULT_VALUE] * var_num
            label = f'trait{len(self._traits) + 1}'
            self._traits.append(self.TraitData(label, ranges))
        while len(self._traits) > traits_num:
            self._traits.pop()
        self._current_trait = min(self._current_trait, len(self._traits))
        if traits_num == 0:
            self._update_frames(self.TabContext.NO_TRAITS)
        else:
            self._update_frames(self.TabContext.TRAITS)

    def add_external_variable(self):
        for trait in self._traits:
            trait.data.append(RangesTable.get_new_row())
        if self._traits:
            self.select_trait(self._current_trait)

    def remove_external_variable(self):
        for trait in self._traits:
            if trait: trait.data.pop()
        if self._traits:
            self.select_trait(self._current_trait)

    def reset_default(self):
        for trait in self._traits:
            trait.label = f'trait{self._traits.index(trait) + 1}'
            trait.data = [RangesTable.DEFAULT_VALUE] * len(trait.data)
        if self._traits:
            self.select_trait(self._current_trait)

    def clear_external_variables(self):
        self._traits = []
        self.update_traits_num(0, 0)
        
    def add_trait(self, label : str, data : List[List]):
        self._traits.append(self.TraitData(label, data))
        self.select_trait(len(self._traits))
        self.update_traits_num(len(self._traits), len(data))
