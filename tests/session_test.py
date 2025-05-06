import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib.controller.controller import Controller
from lib.utils import SET_MODE_DEV

SET_MODE_DEV()


class SessionTest(Controller):
    def __init__(self):
        super().__init__()

    def load_test(self):
        # Simple Test
        simple_test_mpm = r"C:\Users\raz3z\Projects\Shmuel\posac\tests\simple_test\simple_test.session"
        simple_test_drv = (
            r"C:\Users\raz3z\Projects\Shmuel\posac\tests\simple_test\posainp.DRV"
        )
        self.load_session(simple_test_mpm)

        # Verify recoding operations were loaded correctly
        recoding_ops = self.gui.notebook.internal_recoding_tab.get_operations_values()
        assert len(recoding_ops) == 3, "Should have 3 recoding operations"
        # Check first operation (Variable 1)
        assert recoding_ops[0]["selected_variables"] == 1, (
            "First operation should be for variable 1"
        )
        assert ("1", "1") in recoding_ops[0]["recoding_pairs"], (
            "Should have 1->1 recoding"
        )
        assert ("2", "2") in recoding_ops[0]["recoding_pairs"], (
            "Should have 2->2 recoding"
        )

        # Check second operation (Variable 2)
        assert recoding_ops[1]["selected_variables"] == 2, (
            "Second operation should be for variable 2"
        )
        assert ("2", "2") in recoding_ops[1]["recoding_pairs"], (
            "Should have 2->2 recoding"
        )
        assert ("3", "3") in recoding_ops[1]["recoding_pairs"], (
            "Should have 3->3 recoding"
        )

        # Check third operation (Variable 3)
        assert recoding_ops[2]["selected_variables"] == "3", (
            "Third operation should be for variable 3"
        )
        assert ("3", "3") in recoding_ops[2]["recoding_pairs"], (
            "Should have 3->3 recoding"
        )
        assert ("4", "4") in recoding_ops[2]["recoding_pairs"], (
            "Should have 4->4 recoding"
        )
        self.run_posac()

if __name__ == '__main__':
    a = SessionTest()
    a.load_test()
    a.run_process()
