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
        assert not tt._showing_traits, "Should not be showing traits"
        assert tt.get_traits_num() == 0, "Should have 0 traits"
        assert not tt.get_traits(), "Traits list should be empty"

    def test_traits_tab(self):
        from lib.gui.components.ranges_table import RangesTable
        self.notebook.select(5)
        tt = self.notebook.traits_tab
        # default values test
        self.assert_no_traits()
        # adding variables and traits test
        num_traits_1 = 12
        num_ex_var_1 = 30
        self.add_external_variables(num_ex_var_1)
        self.notebook.external_variables_ranges_tab.set_traits_num(num_traits_1)
        assert tt._showing_traits, "Should be showing traits"
        cur_traits = tt.get_traits()
        # Verify correct number of traits created
        assert len(cur_traits) == num_traits_1, f"Expected {num_traits_1} traits, got {len(cur_traits)}"
        # Verify each trait has correct label and number of ext vars
        for i, trait in enumerate(cur_traits):
            assert trait.label == f"trait{i + 1}", f"Trait {i+1} has wrong label"
            assert len(trait.data) == num_ex_var_1, f"Trait {i+1} has wrong number of ext vars"
        # reset traits test
        self.notebook.external_variables_ranges_tab.set_traits_num(0)
        self.notebook.external_variables_ranges_tab.set_traits_num(num_traits_1)
        cur_traits = tt.get_traits()
        assert len(cur_traits) == num_traits_1, "Traits count wrong after reset"
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
        self.add_external_variables(num_ex_var_2)
        self.notebook.external_variables_ranges_tab.set_traits_num(num_traits_2)
        for i in range(num_traits_2):
            tt.set_trait(
                i + 1,
                label=f"test_trait{i * 5 + 1}",
                data=[[str(i + 1), "1-9"] for _ in range(num_ex_var_2)],
            )
        # Verify all traits have correct data
        result_traits = tt.get_traits()
        for i in range(num_traits_2):
            assert result_traits[i].label == f"test_trait{i * 5 + 1}", \
                f"Trait {i+1} label wrong"
            assert result_traits[i].data[0][0] == str(i + 1), \
                f"Trait {i+1} first ext var has wrong count"
        tt.reset_default()
        self.gui.notebook.clear_external_variables()

    def test_traits_tab_data_persistence(self):
        """Test that trait data persists when adding/removing external variables"""
        self.notebook.select(5)
        tt = self.notebook.traits_tab

        # Setup: 1 trait, 1 external variable
        self.add_external_variables(1)
        self.notebook.external_variables_ranges_tab.set_traits_num(1)

        # Edit the trait table UI directly (simulating user input)
        # set_range expects [range1, range2, ...] and prepends the count automatically
        tt.traits_table.set_range(0, ['2-6'])

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

    def test_traits_switching_via_combobox(self):
        """Test that trait data persists when switching traits using the combobox dropdown"""
        tt = self.notebook.traits_tab

        # Setup: 3 traits, 2 external variables
        self.add_external_variables(2)
        self.notebook.external_variables_ranges_tab.set_traits_num(3)
        self.gui.navigator.set_page(self.gui.navigator.traits_tab_num)

        # Set unique data for trait 1
        # Note: set_range expects [range1, range2, ...] - count is prepended automatically
        tt.trait_entry.delete(0, 'end')
        tt.trait_entry.insert(0, 'Trait1_Label')
        tt.traits_table.set_range(0, ['1-3', '5-7'])
        tt.traits_table.set_range(1, ['2-4'])

        # Switch to trait 2 using combobox (simulates _on_trait_num_change)
        tt.traits_num_box.set(2)
        tt._on_trait_num_change(type('Event', (), {'widget': tt.traits_num_box})())

        # Set unique data for trait 2
        tt.trait_entry.delete(0, 'end')
        tt.trait_entry.insert(0, 'Trait2_Label')
        tt.traits_table.set_range(0, ['4-6'])
        tt.traits_table.set_range(1, ['7-9'])

        # Switch back to trait 1 using combobox
        tt.traits_num_box.set(1)
        tt._on_trait_num_change(type('Event', (), {'widget': tt.traits_num_box})())

        # Verify trait 1 data persisted
        assert tt.trait_entry.get() == 'Trait1_Label', \
            f"Trait 1 label lost! Expected 'Trait1_Label', got '{tt.trait_entry.get()}'"
        assert tt.traits_table.get_ranges_for_variable(0) == ['1-3', '5-7'], \
            f"Trait 1 ext var 0 ranges lost!"
        assert tt.traits_table.get_ranges_for_variable(1) == ['2-4'], \
            f"Trait 1 ext var 1 ranges lost!"

        # Switch to trait 2 and verify its data persisted
        tt.traits_num_box.set(2)
        tt._on_trait_num_change(type('Event', (), {'widget': tt.traits_num_box})())

        assert tt.trait_entry.get() == 'Trait2_Label', \
            f"Trait 2 label lost! Expected 'Trait2_Label', got '{tt.trait_entry.get()}'"
        assert tt.traits_table.get_ranges_for_variable(0) == ['4-6'], \
            f"Trait 2 ext var 0 ranges lost!"
        assert tt.traits_table.get_ranges_for_variable(1) == ['7-9'], \
            f"Trait 2 ext var 1 ranges lost!"

        # Cleanup
        self.notebook.clear_external_variables()

    def test_traits_switching_via_navigator(self):
        """
        Test that trait data persists when switching traits using navigator Next/Prev buttons.
        This was the original bug - navigator didn't save before switching.
        """
        tt = self.notebook.traits_tab
        nav = self.gui.navigator

        # Reset navigator to known state
        nav.cur_page = -1

        # Setup: 3 traits, 2 external variables
        self.add_external_variables(2)
        self.notebook.external_variables_ranges_tab.set_traits_num(3)

        # Navigate to traits tab
        nav.set_page(nav.traits_tab_num)
        assert nav.cur_page == nav.traits_tab_num, "Should be on traits tab"
        assert tt._current_trait == 1, "Should start on trait 1"

        # Set unique data for trait 1
        # Note: set_range expects [range1, range2, ...] - count is prepended automatically
        tt.trait_entry.delete(0, 'end')
        tt.trait_entry.insert(0, 'NavTrait1')
        tt.traits_table.set_range(0, ['1-2'])
        tt.traits_table.set_range(1, ['3-4'])

        # Switch to trait 2 using NAVIGATOR NEXT button
        nav.next_tab_clicked()
        assert tt._current_trait == 2, "Should be on trait 2"

        # Set unique data for trait 2
        tt.trait_entry.delete(0, 'end')
        tt.trait_entry.insert(0, 'NavTrait2')
        tt.traits_table.set_range(0, ['5-6'])
        tt.traits_table.set_range(1, ['7-8'])

        # Switch to trait 3 using NAVIGATOR NEXT button
        nav.next_tab_clicked()
        assert tt._current_trait == 3, "Should be on trait 3"

        # Set unique data for trait 3
        tt.trait_entry.delete(0, 'end')
        tt.trait_entry.insert(0, 'NavTrait3')
        tt.traits_table.set_range(0, ['2-3'])
        tt.traits_table.set_range(1, ['4-5'])

        # Now switch BACK to trait 2 using NAVIGATOR PREV button
        nav.prev_tab_clicked()
        assert tt._current_trait == 2, "Should be back on trait 2"

        # CRITICAL: Verify trait 2 data persisted after navigator switch
        assert tt.trait_entry.get() == 'NavTrait2', \
            f"Trait 2 label lost via navigator! Expected 'NavTrait2', got '{tt.trait_entry.get()}'"
        assert tt.traits_table.get_ranges_for_variable(0) == ['5-6'], \
            f"Trait 2 ext var 0 ranges lost via navigator! Got {tt.traits_table.get_ranges_for_variable(0)}"
        assert tt.traits_table.get_ranges_for_variable(1) == ['7-8'], \
            f"Trait 2 ext var 1 ranges lost via navigator! Got {tt.traits_table.get_ranges_for_variable(1)}"

        # Switch back to trait 1 and verify
        nav.prev_tab_clicked()
        assert tt._current_trait == 1, "Should be back on trait 1"
        assert tt.trait_entry.get() == 'NavTrait1', \
            f"Trait 1 label lost via navigator! Expected 'NavTrait1', got '{tt.trait_entry.get()}'"
        assert tt.traits_table.get_ranges_for_variable(0) == ['1-2'], \
            f"Trait 1 ext var 0 ranges lost via navigator!"
        assert tt.traits_table.get_ranges_for_variable(1) == ['3-4'], \
            f"Trait 1 ext var 1 ranges lost via navigator!"

        # Navigate forward through all traits and verify trait 3
        nav.next_tab_clicked()  # to trait 2
        nav.next_tab_clicked()  # to trait 3
        assert tt._current_trait == 3, "Should be on trait 3"
        assert tt.trait_entry.get() == 'NavTrait3', \
            f"Trait 3 label lost! Expected 'NavTrait3', got '{tt.trait_entry.get()}'"
        assert tt.traits_table.get_ranges_for_variable(0) == ['2-3'], \
            f"Trait 3 ext var 0 ranges lost!"

        # Cleanup
        self.notebook.clear_external_variables()
        nav.cur_page = -1
        nav.show_first_page()

    def test_traits_multiple_rapid_switches(self):
        """Test data integrity with multiple rapid back-and-forth switches"""
        tt = self.notebook.traits_tab
        nav = self.gui.navigator

        # Reset navigator to known state
        nav.cur_page = -1

        # Setup: 3 traits, 2 external variables
        self.add_external_variables(2)
        self.notebook.external_variables_ranges_tab.set_traits_num(3)
        nav.set_page(nav.traits_tab_num)

        # Set data for all 3 traits
        # Format: (label, [ranges for ext var 0], [ranges for ext var 1])
        test_data = [
            ('Label_A', ['1-1'], ['2-2']),
            ('Label_B', ['3-3'], ['4-4']),
            ('Label_C', ['5-5'], ['6-6']),
        ]

        for i, (label, range0, range1) in enumerate(test_data):
            tt.select_trait(i + 1)
            tt.trait_entry.delete(0, 'end')
            tt.trait_entry.insert(0, label)
            tt.traits_table.set_range(0, range0)
            tt.traits_table.set_range(1, range1)

        # Rapid switching: 1 -> 2 -> 3 -> 2 -> 1 -> 3 -> 1 -> 2
        switch_sequence = [2, 3, 2, 1, 3, 1, 2]
        for target in switch_sequence:
            if tt._current_trait < target:
                while tt._current_trait < target:
                    nav.next_tab_clicked()
            else:
                while tt._current_trait > target:
                    nav.prev_tab_clicked()

        # Final verification: check all 3 traits have correct data
        for i, (label, range0, range1) in enumerate(test_data):
            tt.select_trait(i + 1)
            assert tt.trait_entry.get() == label, \
                f"Trait {i+1} label corrupted after rapid switches! Expected '{label}', got '{tt.trait_entry.get()}'"
            actual_range0 = tt.traits_table.get_ranges_for_variable(0)
            assert actual_range0 == range0, \
                f"Trait {i+1} ext var 0 corrupted! Expected {range0}, got {actual_range0}"

        # Cleanup
        self.notebook.clear_external_variables()
        nav.cur_page = -1
        nav.show_first_page()

    def test_traits_edit_then_page_change(self):
        """Test that trait data is saved when navigating away from traits tab entirely"""
        tt = self.notebook.traits_tab
        nav = self.gui.navigator

        # Reset navigator to known state
        nav.cur_page = -1

        # Setup: 2 traits, 1 external variable
        self.add_external_variables(1)
        self.notebook.external_variables_ranges_tab.set_traits_num(2)
        nav.set_page(nav.traits_tab_num)

        # Edit trait 1
        # Note: set_range expects [range1, range2, ...] - count is prepended automatically
        tt.trait_entry.delete(0, 'end')
        tt.trait_entry.insert(0, 'EditedTrait1')
        tt.traits_table.set_range(0, ['2-5'])

        # Switch to trait 2 within same page
        nav.next_tab_clicked()
        tt.trait_entry.delete(0, 'end')
        tt.trait_entry.insert(0, 'EditedTrait2')
        tt.traits_table.set_range(0, ['6-9'])

        # Navigate to next page (away from traits tab)
        nav.next_tab_clicked()  # This should go to next page since we're on last trait
        assert nav.cur_page > nav.traits_tab_num, "Should have moved past traits tab"

        # Navigate back to traits tab
        nav.set_page(nav.traits_tab_num)

        # Verify both traits have their data
        tt.select_trait(1)
        assert tt.trait_entry.get() == 'EditedTrait1', \
            f"Trait 1 label lost after page change! Got '{tt.trait_entry.get()}'"
        assert tt.traits_table.get_ranges_for_variable(0) == ['2-5'], \
            f"Trait 1 ranges lost after page change!"

        tt.select_trait(2)
        assert tt.trait_entry.get() == 'EditedTrait2', \
            f"Trait 2 label lost after page change! Got '{tt.trait_entry.get()}'"
        assert tt.traits_table.get_ranges_for_variable(0) == ['6-9'], \
            f"Trait 2 ranges lost after page change!"

        # Cleanup
        self.notebook.clear_external_variables()
        nav.cur_page = -1
        nav.show_first_page()

    def test_traits_get_state_saves_current(self):
        """Test that get_state properly saves the currently displayed trait"""
        tt = self.notebook.traits_tab
        nav = self.gui.navigator

        # Reset navigator to known state
        nav.cur_page = -1

        # Setup: 2 traits, 1 external variable
        self.add_external_variables(1)
        self.notebook.external_variables_ranges_tab.set_traits_num(2)
        nav.set_page(nav.traits_tab_num)

        # Edit trait 1
        # Note: set_range expects [range1, range2, ...] - count is prepended automatically
        tt.select_trait(1)
        tt.trait_entry.delete(0, 'end')
        tt.trait_entry.insert(0, 'StateTrait1')
        tt.traits_table.set_range(0, ['1-3'])

        # Edit trait 2
        tt.select_trait(2)
        tt.trait_entry.delete(0, 'end')
        tt.trait_entry.insert(0, 'StateTrait2')
        tt.traits_table.set_range(0, ['4-6'])

        # Get state while on trait 2 (should save trait 2's current UI state)
        state = self.notebook.get_state()
        traits = state['traits']

        # Verify both traits are in state correctly
        assert traits[0].label == 'StateTrait1', \
            f"State doesn't have trait 1 label! Got '{traits[0].label}'"
        assert traits[1].label == 'StateTrait2', \
            f"State doesn't have trait 2 label! Got '{traits[1].label}'"

        # Cleanup
        self.notebook.clear_external_variables()
        # Reset navigator to initial state for subsequent tests
        nav.cur_page = -1
        nav.show_first_page()

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
        rt.select_inversion()  # Use API method instead of invert_var

        # Verify first operation state
        op1 = rt._recoding_operations[0]
        assert op1.selected_variables == 1 or op1.selected_variables == "1", (
            f"First operation should target variable 1, got {op1.selected_variables}"
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
        rt.select_inversion()  # Use API method

        # Switch to second operation and set it up
        rt.select_operation(2)
        rt.set_variables("2,3")
        rt.add_pair("5", "6")
        rt.select_manual_recoding()  # Use API method

        # Switch back to first operation and verify state persisted
        rt.select_operation(1)
        assert rt.var_index_entry.get() == "1", "Variable selection should be preserved"
        assert len(rt.pair_tree.get_children()) == 2, "Should have 2 pairs"
        assert rt.operation_type.get() == "Inversion", "Operation type should be Inversion (from op 1)"
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
        rt.select_inversion()  # Use API method

        # Switch to operation 3 and remove it
        rt.select_operation(3)
        rt._remove_current_operation()

        # Verify operation 1 state is preserved
        rt.select_operation(1)
        assert rt.var_index_entry.get() == '1', "Variable selection should be preserved"
        assert len(rt.pair_tree.get_children()) == 2, "Should have 2 pairs"
        assert rt.operation_type.get() == "Inversion", "Operation type should be Inversion (from op 1)"
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
        a.test_traits_switching_via_combobox()
        a.test_traits_switching_via_navigator()
        a.test_traits_multiple_rapid_switches()
        a.test_traits_edit_then_page_change()
        a.test_traits_get_state_saves_current()
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

