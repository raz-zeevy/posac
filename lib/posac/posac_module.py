import os
import subprocess
from contextlib import contextmanager
from typing import List, Dict

from lib.posac.posac_input_writer import PosacInputWriter
from lib.utils import *

NO_POSACSEP = """
STOP POSAC Completed
STOP LSA1 Completed
STOP LSA2 Completed
At line 263 of file POSACSEP.FOR (unit = 5, file = 'stdin')
Fortran runtime error: End of file

Error termination. Backtrace:

Could not print backtrace: libbacktrace could not find executable to open
#0  0x433a93
#1  0x42c3be
#2  0x4289c2
#3  0x42dbdf
#4  0x43eb70
#5  0x42e61d
#6  0x446f8e
#7  0x404b3a
#8  0x4055b5
#9  0x405dd3
#10  0x401232


Process finished with exit code 0"""

@contextmanager
def cwd(path):
    oldpwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(oldpwd)


class PosacModule:
    def __init__(self):
        self.posacsep = [2] * 8  # Example list, replace with actual values
        # self.posacsep = []

    def create_files(self,
                     job_name: str,
                     num_variables: int,
                     idata: int,
                     lowfreq: int,
                     missing: int,
                     ipower: int,
                     itemdplt: int,
                     nlab: int,
                     nxt: int,
                     map_: int,
                     iextdiag: int,
                     itable: int,
                     initx: int,
                     iboxstrng: int,
                     iff: int,
                     itrm: int,
                     iwrtfls: int,
                     ifshmr: int,
                     ifrqone: int,
                     variables_details: list,
                     min_category: int = None,
                     max_category: int = None,
                     nd1: int = None,
                     nd2: int = None,
                     ext_var_ranges: List[List[int]] = None,
                     traits: List[Dict[str, List[List[int]]]] = None,
                     init_approx_format: str = None,
                     init_approx: List[List[float]] = None,
                     boxstring: str = None,
                     form_feed: str = None,
                     shemor_directives: List[str] = None):
        input_writer = PosacInputWriter()
        input_writer.create_posac_input_file(job_name=job_name,
                                             num_variables=num_variables,
                                             idata=idata,
                                             lowfreq=lowfreq,
                                             missing=missing,
                                             ipower=ipower,
                                             itemdplt=itemdplt,
                                             nlab=nlab,
                                             nxt=nxt,
                                             map_=map_,
                                             iextdiag=iextdiag,
                                             itable=itable,
                                             initx=initx,
                                             iboxstrng=iboxstrng,
                                             iff=iff,
                                             itrm=itrm,
                                             iwrtfls=iwrtfls,
                                             ifshmr=ifshmr,
                                             ifrqone=ifrqone,
                                             variables_details=variables_details,
                                             min_category=min_category,
                                             max_category=max_category,
                                             nd1=nd1,
                                             nd2=nd2,
                                             ext_var_ranges=ext_var_ranges,
                                             traits=traits,
                                             init_approx_format=init_approx_format,
                                             init_approx=init_approx,
                                             boxstring=boxstring,
                                             form_feed=form_feed,
                                             shemor_directives=shemor_directives)
    def run(self, data_file : str,
            posac_out: str,
            lsa1_out,
            lsa2_out,
            posacsep):
        """
        The way this function works if there is no posacsep the return code
        will still be 0 but NOPSOACSEP will be printed
        :return:
        """
        def get_path(path: str):
            if os.path.exists(path):
                return os.path.abspath(path)
            else:
                return SCRIPT_NESTING_PREFIX + path
        posac_input_drv_file = p_POSAC_DRV
        # Define the command and arguments
        arguments = [
            get_path(posac_input_drv_file),  # A file in a specific format (see
            # fssainp.drv
            # instructions file) that tells the program how to read data file and
            # what you want done.
            data_file,
            # Path and filename of the input data file in ASCII (simple txt
            # file). You can change it to fit with your own directory, and you
            # can simplify
            # filename. For example, c:\tstfssa\tstdata.dat
            posac_out,  # Path and filename of the output
            # data file. You can change it to your own directory, and simplify
            # filename. For example  c:\tstfssa\tstdata.fss
            lsa1_out,
            lsa2_out
        ]
        # command = r"C:\Users\Raz_Z\Desktop\shmuel-project\fssa-21\FASSA.BAT"
        command = "PXPOS.BAT"

        # Combine the command and arguments into a single list
        full_command = [command] + arguments

        # Run the command
        posac_dir = get_script_dir_path()
        posacsep = [2] * 8
        with cwd(posac_dir):
            process = subprocess.Popen(full_command,
                                    shell=True,
                                     stdin=subprocess.PIPE,
                                    # stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    text=True)
            input_data = "\n".join(map(str, posacsep)) + "\n"
            print("Input data:", input_data)
            try:
                stdout, stderr = process.communicate(input=input_data, timeout=15)
            except subprocess.TimeoutExpired:
                process.kill()
                stdout, stderr = process.communicate()
            # Print the output and error, if any
            if process.returncode != 0:
                raise Exception(f"POSAC script failed : {process.stderr}")
            # if RESULTS_SUCCESS_STDERR in stderr:
            #     if len(process.stderr.split("\n")) >= 3:
            #         if process.stderr.split("\n")[
            #             2] == 'Fortran runtime error: ' \
            #                   'Cannot write to file opened for READ':
            #             exception = stderr.split('\n')[2]
            #             raise Exception(exception)
            #     else:
            #         raise Exception(f"POSAC script failed : {stderr}")
            # else:
            #     raise Exception(f"POSAC script failed : {stderr}")
            print("Output:", stdout)
            print("Error:", stderr)

    def run_2(self, data_file : str,
            posac_out: str,
            lsa1_out,
            lsa2_out,
            posacsep):
        """
        The way this function works if there is no posacsep the return code
        will still be 0 but NOPSOACSEP will be printed
        :return:
        """
        def get_path(path: str):
            if os.path.exists(path):
                return os.path.abspath(path)
            else:
                return SCRIPT_NESTING_PREFIX + path

        posac_input_drv_file = p_POSAC_DRV
        # Define the command and arguments
        arguments = [
            get_path(posac_input_drv_file),  # A file in a specific format (see
            # fssainp.drv
            # instructions file) that tells the program how to read data file and
            # what you want done.
            data_file,
            # Path and filename of the input data file in ASCII (simple txt
            # file). You can change it to fit with your own directory, and you
            # can simplify
            # filename. For example, c:\tstfssa\tstdata.dat
            posac_out,  # Path and filename of the output
            # data file. You can change it to your own directory, and simplify
            # filename. For example  c:\tstfssa\tstdata.fss
            lsa1_out,
            lsa2_out
        ]
        # command = r"C:\Users\Raz_Z\Desktop\shmuel-project\fssa-21\FASSA.BAT"
        command = "PXPOS.BAT"

        # Combine the command and arguments into a single list
        full_command = [command] + arguments

        # Run the command
        posac_dir = get_script_dir_path()
        with cwd(posac_dir):
            result = subprocess.run(full_command)
            if result.returncode == 0:
                print("Command succeeded:", result.stdout)
            else:
                print("Command failed with error:", result.stderr)

if __name__ == '__main__':
    """
    """
    posac = PosacModule()
    posac.run(r"C:\Users\Raz_Z\Projects\Shmuel\posac\tests\simple_test"
              r"\results\KEDDIR2.DAT",
              "C:\\Users\\Raz_Z\\Desktop\\shmuel-project\\shared\\job1.pos",
                "C:\\Users\\Raz_Z\\Desktop\\shmuel-project\\shared\\job1.ls1",
                "C:\\Users\\Raz_Z\\Desktop\\shmuel-project\\shared\\job1.ls2",
              [2]*8)
