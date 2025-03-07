from pathlib import Path
import pytest
import os
from lib.utils import SET_MODE_TEST
from tests.utils import are_files_identical
from lib.controller.controller import Controller
from tkinter import ttk

class TestScenarios:
    """Test class for running full POSAC scenarios"""
    
    @classmethod
    def setup_class(cls):
        """Create a single controller instance for all tests"""
        cls.controller = Controller()
        SET_MODE_TEST()  # Add this to prevent GUI issues during tests
        cls.notebook = cls.controller.gui.notebook

    @classmethod
    def teardown_class(cls):
        """Clean up after all tests are done"""
        if hasattr(cls, 'controller'):
            cls.controller.gui.root.destroy()
            cls.controller.gui.root.quit()
            
    @pytest.fixture(autouse=True)
    def setup(self, visual_mode):
        """Reset state between tests"""
        # Reset state before each test
        self.controller.restart_session()
        self.controller.gui.reset()
        yield
    
    def _setup_visual_test(self):
        """Setup visual testing environment with Done button and instructions"""
        def on_done():
            buttons_frame.destroy()
            self.controller.gui.root.quit()
        
        def on_open_run_dir():
            from lib.posac.posac_module import PosacModule
            PosacModule.open_running_files_dir()
            
        buttons_frame = ttk.Frame(self.controller.gui.root)
        buttons_frame.pack(side='bottom', pady=10)
        done_button = ttk.Button(
            buttons_frame,
            text="Done Testing",
            command=on_done
        )
        done_button.pack(side='left',padx=3)
        
        open_run_dir_button = ttk.Button(
            buttons_frame,
            text="Open Run Directory",
            command=on_open_run_dir
        )
        open_run_dir_button.pack(side='left',padx=3)
        self.controller.gui.root.mainloop()

    def _setup_base_scenario(self, job_name: str, data_file: str):
        """Setup basic scenario configuration"""
        self.controller.restart_session()
        
        # Setup general tab
        self.notebook.general_tab.set(
            job_name=job_name,
            data_file=data_file,
            lines_per_case=1,
            plot_item_diagram=True,
            plot_external_diagram=True,
            only_freq=0,
            posac_type='D',
            subject_type='S',
            id_location=[0, 0]
        )
        
        # Navigate to internal variables
        self.controller.gui.navigator.next_page()
        self.controller.gui.navigator.next_page()

    def _setup_output_files(self, scenario_dir: str):
        """Setup output files for a scenario"""
        output_dir = os.path.abspath(os.path.join("tests", scenario_dir, "output"))
        os.makedirs(output_dir, exist_ok=True)
        
        self.notebook.output_files_tab.set_all(
            os.path.join(output_dir, "job1.pos"),
            os.path.join(output_dir, "job1.ls1"),
            os.path.join(output_dir, "job1.ls2")
        )
        
        return output_dir

    def run_simple_scenario(self):
        """Run the simple scenario and return results"""
        self._setup_base_scenario(
            "kedar dj 24v 187pp diff dich: 1 2 3->2, 4 5 ->1",
            r"tests\simple_test\KEDDIR2.DAT"
        )

        # Add internal variables
        labels = ['ut', 'ut', 'ut', 'eq', 'fr', 'fr', 'ca', 'ca']
        for i in range(len(labels)):
            self.notebook.add_internal_variable(values_=['1', '1', 17 + i, labels[i]])
        
        # Add recoding operations
        self.notebook.internal_recoding_tab.set_recoding_num(3)
        
        # First recoding operation
        self.notebook.internal_recoding_tab.add_pair('1', '1')
        self.notebook.internal_recoding_tab.add_pair('2', '2')
        self.notebook.internal_recoding_tab.set_variables(1)
        
        # Second recoding operation
        self.notebook.internal_recoding_tab.select_operation(2)
        self.notebook.internal_recoding_tab.add_pair('3', '3')
        self.notebook.internal_recoding_tab.add_pair('2', '2')
        self.notebook.internal_recoding_tab.set_variables(2)
        
        # Third recoding operation
        self.notebook.internal_recoding_tab.select_operation(3)
        self.notebook.internal_recoding_tab.add_pair('4', '4')
        self.notebook.internal_recoding_tab.add_pair('3', '3')
        self.notebook.internal_recoding_tab.set_variables(3)

        # Setup external variables and traits
        self.controller.gui.navigator.next_page()
        self.notebook.add_external_variable(values_=[1, 1, 25, 'xv1'])
        
        self.controller.gui.navigator.next_page()
        self.notebook.external_variables_ranges_tab.set_range(0, ['6-9'])
        self.notebook.external_variables_ranges_tab.set_traits_num(4)
        
        self.controller.gui.navigator.next_page()
        for i in range(4):
            self.notebook.traits_tab.set_trait(i + 1, None, [[1, f'{i+6}-{i+6}']])
        
        # Technical options
        self.controller.gui.navigator.next_page()
        self.controller.gui.set_options(max_iterations=15)
        self.controller.gui.set_options(power_weights_low=4)
        self.controller.gui.set_options(power_weights_high=4)
        
        # Setup output and run
        self.controller.gui.navigator.next_page()
        output_dir = self._setup_output_files("simple_test")
        self.controller.run_posac()
        self.controller.enable_view_output()
        self.controller.save_session(Path(output_dir).parent /  "simple_test.session")
        
        return {
            'posac_drv': os.path.abspath('tests/simple_test/posainp.DRV'),
            'job_pos': os.path.join(output_dir, "job1.pos"),
            'expected_pos': os.path.abspath(r"tests\simple_test\results\job1.pos")
        }

    def run_jneeds_scenario(self):
        """Run the JNEEDS scenario and return results"""
        self._setup_base_scenario(
            "jneeds",
            r"tests\jneeds\jneedsTR.datt"
        )

        # Add internal variables
        labels = ['jn1', 'jn2']
        for i in range(len(labels)):
            self.notebook.add_internal_variable(values_=['1', '1', i + 1, labels[i]])
        
        # Navigate to output and run
        self.controller.gui.navigator.next_page()
        self.controller.gui.navigator.next_page()
        
        output_dir = self._setup_output_files("jneeds")
        self.controller.run_posac()
        self.controller.enable_view_output()
        self.controller.save_session(Path(output_dir).parent /  "jneeds.session")
        return {
            'posac_drv': os.path.abspath('tests/jneeds/posainp.DRV'),
            'job_pos': os.path.join(output_dir, "job1.pos"),
            'expected_pos': os.path.abspath(r"tests\jneeds\results\job1.pos")
        }
    
    def run_w250_scenario(self):
        """  
    w250
    6   0   0   0   1   1   6   2   4   1   0   0   0   0  15   0   1   0
    (T64,I1,T65,I1,T66,I1,T67,I1,T128,I1,T129,I1)
    4   4
    1      v1
    2      v2
    3      v3
    4      v4
    5      xv1
    6      xv2
    5   1   1   4
    6   1   1   4
    trait1 suff-income
    5   1   1   2
    6   1   1   4
    trait2 served army
    5   1   1   4
    6   1   2   4
    trait3 combat
    5   1   1   4
    6   1   4   4
    trait4 suff inc & service
    5   1   1   2
    6   1   2   4
    SHEMOR
    RECORD LENGTH  80
    FOR X,Y RECODE 0 THRU  25 = 1,  26 THRU  50 = 2,
                51 THRU  75 = 3,  76 THRU 100 = 4.
    FOR J,L RECODE 0 THRU  50 = 1,  51 THRU 100 = 2,
                101 THRU 150 = 3, 151 THRU 200 = 4.

        """
        """Run the W250 scenario and return results"""
        self._setup_base_scenario(
            "w250",
            r"tests\w250\w250recd.dat"
        )

        # Add internal variables
        self.notebook.add_internal_variable(values_=['1', 1, '64', 'v1'])
        self.notebook.add_internal_variable(values_=['1', 1, '65','v2'])
        self.notebook.add_internal_variable(values_=['1', 1, '66','v3'])
        self.notebook.add_internal_variable(values_=['1', 1, '67','v4'])
        
        # add external variables
        self.notebook.add_external_variable(values_=[1, 1, 128, 'xv1'])
        self.notebook.add_external_variable(values_=[1, 1, 129, 'xv2'])
        
        # add external variables ranges
        self.notebook.external_variables_ranges_tab.set_range(0, ['1-4'])
        self.notebook.external_variables_ranges_tab.set_range(1, ['1-4'])
        # add traits
        self.notebook.traits_tab.add_trait('trait1 suff-income', [['5', '1', '1-2'], ['6', '1', '1-4']])
        self.notebook.traits_tab.add_trait('trait2 served army', [['5', '1', '1-4'], ['6', '1', '2-4']])
        self.notebook.traits_tab.add_trait('trait3 combat', [['5', '1', '1-4'], ['6', '1', '4-4']])
        self.notebook.traits_tab.add_trait('trait4 suff inc & service', [['5', '1', '1-2'], ['6', '1', '2-4']])
        self.notebook.external_variables_ranges_tab.set_traits_num(4)
        # Technical options RECORD LENGTH
        self.controller.gui.set_options(record_length=80)
        self.controller.gui.set_options(set_selection='A')
        self.controller.gui.set_options(posac_axes='Yes')
        test_dir = os.path.abspath(r"tests\w250")
        output_dir = self._setup_output_files("w250")
        posac_axes_out = os.path.abspath(os.path.join(output_dir, "test.pax"))
        self.controller.gui.set_options(posac_axes_out=posac_axes_out)
        self.controller.run_posac()
        self.controller.enable_view_output()
        self.controller.save_session(Path(output_dir).parent /  "w250.session")
        
        return {
            'posac_drv': os.path.abspath(os.path.join(test_dir, 'posainp.DRV')),
            'job_pos': os.path.join(output_dir, "job1.pos"),
            'expected_pos': os.path.abspath(os.path.join(test_dir, 'results', 'job1.pos')),
            'posac_axes_out': posac_axes_out
        }
            
    def test_w250_scenario(self, visual_mode):
        """Test the W250 scenario with optional visual validation"""
        results = self.run_w250_scenario()
        if visual_mode:
            self._setup_visual_test()
            
    def test_jneeds_scenario(self, visual_mode):
        """Test the JNEEDS scenario with optional visual validation"""
        results = self.run_jneeds_scenario()
        if visual_mode:
            self._setup_visual_test()
            
    def test_simple_scenario(self, visual_mode):
        """Test the simple scenario with optional visual validation"""
        results = self.run_simple_scenario()
        if visual_mode:
            self._setup_visual_test()
            
            
            
    