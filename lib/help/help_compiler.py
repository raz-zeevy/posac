import logging
import pickle
import re
from pathlib import Path
from lib.help.posac_help import BIN_PATH
POSAC_HELP_FILE = Path(BIN_PATH).parent / "posac.txt"

#INIT LOGGER
logger = logging.getLogger(__name__)


def parse_help_file(filepath=POSAC_HELP_FILE):
    with open(filepath, "r", encoding="latin1") as file:
        raw_text = file.read()

    sections = {}
    section_pattern = re.compile(r"# \$ k (.+?)\n(.*?)\n(?=# \$ k |$)", re.DOTALL)
    matches = section_pattern.findall(raw_text)

    for title, content in matches:
        # Replace <b> tags with a structure to denote bold formatting
        sections[title.strip()] = content.strip()

    return sections

def compile_help_file(input_file=POSAC_HELP_FILE, output_file=BIN_PATH):
    sections = parse_help_file(input_file)
    with open(output_file, "wb") as bin_file:
        pickle.dump(sections, bin_file)
    print(f"Help file compiled successfully and saved to {output_file}")

if __name__ == "__main__":
    compile_help_file()
