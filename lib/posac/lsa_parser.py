import inspect
import json
import warnings

from lib.utils import *

COORDS_ROW = "  ITEM NUMBER         X           Y"
END_BLOCK = '\x0c'
BUFFER = "."


class ParsingError(Exception): pass

class Lsa1Parser:
    def __init__(self, file):
        self.index = 0
        self.rows = file.readlines()
        self.current_row = self.rows[0]
        #
        self.metadata = None
        self.dim_data = {}
        self.models = []
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
                warnings.warn(f"OUTPUT PARSER ERORR: {e} \non {called_function}")

    def next_rows(self, num: int):
        called_function = inspect.stack()[1].function
        for i in range(num):
            self.next_row(called_function=called_function)

    def extract_data(self):
        while self.index < len(self.rows) - 1:
            if COORDS_ROW in self.current_row:
                self.next_rows(2)
                self.out_graph_coords = self.parse_graph_coords()
                break
            self.next_row()

    def parse_graph_coords(self):
        graph_coords = dict(
            index= [],
            x = [],
            y = [],
            labels = [],
        )
        while END_BLOCK not in self.current_row:
            if self.current_row == "\n":
                self.next_row()
                continue
            row = self.current_row.replace("*"," ").replace("\n","")
            row_data = [i for i in row.split("   ") if i.strip()]
            graph_coords['index'].append(int(row_data[0]))
            graph_coords['x'].append(float(row_data[1]))
            graph_coords['y'].append(float(row_data[2]))
            graph_coords['labels'].append(row_data[3])
            if len(row_data) != 4:
                raise ParsingError(f"Expected 4 columns, got {len(row_data)}")
            self.next_row()
        return graph_coords

    def get_output(self):
        return {
            "out_coords": self.out_graph_coords,
        }

def parse_output(file_path):
    with open(file_path, 'r', encoding='latin-1') as file:
        output_parser = Lsa1Parser(file)
    return output_parser.get_output()

if __name__ == '__main__':
    output_path = r"C:\Users\Raz_Z\Projects\Shmuel\posac\tests\simple_test\output\job1.ls1"
    print(json.dumps(parse_output(output_path),
                     sort_keys=True, indent=4))
    output_path = r"C:\Users\Raz_Z\Projects\Shmuel\posac\tests\simple_test" \
                  r"\output\job1.ls2"
    print(json.dumps(parse_output(output_path),
                     sort_keys=True, indent=4))
    print("done")
