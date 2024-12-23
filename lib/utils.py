import os
from lib import config

WINDOW_HEIGHT = 635
WINDOW_WIDTH = 860

SESSION_FILE_EXTENSION = "mmp"

def get_window_width():
    return real_size(WINDOW_WIDTH)

def get_window_height():
    return real_size(WINDOW_HEIGHT)

def rreal_size(args):
    return real_size(args, _round=True)

def real_size(args, _round=False):
    """
    This function is used to calculate the real size of the GUI elements
    :param args:
    :param _round:
    :return:
    """
    # get the dpi_ratio from the enviroment
    dpi_ratio = float(os.environ.get('DPI_RATIO', 0))
    if not dpi_ratio:
        if _round:
            return round(args)
        return args
    elif isinstance(args, tuple):
        if _round:
            return tuple([round(arg * dpi_ratio) for arg in args])
        return tuple([arg * dpi_ratio for arg in args])
    elif isinstance(args, (int, float)):
        if _round:
            return round(args * dpi_ratio)
        return args * dpi_ratio
    else:
        raise ValueError(f"Invalid type: {type(args)}")

DELIMITER_1_D = "1-digit"
DELIMITER_2_D = "2-digit"

GROUPING_TYPES = ["Percentile", "Equal Intervals", "By Rank"]

######################
#        FSS         #
######################
# Script paths
p_FSS_DIR = './scripts/IdoPosac'
SCRIPT_PEARSON = "PEARSON"
SCRIPT_MONO = "MONO"

def GET_MODE():
    return os.environ.get('MODE')

def SET_MODE_TEST():
    import os
    os.environ['MODE'] = config.MODE_DEBUG

def SET_MODE_PRODUCTION():
    import os
    os.environ['MODE'] = config.MODE_PRODUCTION

def SET_MODE_NO_VALIDATION():
    import os
    os.environ['MODE'] = config.MODE_NO_VALIDATION

def IS_PRODUCTION():
    return GET_MODE() == config.MODE_PRODUCTION

def IS_NO_VALIDATE():
    return GET_MODE() == config.MODE_NO_VALIDATION

def get_script_dir_path():
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        fss_dir = os.path.join(base_dir, p_FSS_DIR)
    except FileNotFoundError:
        raise FileNotFoundError("FSSA script directory not found")
    return fss_dir


# Output Paths
SCRIPT_NESTING_PREFIX = "..\\..\\..\\"
p_OUTPUT_DIR = "output"
OUTPUT_FILE_NAME = "DJK21.FSS"
p_OUTPUT_FILE = os.path.join(p_OUTPUT_DIR, OUTPUT_FILE_NAME)
P_POSACSEP_DIR = os.path.join(get_script_dir_path(), "POSACSEP.OUT")

# Input paths
RUN_FILES_DIR = "..\\run_files"
RUN_FILES_DIR = os.path.join(get_script_dir_path(), RUN_FILES_DIR)
DRV_IN_NAME = "POSACINP.DRV"
DATA_FILE_NAME = "POSACDATA.DAT"
DATA_FILE_NAME_ORG = "POSACDATA_ORG.DAT"
p_POSAC_DRV = os.path.join(RUN_FILES_DIR, DRV_IN_NAME)
p_DATA_FILE = os.path.join(RUN_FILES_DIR, DATA_FILE_NAME)
p_DATA_FILE_ORG = os.path.join(RUN_FILES_DIR, DATA_FILE_NAME_ORG)
INPUT_MATRIX_FORMAT = "(8F10.7)"
POSAC_SEP_OUT = "POSACSEP.TAB"
POSAC_SEP_PATH = os.path.join(get_script_dir_path(), POSAC_SEP_OUT)
# Results

RESULTS_SUCCESS_STDERR = "STOP SSA terminated successfully."

### Gui

START_PAGE_NAME = "StartPage"
INPUT_PAGE_NAME = "InputPage"
MATRIX_INPUT_PAGE_NAME = "MatrixInputPage"
DATA_PAGE_NAME = "DataPage"
DIMENSIONS_PAGE_NAME = "DimensionsPage"
FACET_PAGE_NAME = "FacetPage"
FACET_VAR_PAGE_NAME = "FacetVarPage"
MANUAL_FORMAT_PAGE_NAME = "ManualFormatPage"
HYPOTHESIS_PAGE_NAME = "HypothesisPage"
FACET_DIM_PAGE_NAME = "FacetDimPage"

########
# Help #
########

help_pages_dict = {
    START_PAGE_NAME: "start_screen",
    INPUT_PAGE_NAME: "recorded_data_screen",
    DATA_PAGE_NAME: "data_screen",
    DIMENSIONS_PAGE_NAME: "dimensions_and_coefficients_screen",
    FACET_PAGE_NAME: "facets_definition_screen",
    FACET_VAR_PAGE_NAME: "variable_elements_in_facets_screen",
    MANUAL_FORMAT_PAGE_NAME: "variable_definition_screen",
    HYPOTHESIS_PAGE_NAME: "hypotheses_screen",
    FACET_DIM_PAGE_NAME: "contents"
}


##################
#   Resources    #
##################

def get_resource(asset_name):
    # Get the directory of the current script file
    script_dir = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(script_dir, "assets", asset_name)
    path = os.path.abspath(path)
    # check
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Resource not found: {path}")
    return path

def get_path(relative_path):
    # Get the directory of the current script file
    script_dir = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(script_dir,".." ,relative_path)
    path = os.path.abspath(path)
    # check
    if not os.path.exists(path):
        raise FileNotFoundError(f"Path not found: {path}")
    return path

##################
#   Exceptions   #
##################

class DataLoadingException(Exception):
    pass
