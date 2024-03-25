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
        general_tab = GeneralTab(self)
        self.add(general_tab, text='General')
        zero_option_tab = ZeroOptionTab(self)
        self.add(zero_option_tab, text='Zero(0) option')
        internal_variables_tab = IVariablesTab(self)
        self.add(internal_variables_tab, text='Internal variables')
        external_variables_tab = EVariablesTab(self)
        self.add(external_variables_tab, text='External variables')
        external_variables_ranges_tab = EVRangesTab(self)
        self.add(external_variables_ranges_tab,
                 text='External variables ranges')
        traits_tab = TraitsTab(self)
        self.add(traits_tab, text='Traits')
        posacsep_tab = PosacsepTab(self)
        self.add(posacsep_tab, text='Posacsep')
        output_file_tab = OFilesTab(self)
        self.add(output_file_tab, text='Output Files')
