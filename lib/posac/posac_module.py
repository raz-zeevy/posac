import os
import subprocess
from contextlib import contextmanager
from logging import getLogger
from typing import Dict, List

from lib.gui.tabs.internal_recoding_tab import RecodingOperation
from lib.posac.data_loader import create_posac_data_file
from lib.posac.data_loader import load_other_formats as load_data_manual
from lib.posac.posac_input_writer import PosacInputWriter
from lib.posac.recoding import apply_recoding
from lib.utils import *

logger = getLogger(__name__)

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

class PosacDataError(Exception):
    """Custom exception for POSAC data handling errors"""
    pass

class PosacModule:
    def __init__(self):
        self.posacsep = [2] * 8  # Example list, replace with actual values
        # self.posacsep = []

    def prepare_data_file(self, data_file: str,
                          lines_per_var,
                          manual_format,
                          recoding_operations: List[RecodingOperation]):
        """Prepare data files for POSAC analysis.

        Creates two files if recoding is applied:
        - POSACDATA_ORG.DAT: Original data without recoding
        - POSACDATA.DAT: Data after applying recoding operations

        Raises:
            PosacDataError: If there are issues with data loading or file creation
            ValueError: If input parameters are invalid
        """
        try:
            # First load the data
            data_matrix = load_data_manual(
                data_file,
                lines_per_var=lines_per_var,
                manual_format=manual_format,
                safe_mode=False,
            )

            # If we have recoding operations, save both original and recoded data
            if recoding_operations:
                try:
                    create_posac_data_file(data_matrix, p_DATA_FILE_ORG)
                    recoded_matrix = apply_recoding(data_matrix, recoding_operations)
                    create_posac_data_file(recoded_matrix, p_DATA_FILE)
                except (ValueError, IOError) as e:
                    raise PosacDataError(
                        f"Failed to apply recoding or save files: {str(e)}"
                    )
            else:
                try:
                    # Just save the original data
                    create_posac_data_file(data_matrix, p_DATA_FILE)
                except IOError as e:
                    raise PosacDataError(f"Failed to save data file: {str(e)}")

        except Exception as e:
            raise PosacDataError(f"Error preparing data files: {str(e)}")

    def create_files(
        self,
        data_file: str,
        lines_per_var: int,
        recoding_operations: List[str],
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
        shemor_directives_key: str = None,
        record_length: int = None,
    ):
        if not os.path.exists(RUN_FILES_DIR):
            os.makedirs(RUN_FILES_DIR)
        input_writer = PosacInputWriter()
        self.prepare_data_file(
            data_file, lines_per_var, variables_details, recoding_operations
        )
        input_writer.create_posac_input_file(
            job_name=job_name,
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
            shemor_directives_key=shemor_directives_key,
            record_length=record_length,
        )

    def run(self, posac_out: str,
            lsa1_out : str,
            lsa2_out : str,
            posacsep : List[int],
            posac_axes_out : str = None):
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
        data_file = p_DATA_FILE
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
            lsa2_out,
        ]
        if posac_axes_out:
            arguments.append(posac_axes_out)
        # command = r"C:\Users\Raz_Z\Desktop\shmuel-project\fssa-21\FASSA.BAT"
        command = "PXPOS.BAT"

        # Combine the command and arguments into a single list
        full_command = [command] + arguments

        # Run the command
        posac_dir = get_script_dir_path()
        with cwd(posac_dir):
            print("################")
            print("Run Command: " + " ".join(full_command))
            process = subprocess.Popen(
                full_command,
                shell=True,
                stdin=subprocess.PIPE,
                # stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            posac_sep_input = "\n".join(map(str, posacsep)) + "\n"
            print("Input data:\n", posac_sep_input)
            try:
                stdout, stderr = process.communicate(input=posac_sep_input, timeout=15)
            except subprocess.TimeoutExpired:
                process.kill()
                stdout, stderr = process.communicate()
            # Print the output and error, if any
            if process.returncode != 0:
                raise Exception(f"POSAC script failed : {process.stderr}")
            # if not stdout:
            #     raise Exception(
            #         "Something went wrong with the POSAC script, make sure the output paths are vaid paths"
            #     )
            print("Output:", stdout)
            print("Error:", stderr)

    @staticmethod
    def open_running_files_dir():
        run_dir = RUN_FILES_DIR
        if os.path.exists(run_dir):
            os.startfile(run_dir)
        else:
            print(f"Run directory {run_dir} does not exist")

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
