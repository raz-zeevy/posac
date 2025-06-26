import pickle
from typing import Dict

from lib.help.help_window.markup_parser import MarkupParser

BIN_PATH = "lib/help/posac_help.bin"

class HelpProperty:
    """A descriptor that automatically fetches help text for Help class attributes."""
    def __init__(self, help_text):
        self.help_text = help_text

    def __get__(self, obj, objtype=None):
        return PosacHelp[self.help_text]


class Help:
    WELCOME = HelpProperty("Welcome to the Posac program")
    NAME_OF_JOB = HelpProperty("Name of the job")
    INPUT_DATA_FILE = HelpProperty("Input data file")
    LINES_PER_CASE = HelpProperty("Lines Per Case")
    NUMBER_OF_INTERNAL_VARS = HelpProperty("Number of internal variables")
    NUMBER_OF_EXTERNAL_VARS = HelpProperty("Number of external variables")
    ITEM_DIAGRAMS = HelpProperty("Item diagrams")
    EXTERNAL_DIAGRAMS = HelpProperty("external diagrams")
    FREQUENCY = HelpProperty("Frequency")
    STRUCTURAL_POSAC = HelpProperty("Structural Posac")
    DATA_SUBJECTS = HelpProperty("Data Subjects")
    MISSING_VALUE = HelpProperty("Missing value")
    NEXT_COMMAND = HelpProperty("Next command")
    BACK_COMMAND = HelpProperty("Back command")
    RUN_COMMAND = HelpProperty("Run command")
    INTERNAL_VARS = HelpProperty("Internal variables")
    EXTERNAL_VARS = HelpProperty("External variables")
    EXTERNAL_VARS_RANGES = HelpProperty("External variables ranges")
    EXTERNAL_TRAITS = HelpProperty("External Traits")
    POSAC_AXES = HelpProperty("Posac axes")
    GRAPHIC_CHARS = HelpProperty("Graphic characters")
    FORMFEED = HelpProperty("formfeed")
    BALANCING_WEIGHTS = HelpProperty("Balancing weights")
    ITERATIONS_NUMBER = HelpProperty("Iterations number")
    ASCII_OUTPUT_FILES = HelpProperty("ASCII output files")
    POSACSEP_OPTION = HelpProperty("POSACSEP Option")
    POSACSEP_THRESHOLDS = HelpProperty("POSACSEP thresholds")
    VIEWING_RESULTS = HelpProperty("Viewing Results")
    HANDLING_RESULT_FILES = HelpProperty("Handling Result Files")
    OUTPUT_FILES = HelpProperty("Output Files")
    RECODE_FUNCTION = HelpProperty("Recode Function")


class PosacHelp:
    _sections: Dict[str, str] = None
    parser = MarkupParser()

    @classmethod
    def _initialize(cls, filepath=BIN_PATH):
        """Load help data and metadata once and store them at the class level."""
        if cls._sections is None:
            with open(filepath, "rb") as file:
                data = pickle.load(file)
                cls._sections = data

    @classmethod
    def get(cls, section_name, return_dict=True):
        """Fetch help text by section name."""
        cls._initialize()  # Ensure data is loaded
        if return_dict:
            return dict(
                help_title=section_name,
                help_text=cls.strip_for_f1(cls._sections.get(section_name, "Section not found.")),
            )
        else:
            return cls._sections.get(section_name, "Section not found.")

    @staticmethod
    def strip_for_f1(content: str) -> str:
        """Remove markup tags from content for F1 functionality"""
        res = MarkupParser().strip_markup(content)
        # remove everything after "related topics" including it
        res = res.split("Related Topics")[0].replace("\n", " ")
        res = res.replace("<f1_br>", "\n")
        if "<f1_ignore>" in res:
            res = res.split("<f1_ignore>")[0]
        return res


    @staticmethod
    def __class_getitem__(section_name):
        """Enable subscript notation for accessing help sections."""
        return PosacHelp.get(section_name)

    @classmethod
    def get_all_sections(cls):
        """Return a list of all section names."""
        cls._initialize()
        return list(cls._sections.keys())


if __name__ == "__main__":
    # print(PosacHelp.find_by_keyword("posac"))
    print(PosacHelp.get("Balancing weights"))