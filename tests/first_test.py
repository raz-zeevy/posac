from lib.controller.controller import Controller

DATA_PATH = "data/first_test_data.csv"


class first_test(Controller):
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
            id_location=(1, 2)
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
        zo.set(
            zero_option=False)
        test_values = zo.get_all()
        zo.set_default()
        assert zo.get_all() == zo.DEFAULT_VALUES
        zo.set(**test_values)
        cur_values = zo.get_all()
        assert test_values == cur_values

    def test_internal_variables_tab(self):
        self.notebook.select(2)
        iv = self.notebook.internal_variables_tab
        iv.remove_variable()
        dummy_vars = [
            [1, 2, 3, 4],
            [1, 2, 3, 4],
            [1, 2, 3, 4],
            [1, 2, 3, 4],
        ]
        for i in range(len(dummy_vars)):
            for j in range(len(dummy_vars[i])):
                dummy_vars[i][j] = str(dummy_vars[i][j])
        first_var = ['10', '5', '3', '8']
        iv.add_variable(first_var, check=False)
        for i in range(len(dummy_vars)):
            iv.add_variable(dummy_vars[i], check=True)
        test_values = iv.get_selected_variables()
        assert test_values == dummy_vars
        test_values = iv.get_all_variables()
        assert test_values == [first_var] + dummy_vars
        iv.clear_variables()
        assert not iv.get_all_variables()
        iv.set_default()
        assert not iv.get_all_variables()

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
        first_var = ['10', '5', '3', '8']
        ev.add_variable(first_var, check=False)
        assert len(ev.get_all_variables()) == 1
        for i in range(len(dummy_vars)):
            ev.add_variable(dummy_vars[i], check=True)
        test_values = ev.get_selected_variables()
        assert test_values == dummy_vars
        test_values = ev.get_all_variables()
        assert len(test_values) == len(dummy_vars) + 1
        assert test_values == [first_var] + dummy_vars
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
            ['1', '1-9', '1-9', '1-3'],
            ['2', '1-3', '1-2', '1-5'],
            ['3', '1-9', '1-9', '1-3']
        ]
        evr.set_range(0, test_values[0])
        evr.set_range(1, test_values[1])
        evr.set_range(2, test_values[2])
        assert evr.get_all_ranges() == test_values
        # Set the number of external traits
        traits_num = 12
        evr.set_traits_num(traits_num)
        assert evr.get_external_traits_num() == traits_num
        #
        all_data = evr.get_all()
        evr.set_default()
        assert evr.get_all_ranges() == [evr.DEFAULT_VALUE] * 3
        evr.set_all(all_data['ranges'], all_data['traits_num'])
        assert evr.get_all() == {
            'ranges': test_values,
            'traits_num': traits_num
        }
        evr.set_default()
        self.notebook.clear_external_variables()

    def assert_no_traits(self):
        tt = self.notebook.traits_tab
        assert tt._context == tt.TabContext.NO_TRAITS
        assert tt.get_current_trait() == 1
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
        self.notebook.external_variables_ranges_tab.set_traits_num(
            num_traits_1)
        assert tt._context == tt.TabContext.TRAITS
        cur_traits = tt.get_traits()
        def_test_traits = [tt.TraitData(f'trait{i + 1}', [
            ['1', '1-9'] for _ in range(num_ex_var_1)])
                           for i in range(num_traits_1)]
        assert cur_traits == def_test_traits
        # reset traits test
        self.notebook.external_variables_ranges_tab.set_traits_num(0)
        self.notebook.external_variables_ranges_tab.set_traits_num(
            num_traits_1)
        assert cur_traits == def_test_traits
        # simple set test
        tt.set_trait(1,
                     label='test_trait',
                     data=[['2', '1-9', '1-3'] if i > 10 else ['1', '1-2']
                           for i in range(num_ex_var_1)
                           ]
                     )
        assert tt.get_traits()[0].label == 'test_trait'
        # clear external variables test
        self.notebook.clear_external_variables()
        self.assert_no_traits()
        # adding complex variables and traits test
        num_traits_2 = 12
        num_ex_var_2 = 20
        test_traits_1 = [
            tt.TraitData(f'test_trait{i * 5 + 1}', [
                ['1', '1-9'] for _ in range(num_ex_var_2)])
            for i in range(num_traits_2)
        ]

        # modify the test_traits_1 to be unique numbers
        for i in range(num_traits_2):
            for j in range(num_ex_var_2):
                test_traits_1[i].data[j][0] = str(i + 1)
        self.add_external_variables(num_ex_var_2)
        self.notebook.external_variables_ranges_tab.set_traits_num(
            num_traits_2)
        for i in range(num_traits_2):
            tt.set_trait(i + 1, label=f'test_trait{i * 5 + 1}',
                         data=[test_traits_1[i].data[j] for j in
                               range(num_ex_var_2)])
        assert tt.get_traits() == test_traits_1
        tt.reset_default()
        self.gui.notebook.clear_external_variables()

    def test_posacsep_tab(self):
        var_num = 10
        self.notebook.select(6)
        pt = self.notebook.posacsep_tab
        self.add_internal_variables(var_num)

        # Test 1: Check set_combo with False
        pt.set_combo(False)
        assert not pt.get_combo()

        # Test 2: Check set_values with different values
        pt.set_values(var_num * [5])
        assert pt.get_values() == var_num * [5]

        # Test 3: Check get_values after set_values
        pt.set_values(var_num * [2])
        assert pt.get_values() == var_num * [2]

        # Test 4: Check reset_to_default()
        pt.reset_to_default()
        assert pt.get_values() == var_num * [pt.DEFAULT_ROW[0]]

    def test_output_tab(self):
        self.notebook.select(7)
        oft = self.notebook.output_files_tab
        # ot.set(
        #     output_file="test_output_file",
        #     output_format="csv",
        #     output_type="all",
        #     output_options="all"
        # )
        # test_values = ot.get_all()
        # ot.set_default()
        # assert ot.get_all() == ot.DEFAULT_VALUES
        # ot.set(**test_values)
        # cur_values = ot.get_all()
        # assert test_values == cur_values


if __name__ == '__main__':
    a = first_test()
    a.test_general_tab()
    a.test_zero_option()
    a.test_internal_variables_tab()
    a.test_external_variables_tab()
    a.test_external_variables_ranges_tab()
    a.test_traits_tab()
    a.test_posacsep_tab()
    a.test_output_tab()
    a.run_process()
