import os
import sys

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from lib.controller.controller import Controller

DATA_PATH = "data/first_test_data.csv"


class GuiTest(Controller):
    def __init__(self):
        super().__init__()
        self.notebook = self.gui.notebook

    ##### Helper functions
    def add_external_variables(self, n):
        for _ in range(n):
            self.notebook.add_external_variable()

    def add_internal_variables(self, n):
        for _ in range(n):
            self.notebook.add_internal_variable()

    #### Tests
    def test_general_tab(self):
        self.notebook.select(0)
        gt = self.notebook.general_tab
        gt.set(
            job_name="Test",
            data_file=DATA_PATH,
            lines_per_case=3,
            plot_item_diagram=True,
            plot_external_diagram=False,
            posac_type="D",
            subject_type="S",
            id_location=(1, 2),
        )
        test_values = gt.get_all()
        gt.set_default()
        assert gt.get_all() == gt.DEFAULT_VALUES
        gt.set(**test_values)
        cur_values = gt.get_all()
        assert test_values == cur_values

    def test_zero_option(self):
        self.notebook.select(1)
        zo = self.notebook.zero_option_tab
        zo.set(zero_option=False)
        test_values = zo.get_all()
        zo.reset_default()
        assert zo.get_all() == zo.DEFAULT_VALUES
        zo.set(**test_values)
        cur_values = zo.get_all()
        assert test_values == cur_values

    def test_internal_variables_tab(self):
        """Test internal variables tab functionality"""
        self.notebook.select(2)  # Select internal variables tab
        iv = self.notebook.internal_variables_tab

        # Test adding/removing variables
        iv.remove_variable()
        first_var = ["10", "1", "1", "8"]
        iv.add_variable(first_var, check=False)

        # Add multiple variables
        dummy_vars = [
            ["1", "2", "3", "4"],
            ["1", "2", "3", "4"],
            ["1", "2", "3", "4"],
            ["1", "2", "3", "4"],
        ]
        for var in dummy_vars:
            iv.add_variable(var, check=True)

        # Verify selected variables
        test_values = iv.get_selected_variables()
        for i, row in enumerate(dummy_vars):
            assert row[:4] == test_values[i][:4]

        self.gui.notebook.clear_internal_variables()

    def test_external_variables_tab(self):
        self.notebook.select(3)
        ev = self.notebook.external_variables_tab
        ev.remove_variable()
        dummy_vars = [
            [1, 2, 3, 4],
            [1, 2, 3, 4],
            [1, 2, 3, 4],
            [1, 2, 3, 4],
        ]
        for i in range(len(dummy_vars)):
            for j in range(len(dummy_vars[i])):
                dummy_vars[i][j] = str(dummy_vars[i][j])
        first_var = ["10", "5", "3", "8"]
        ev.add_variable(first_var, check=False)
        assert len(ev.get_all_variables()) == 1
        for i in range(len(dummy_vars)):
            ev.add_variable(dummy_vars[i], check=True)
        test_values = ev.get_selected_variables()
        for i, row in enumerate(dummy_vars):
            assert row[:4] == test_values[i][:4]
        test_values = ev.get_all_variables()
        assert len(test_values) == len(dummy_vars) + 1
        ev.clear_variables()
        assert not ev.get_all_variables()
        ev.set_default()
        assert not ev.get_all_variables()

    def test_external_variables_ranges_tab(self):
        self.notebook.select(4)
        evr = self.notebook.external_variables_ranges_tab
        # Add an external variable
        self.add_external_variables(3)
        assert evr.num_external_ranges == 3
        test_values = [
            ["1", "1-9", "1-9", "1-3"],
            ["2", "1-3", "1-2", "1-5"],
            ["3", "1-9", "1-9", "1-3"],
        ]
        evr.set_range(0, test_values[0])
        evr.set_range(1, test_values[1])
        evr.set_range(2, test_values[2])
        assert evr.get_all_ranges_values() == test_values
        # Set the number of external traits
        traits_num = 12
        evr.set_traits_num(traits_num)
        assert evr.get_external_traits_num() == traits_num
        #
        all_data = evr.get_all()
        evr.set_default()
        assert evr.get_all_ranges_values() == [evr.DEFAULT_VALUE] * 3
        evr.set_all(all_data["ranges"], all_data["traits_num"])
        assert evr.get_all() == {"ranges": test_values, "traits_num": traits_num}
        evr.set_default()
        self.notebook.clear_external_variables()

    def assert_no_traits(self):
        tt = self.notebook.traits_tab
        assert tt._context == tt.TabContext.NO_TRAITS
        assert tt.get_current_trait() == 0
        assert not tt.get_traits()

    def test_traits_tab(self):
        self.notebook.select(5)
        tt = self.notebook.traits_tab
        # default values test
        self.assert_no_traits()
        # adding variables and traits test
        num_traits_1 = 12
        num_ex_var_1 = 30
        self.add_external_variables(num_ex_var_1)
        self.notebook.external_variables_ranges_tab.set_traits_num(num_traits_1)
        assert tt._context == tt.TabContext.TRAITS
        cur_traits = tt.get_traits()
        def_test_traits = [
            tt.TraitData(f"trait{i + 1}", [["1", "1-9"] for _ in range(num_ex_var_1)])
            for i in range(num_traits_1)
        ]
        assert cur_traits == def_test_traits
        # reset traits test
        self.notebook.external_variables_ranges_tab.set_traits_num(0)
        self.notebook.external_variables_ranges_tab.set_traits_num(num_traits_1)
        assert cur_traits == def_test_traits
        # simple set test
        tt.set_trait(
            1,
            label="test_trait",
            data=[
                ["2", "1-9", "1-3"] if i > 10 else ["1", "1-2"]
                for i in range(num_ex_var_1)
            ],
        )
        assert tt.get_traits()[0].label == "test_trait"
        # clear external variables test
        self.notebook.clear_external_variables()
        self.assert_no_traits()
        # adding complex variables and traits test
        num_traits_2 = 12
        num_ex_var_2 = 20
        test_traits_1 = [
            tt.TraitData(
                f"test_trait{i * 5 + 1}", [["1", "1-9"] for _ in range(num_ex_var_2)]
            )
            for i in range(num_traits_2)
        ]

        # modify the test_traits_1 to be unique numbers
        for i in range(num_traits_2):
            for j in range(num_ex_var_2):
                test_traits_1[i].data[j][0] = str(i + 1)
        self.add_external_variables(num_ex_var_2)
        self.notebook.external_variables_ranges_tab.set_traits_num(num_traits_2)
        for i in range(num_traits_2):
            tt.set_trait(
                i + 1,
                label=f"test_trait{i * 5 + 1}",
                data=[test_traits_1[i].data[j] for j in range(num_ex_var_2)],
            )
        assert tt.get_traits() == test_traits_1
        tt.reset_default()
        self.gui.notebook.clear_external_variables()

    def test_traits_tab_data_persistence(self):
        """Test that trait data persists when adding/removing external variables"""
        self.notebook.select(5)
        tt = self.notebook.traits_tab

        # Setup: 1 trait, 1 external variable
        self.notebook.external_variables_ranges_tab.set_traits_num(1)
        self.add_external_variables(1)

        # Edit the trait table UI directly (simulating user input)
        # This updates the UI but not yet the internal model (self._traits)
        tt.traits_table.set_range(0, ['1', '2-6'])

        # Verify UI has it
        assert tt.traits_table.get_ranges_for_variable(0) == ['2-6']

        # Add external variable -> Should trigger sync before update
        self.add_external_variables(1)

        # Check if UI still has the old value for var 0
        ranges_var_0 = tt.traits_table.get_ranges_for_variable(0)
        assert ranges_var_0 == ['2-6'], f"Data lost! Expected ['2-6'], got {ranges_var_0}"

        # Cleanup
        self.notebook.clear_external_variables()
        tt.reset_default()

    def test_posacsep_tab(self):
        var_num = 10
        self.notebook.select(6)
        pt = self.notebook.posacsep_tab
        self.add_internal_variables(var_num)

        # Test 1: Check set_combo with False
        pt.set_combo(False)
        assert not pt.get_combo()
        pt.set_combo(True)
        # Test 2: Check set_values with different values
        pt.set_values(var_num * [5])
        assert pt.get_values() == var_num * [5], (
            f"Expected {var_num * [5]}, got {pt.get_values()}"
        )

        # Test 3: Check get_values after set_values
        pt.set_values(var_num * [2])
        assert pt.get_values() == var_num * [2]

        # Test 4: Check reset_to_default()
        pt.set_to_default()
        assert pt.get_values() == var_num * [pt.DEFAULT_VALUE]
        self.notebook.clear_internal_variables()
        assert not pt.get_values()

    def test_output_tab(self):
        self.notebook.select(7)  # Select Output Files tab
        oft = self.notebook.output_files_tab

        # Save original values to restore later
        original_values = oft.get_all()

        # Test default values
        oft.reset_default()
        default_values = oft.get_all()
        assert default_values == {
            "posac": oft.DEFAULT_OUT_POS,
            "lsa1": oft.DEFAULT_OUT_LS1,
            "lsa2": oft.DEFAULT_OUT_LS2,
        }

        # Test set_all method
        test_paths = {
            "posac": "C:/test/path/test.pos",
            "lsa1": "C:/test/path/test.ls1",
            "lsa2": "C:/test/path/test.ls2",
        }
        oft.set_all(test_paths["posac"], test_paths["lsa1"], test_paths["lsa2"])
        assert oft.get_all() == test_paths

        # Test get_default_base_name with job name
        # First, set a job name
        self.notebook.general_tab.set_job_name("test_job")
        assert oft.get_default_base_name() == "test_job"

        # Test get_default_base_name with data file name (when job name is empty)
        self.notebook.general_tab.set_job_name("")
        self.notebook.general_tab.set_data_file("C:/data/test_data.dat")
        assert oft.get_default_base_name() == "test_data"

        # Test get_default_base_name with fallback to "job" when both are empty
        self.notebook.general_tab.set_job_name("")
        self.notebook.general_tab.set_data_file("")
        assert oft.get_default_base_name() == "job"

        # Restore original values
        oft.set_all(
            original_values["posac"], original_values["lsa1"], original_values["lsa2"]
        )
        self.notebook.general_tab.set_job_name("")
        self.notebook.general_tab.set_data_file("")

    def test_navigation(self):
        # Test: Check initial page
        assert self.gui.navigator.cur_page == -1

        # Test: Navigate to next page
        self.gui.navigator.next_page()
        assert self.gui.navigator.cur_page == 0

        # Test: Navigate to previous page
        self.gui.navigator.prev_page()
        assert self.gui.navigator.cur_page == -1

        # Test: Navigate to a specific page
        for i in range(3):
            self.gui.navigator.next_page()
        assert self.gui.navigator.cur_page == 2

        # Test 5: Navigate through the traits
        traits_num = 3
        self.add_external_variables(3)
        self.gui.navigator.next_page()
        self.gui.navigator.next_page()
        self.notebook.external_variables_ranges_tab.set_traits_num(traits_num)
        self.gui.navigator.next_page()
        for _ in range(traits_num - 1):
            self.gui.navigator.next_tab_clicked()
            assert self.gui.navigator.cur_page == self.gui.navigator.traits_tab_num
        self.gui.navigator.next_page()
        assert self.gui.navigator.cur_page == self.gui.navigator.traits_tab_num + 1
        for _ in range(traits_num - 1):
            self.gui.navigator.prev_tab_clicked()
            assert self.gui.navigator.cur_page == self.gui.navigator.traits_tab_num

        self.gui.navigator.next_page()
        # Test: Navigate beyond the last page
        for _ in range(5):
            self.gui.navigator.next_page()
        assert self.gui.navigator.cur_page == self.gui.navigator.max_page
        # Test: Navigate before the first page
        for _ in range(10 + traits_num):
            self.gui.navigator.prev_page()
        assert self.gui.navigator.cur_page == -1
        # Test 7: Navigate between the external var tabs
        # No external variables
        self.gui.navigator.set_page(3)
        self.notebook.clear_external_variables()
        self.gui.navigator.next_page()
        assert self.gui.navigator.cur_page == 6
        self.gui.navigator.prev_page()
        assert self.gui.navigator.cur_page == 3
        #
        # Test 8: Navigate between the external var tabs
        # With external variables
        self.add_external_variables(3)
        self.gui.navigator.set_page(3)
        self.gui.navigator.next_page()
        assert self.gui.navigator.cur_page == 4
        self.gui.navigator.prev_page()
        assert self.gui.navigator.cur_page == 3

    def test_internal_recoding_tab(self):
        """Test internal recoding tab basic functionality"""
        self.notebook.select(3)  # Select internal recoding tab
        rt = self.notebook.internal_recoding_tab

        # Test adding operations
        rt.set_recoding_num(2)
        assert len(rt._recoding_operations) == 2, "Should have 2 recoding operations"

        # Set up first operation
        rt.set_variables(1)
        rt.add_pair("1", "2")
        rt.add_pair("3", "4")
        rt.invert_var.set(True)

        # Verify first operation state
        op1 = rt._recoding_operations[0]
        assert op1.selected_variables == ["1"], (
            "First operation should target variable 1"
        )
        assert ("1", "2") in op1.recoding_pairs, "Should contain 1->2 recoding pair"
        assert ("3", "4") in op1.recoding_pairs, "Should contain 3->4 recoding pair"
        assert op1.invert, "Should be inverted"
        rt.reset_default()
        assert not rt._recoding_operations

    def test_internal_recoding_tab_switching(self):
        """Test that operation data persists when switching between operations"""
        self.notebook.select(3)  # Select internal recoding tab
        rt = self.notebook.internal_recoding_tab

        # Setup: Create 2 operations
        rt.set_recoding_num(2)
        assert len(rt._recoding_operations) == 2, "Should have 2 recoding operations"

        # Set up first operation
        rt.set_variables(1)
        rt.add_pair("1", "2")
        rt.add_pair("3", "4")
        rt.invert_var.set(True)

        # Switch to second operation and set it up
        rt.select_operation(2)
        rt.set_variables("2,3")
        rt.add_pair("5", "6")
        rt.invert_var.set(False)

        # Switch back to first operation and verify state persisted
        rt.select_operation(1)
        assert rt.var_index_entry.get() == "1", "Variable selection should be preserved"
        assert len(rt.pair_tree.get_children()) == 2, "Should have 2 pairs"
        assert not rt.invert_var.get(), "Invert state should be false"
        rt.reset_default()
        assert not rt._recoding_operations

    def test_internal_recoding_tab_remove_operation(self):
        """Test that operation data persists when removing operations"""
        self.notebook.select(3)  # Select internal recoding tab
        rt = self.notebook.internal_recoding_tab

        # Setup: Create 3 operations
        rt.set_recoding_num(3)
        assert len(rt._recoding_operations) == 3, "Should have 3 recoding operations"

        # Set up operation 1
        rt.set_variables(1)
        rt.add_pair("1", "2")
        rt.add_pair("3", "4")
        rt.invert_var.set(True)

        # Switch to operation 3 and remove it
        rt.select_operation(3)
        rt._remove_current_operation()

        # Verify operation 1 state is preserved
        rt.select_operation(1)
        assert rt.var_index_entry.get() == '1', "Variable selection should be preserved"
        assert len(rt.pair_tree.get_children()) == 2, "Should have 2 pairs"
        assert not rt.invert_var.get(), "Invert state should be False"
        rt.reset_default()
        assert not rt._recoding_operations

if __name__ == '__main__':
    a = GuiTest()
    try:
        # Run all test methods in order
        a.test_general_tab()
        a.test_zero_option()
        a.test_internal_variables_tab()
        a.test_external_variables_tab()
        a.test_external_variables_ranges_tab()
        a.test_traits_tab()
        a.test_traits_tab_data_persistence()
        a.test_posacsep_tab()
        a.test_output_tab()
        a.test_navigation()
        a.test_internal_recoding_tab()
        a.test_internal_recoding_tab_switching()
        a.test_internal_recoding_tab_remove_operation()
        exit(0)
    except Exception as e:
        # a.run_process()
        raise e

