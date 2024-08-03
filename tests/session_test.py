from lib.controller.controller import Controller
from lib.utils import p_POSAC_DRV
from tests.utils import are_files_identical

class SessionTest(Controller):
    def __init__(self):
        super().__init__()
    def load_test(self):
        # Simple Test
        simple_test_mpm = r'C:\Users\Raz_Z\Projects\Shmuel\posac\tests\scenarios\simple.mpm'
        simple_test_drv = r"C:\Users\Raz_Z\Projects\Shmuel\posac\tests" \
                          r"\simple_test\results\posainp.DRV"
        self.load_session(simple_test_mpm)
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
