import pickle
import re

def parse_help_file(filename="posac.txt"):
    with open(filename, "r", encoding="latin1") as file:
        raw_text = file.read()

    sections = {}
    section_pattern = re.compile(r"# \$ k (.+?)\n(.*?)\n(?=# \$ k |$)", re.DOTALL)
    matches = section_pattern.findall(raw_text)

    for title, content in matches:
        # Replace <b> tags with a structure to denote bold formatting
        sections[title.strip()] = content.strip()

    return sections

def compile_help_file(input_file="posac.txt", output_file="posac_help.bin"):
    sections = parse_help_file(input_file)
    with open(output_file, "wb") as bin_file:
        pickle.dump(sections, bin_file)

if __name__ == "__main__":
    compile_help_file()
