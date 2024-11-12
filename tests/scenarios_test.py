import os.path

from lib.controller.controller import Controller
import unittest

from lib.utils import p_POSAC_DRV
from tests.utils import are_files_identical

DATA_PATH = "data/first_test_data.csv"


class ScenTest(Controller):
    def __init__(self):
        super().__init__()
        self.notebook = self.gui.notebook
        self.next_page = self.gui.navigator.next_page

    def add_internal_variable(self, n):
        for _ in range(n):
            self.notebook.add_internal_variable()

    def simple_test(self):
        self.restart_session()
        self.notebook.general_tab.set(
            job_name="kedar dj 24v 187pp diff dich: 1 2 3->2, 4 5 ->1",
            data_file=r"C:\Users\Raz_Z\Projects\Shmuel\posac\tests\simple_test\KEDDIR2.DAT",
            lines_per_case=1,
            plot_item_diagram=True,
            plot_external_diagram=True,
            only_freq=0,
            posac_type='D',
            subject_type='S',
            id_location=[0, 0]
        )
        self.gui.navigator.next_page()
        self.gui.navigator.next_page()
        labels = ['ut', 'ut', 'ut', 'eq', 'fr', 'fr', 'ca', 'ca']
        for i in range(len(labels)):
            self.notebook.add_internal_variable(values_=['1', '1', 17 + i,
            labels[
                i]])
        self.next_page()
        self.notebook.add_external_variable(values_=[1, 1, 25, 'xv1'])
        self.next_page()
        self.notebook.external_variables_ranges_tab.set_range(0, ['6-9'])
        self.notebook.external_variables_ranges_tab.set_traits_num(4)
        self.next_page()
        # Traits
        self.notebook.traits_tab.set_trait(1, None, [[1, '6-6']])
        self.notebook.traits_tab.set_trait(2, None, [[1, '7-7']])
        self.notebook.traits_tab.set_trait(3, None, [[1, '8-8']])
        self.notebook.traits_tab.set_trait(4, None, [[1, '9-9']])
        self.next_page()
        # Technical options
        self.gui.set_options(max_iterations=15)
        self.gui.set_options(power_weights_low=4)
        self.gui.set_options(power_weights_high=4)
        # Posacsep
        self.next_page()
        # Output
        self.notebook.output_files_tab.set_all(
            r"C:\Users\Raz_Z\Projects\Shmuel\posac\tests\simple_test\output"
            r"\job1.pos",
            r"C:\Users\Raz_Z\Projects\Shmuel\posac\tests\simple_test\output"
            r"\job1.ls1",
            r"C:\Users\Raz_Z\Projects\Shmuel\posac\tests\simple_test\output"
            r"\job1.ls2"
        )
        self.run_posac()
        assert are_files_identical(p_POSAC_DRV,
                                   os.path.abspath(
                                       'simple_test/posainp.DRV'))
        # assert are_files_identical(
        #     r"C:\Users\Raz_Z\Projects\Shmuel\posac\tests\simple_test\output"
        #     r"\job1.pos",
        #     r"C:\Users\Raz_Z\Projects\Shmuel\posac\tests\simple_test\results"
        #     r"\job1.pos")

    def jneeds(self):
        self.restart_session()
        self.notebook.general_tab.set(
            job_name="jneed 5 compound vars",
            data_file=r"C:\Users\Raz_Z\Projects\Shmuel\posac\tests\jneeds\jneedsTR.datt",
            lines_per_case=1,
            plot_item_diagram=True,
            plot_external_diagram=True,
            only_freq=0,
            posac_type='D',
            subject_type='S',
            id_location=[0, 0]
        )
        self.next_page()
        self.next_page()
        labels = ['v1', 'v2', 'v3', 'v4', 'v5']
        cols = [67, 75, 83, 91, 99]
        for i in range(len(labels)):
            self.notebook.add_internal_variable(values_=['1', '1', cols[i],
                                                         labels[i]])
        self.next_page()
        self.next_page()
        self.notebook.output_files_tab.set_all(
            r"C:\Users\Raz_Z\Projects\Shmuel\posac\tests\jneeds\output"
            r"\job1.pos",
            r"C:\Users\Raz_Z\Projects\Shmuel\posac\tests\jneeds\output"
            r"\job1.ls1",
            r"C:\Users\Raz_Z\Projects\Shmuel\posac\tests\jneeds\output"
            r"\job1.ls2"
        )
        self.run_posac()
        self.save_test_state('jneeds')

    def save_test_state(self, test_name):
        self.save_session(f'scenarios/{test_name}.mpm')

if __name__ == '__main__':
    a = ScenTest()
    a.simple_test()
    # a.jneeds()
    a.run_process()
