from lib.controller.controller import Controller
from lib.utils import p_POSAC_DRV
from tests.utils import are_files_identical

class SessionTest(Controller):
    def __init__(self):
        super().__init__()
        
    def load_test(self):
        # Simple Test
        simple_test_mpm = r'C:\Users\Raz_Z\Projects\Shmuel\posac\tests\scenarios\simple.mpm'
        simple_test_drv = r"C:\Users\Raz_Z\Projects\Shmuel\posac\tests\simple_test\results\posainp.DRV"
        self.load_session(simple_test_mpm)
        
        # Verify recoding operations were loaded correctly
        recoding_ops = self.gui.notebook.internal_recoding_tab.get_operations_values()
        assert len(recoding_ops) == 3, "Should have 3 recoding operations"
        
        # Check first operation
        assert recoding_ops[0]['selected_variables'] == ['1'], "First operation should be for variable 1"
        assert ('1', '1') in recoding_ops[0]['recoding_pairs'], "Should have 1->1 recoding"
        assert ('0', '0') in recoding_ops[0]['recoding_pairs'], "Should have 0->0 recoding"
        
        # Check second operation
        assert recoding_ops[1]['selected_variables'] == ['2'], "Second operation should be for variable 2"
        assert ('1', '1') in recoding_ops[1]['recoding_pairs']
        assert ('0', '0') in recoding_ops[1]['recoding_pairs']
        
        # Check third operation
        assert recoding_ops[2]['selected_variables'] == ['3'], "Third operation should be for variable 3"
        assert ('1', '1') in recoding_ops[2]['recoding_pairs']
        assert ('0', '0') in recoding_ops[2]['recoding_pairs']
        
        self.run_posac()
        assert are_files_identical(p_POSAC_DRV,simple_test_drv)
        # Jneeds
        jneeds_test_mpm = r'C:\Users\Raz_Z\Projects\Shmuel\posac\tests\scenarios\jneeds.mpm'
        jnees_drv = r"C:\Users\Raz_Z\Projects\Shmuel\posac\tests\jneeds\posainp.drv"
        self.load_session(jneeds_test_mpm)
        self.run_posac()
        assert are_files_identical(p_POSAC_DRV,jnees_drv)

if __name__ == '__main__':
    a = SessionTest()
    a.load_test()
    a.run_process()
