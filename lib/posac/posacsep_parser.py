import inspect
import json
import warnings

from lib.utils import *

ITEM_START = "ITEM NO.  "
LINES_START = "corners: minimum"
LINE_START = "Dividing line from"


class ParsingError(Exception): pass


class PosacsepParser:
    def __init__(self, file):
        self.index = 0
        self.rows = file.readlines()
        self.current_row = self.rows[0]
        #
        self.items_data = {}
        self.n_item = None
        self.extract_data()

    def next_row(self, called_function=None):
        # get the name of the function that called next_row
        if not called_function:
            called_function = inspect.stack()[1].function
        try:
            self.index += 1
            self.current_row = self.rows[self.index]
        except IndexError as e:
            if IS_PROD():
                pass
            else:
                warnings.warn(
                    f"OUTPUT PARSER ERORR: {e} \non {called_function}")

    def next_rows(self, num: int):
        called_function = inspect.stack()[1].function
        for i in range(num):
            self.next_row(called_function=called_function)

    def extract_data(self):
        while self.index < len(self.rows) - 1:
            if ITEM_START in self.current_row:
                self.n_item = int(
                    self.current_row.split(ITEM_START)[1].strip())
                self.next_row()
                self.parse_item()
            self.next_row()

    def parse_item(self):
        lines = [[]]
        lines_num = 1
        while len(lines[-1]) < 4:
            if LINE_START in self.current_row:
                s = self.current_row.index("(")
                t = self.current_row.index(")") + 1
                start = self.current_row[s:t].strip()
                s = self.current_row[t - 1:].index("(") + (t - 1)
                end = self.current_row[s:].strip()
                try:
                    start = eval(start)
                    end = eval(end)
                except Exception as e:
                    raise ParsingError(f"Failed to parse line: "
                                       f"{self.current_row}, {e}")
                if len(lines[-1]) < lines_num:
                    lines[-1].append((start, end))
                else:
                    lines_num += 1
                    lines.append([(start, end)])
            self.next_row()
        self.items_data[self.n_item] = lines

    def get_output(self):
        return dict(
            item_edges = self.items_data,
            titles = ["POLAR ROLE",
                      "ATOAC ROLE",
                      "PROMO ROLE",
                      "MODIF ROLE"]
        )

def parse_output(file_path):
    with open(file_path, 'r', encoding='latin-1') as file:
        output_parser = PosacsepParser(file)
    return output_parser.get_output()


if __name__ == '__main__':
    output_path = r"C:\Users\Raz_Z\Projects\Shmuel\posac\lib\scripts\IdoPosac\POSACSEP.OUT"
    print(json.dumps(parse_output(output_path),
                     sort_keys=True, indent=4))
    print("done")
