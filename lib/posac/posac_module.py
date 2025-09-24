import os
import subprocess
from contextlib import contextmanager
from logging import getLogger
from typing import Dict, List, Tuple

from lib.gui.tabs.internal_recoding_tab import RecodingOperation
from lib.posac.data_loader import add_apendix_data, create_posac_data_file
from lib.posac.data_loader import load_other_formats as load_data_manual
from lib.posac.posac_input_writer import PosacInputWriter
from lib.posac.posac_output_parser import OutputParser
from lib.posac.recoding import apply_recoding
from lib.utils import *

logger = getLogger(__name__)

FALSE_ERROR = "Note: The following floating-point exceptions are signalling: IEEE_DENORMAL\nSTOP POSAC Completed\nSTOP LSA1 Completed\nSTOP LSA2 Completed\nNote: The following floating-point exceptions are signalling: IEEE_DENORMAL\nSTOP  \n"
FALSE_ERROR_SHORT = "Note: The following floating-point exceptions are signalling: IEEE_DENORMAL\nSTOP 2\n"
FALSE_ERROR_INVALID_FLAG = "Note: The following floating-point exceptions are signalling: IEEE_DENORMAL\nSTOP POSAC Completed\nNote: The following floating-point exceptions are signalling: IEEE_INVALID_FLAG\nSTOP LSA1 Completed\nSTOP LSA2 Completed\nNote: The following floating-point exceptions are signalling: IEEE_DENORMAL\nSTOP  \n"
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
        self.origin_data_file = None
        self.data_matrix = None
        self.failed_rows : List[int] = None

    def prepare_data_file(
        self,
        data_file: str,
        lines_per_var,
        manual_format,
        recoding_operations: List[RecodingOperation],
        appendix_fields: Tuple[int, int],
    ):
        """Prepare data files for POSAC analysis.

        Creates two files if recoding is applied:
        - POSACDATA_ORG.DAT: Original data without recoding
        - POSACDATA.DAT: Data after applying recoding operations

        Args:
            data_file: Path to the data file
            lines_per_var: Number of lines per variable
            manual_format: Manual format of the data
            recoding_operations: List of recoding operations
            appendix_fields: Tuple of the appendix fields (start col, end col) or
              (variable_ix, -1) if it's a csv file

        Raises:
            PosacDataError: If there are issues with data loading or file creation
            ValueError: If input parameters are invalid
        """
        try:
            # First load the data
            data_matrix, appendix_data, failed_rows = load_data_manual(
                data_file,
                lines_per_var=lines_per_var,
                manual_format=manual_format,
                safe_mode=False,
                appendix_fields=appendix_fields,
            )
            self.data_matrix = data_matrix
            self.failed_rows = failed_rows
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
                self.data_matrix = recoded_matrix
            else:
                try:
                    # Just save the original data
                    create_posac_data_file(data_matrix, p_DATA_FILE)
                except IOError as e:
                    raise PosacDataError(f"Failed to save data file: {str(e)}")

            # Add the appendix data to the data_file (case_id / profile_frequencies)
            if appendix_data is not None:
                add_apendix_data(data_path=p_DATA_FILE, appendix_data=appendix_data)

        except Exception as e:
            if IS_DEV():
                raise e
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
        case_id_location: Tuple[int, int] = None,
        subject_type: str = None,
    ):
        self.origin_data_file = data_file
        if not os.path.exists(RUN_FILES_DIR):
            os.makedirs(RUN_FILES_DIR)
        input_writer = PosacInputWriter()
        self.prepare_data_file(
            data_file,
            lines_per_var,
            variables_details,
            recoding_operations,
            case_id_location,
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
            case_id_location=case_id_location,
            subject_type=subject_type,
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

        # if dir doesnt exist, create it
        posac_out_dir = os.path.dirname(posac_out)
        if not os.path.exists(posac_out_dir):
            os.makedirs(posac_out_dir)

        # Run the command
        posac_dir = get_script_dir_path()
        # write full command to the posac_cmd file
        with open(p_POSAC_CMD, "w") as file:
            cmd_command = ["cd ", posac_dir, "&&", " ".join(full_command)]
            file.write(" ".join(cmd_command))


        with cwd(posac_dir):
            print("################")
            print("Run Command: " + " ".join(full_command))
            process = subprocess.Popen(
                full_command,
                shell=True,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
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
            self.process_results(process, stdout, stderr)
            OutputParser.replace_input_data(posac_out, self.origin_data_file)


    def process_results(self, process, stdout, stderr):
        if process.returncode != 0:
            raise Exception(f"POSAC script failed : {process.stderr}")
        if "Cannot write to file opened for READ" in stderr:
            raise Exception(
                "Permission denied in writing to output file. You may change the output file name to a different one,"
                " or alternatively make sure the file is not open in another program, or the "
                "path is valid and accessible."
            )
        elif stderr and stderr not in [FALSE_ERROR, FALSE_ERROR_INVALID_FLAG]:
            print("Error:\n**************\n", stderr)
            raise Exception("See the output file for more details")

    def get_data_matrix(self):
        return self.data_matrix

    def get_failed_rows(self):
        return self.failed_rows

    @staticmethod
    def open_running_files_dir():
        run_dir = RUN_FILES_DIR
        if os.path.exists(run_dir):
            os.startfile(run_dir)
        else:
            print(f"Run directory {run_dir} does not exist")

    @staticmethod
    def get_recoded_data_path():
        return p_DATA_FILE

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
