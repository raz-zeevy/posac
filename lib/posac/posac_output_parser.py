from dataclasses import dataclass
import inspect
import json
import warnings
import re
from typing import List

from lib.utils import *

COORDS_ROW = "ID   PROFILE                                  SCO  FREQ        " \
             "       X         Y               JOINT   LATERAL"
# import numpy as np

END_BLOCK = '\x0c'
BUFFER = "."


class ParsingError(Exception): pass

class OutputParser:

    _instance = None

    def __init__(self, file_path : str):
        self.index = 0
        with open(file_path, 'r', encoding='latin-1') as file:
            self.rows = file.readlines()
        self.current_row = self.rows[0]
        #
        self.metadata = None
        self.dim_data = {}
        self.models = []
        # pre-extract textual sections (independent of cursor)
        self.psc_solution_text = self._extract_psc_solution_text()
        self.psc_mumatrix_text = self._extract_mumatrix_text()
        self.psc_item_fact_text = self._extract_item_factor_text()
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
            profiles = [],
        )
        while not self.current_row == "\n":
            row = self.current_row.replace("*"," ")
            row_data = [i for i in row.split("  ") if i]
            graph_coords['index'].append(int(row_data[0]))
            graph_coords['profiles'].append(row_data[1])
            graph_coords['x'].append(float(row_data[4]))
            graph_coords['y'].append(float(row_data[5]))
            if len(row_data) != 8:
                raise ParsingError(f"Expected 8 columns, got {len(row_data)}")
            self.next_row()
        return graph_coords

    ################
    # TODO: REMOVE #
    ################

    def parse_dimension(self):
        def parse_dimension_info():
            data = {}
            while not self.current_row == "\n":
                row_data = self.parse_data_line_format(self.current_row)
                data.update(row_data)
                self.next_row()
            return data

        def parse_dimension_data():
            data = []
            while not self.end_block_reached():
                row_rdata = self.current_row.split()
                row_data = {
                    "serial_number": int(row_rdata[0]),
                    "distance_from_centroid": float(row_rdata[1]),
                    "coordinates": [float(row_rdata[i]) for i in range(2,
                                                                       len(
                                                                           row_rdata))],
                }
                data.append(row_data)
                self.next_row()
            return data

        self.current_dim = int(self.current_row.strip().split()[-1])
        self.next_rows(3)
        dim_info = parse_dimension_info()
        self.next_rows(4)
        dim_coord = parse_dimension_data()
        dim_info['coordinates'] = dim_coord
        dim_info['dimension'] = self.current_dim
        return dim_info

    def parse_model(self):
        def parse_divide_geom():
            def find_dot_x_y():
                c_s = self.current_row.find("(")
                c_e = self.current_row.find(")")
                return eval(self.current_row[c_s:c_e + 1].replace(" ", ""))

            row = self.current_row.split()
            shape = row[1]
            if shape == "LINE":
                return {
                    "shape": shape,
                    "x": float(row[4][:-2]),
                    "y": float(row[6][:-2]),
                    "n": float(row[8]),
                }
            elif shape == "AXIS":
                center = find_dot_x_y()
                angle = self.current_row.strip()[-7:]
                return {
                    "shape": shape,
                    "center": center,
                    "angle": float(angle),
                }
            elif shape == "CIRCLE":
                center = find_dot_x_y()
                return {
                    "shape": shape,
                    "center": center,
                    "radius": float(row[-1]),
                }

        def parse_separation_index():
            row = self.current_row.split()
            if len(row) < 8: return {
                "deviant_points_num": np.nan,
                "seperation_index": np.nan,
            }
            return {
                "deviant_points_num": int(row[3]),
                "seperation_index": float(row[7]),
            }

        facet = int(self.current_row.split("AND FACET")[-1].strip()[0])
        model = int(self.current_row.split("MODEL TYPE")[-1].strip())
        self.next_rows(60)
        d_geoms = []
        while " DIVIDING " in self.current_row:
            d_geom = parse_divide_geom()
            d_geoms.append(d_geom)
            self.next_row()
        separation_index = parse_separation_index()
        model_data = {
            "facet": facet,
            "model": model,
            "divide_geoms": d_geoms,
        }
        model_data.update(separation_index)
        return model_data

    @staticmethod
    def split_by_buffer(text):
        first_buffer_index = text.find(BUFFER)
        last_buffer_index = None
        for i in range(first_buffer_index, len(text)):
            if text[i] != BUFFER:
                last_buffer_index = i - 1
                break
        return text[:first_buffer_index], text[last_buffer_index + 1:]

    def parse_data_line_format(self, text):
        var, value = self.split_by_buffer(text)
        var = var.strip().replace(" ", "_").lower()
        value = value.strip().lower()
        try:
            value = float(value)
        except ValueError:
            pass
        if value is None: return
        return {var: value}

    def end_block_reached(self):
        return END_BLOCK in self.current_row

    def extract_metadata(self):
        data = {}
        while not self.end_block_reached():
            row_data = self.parse_data_line_format(self.current_row)
            if not row_data:
                self.next_row()
                continue
            data.update(row_data)
            self.next_row()
        return data

    def _extract_psc_solution_text(self) -> str:
        """Extract the POSAC solution table rows (numbers only, no headers)."""
        try:
            header_index = next(i for i, r in enumerate(self.rows) if COORDS_ROW in r)
        except StopIteration:
            return ""
        # Data starts two lines after the header row
        i = header_index + 2
        lines: List[str] = []
        while i < len(self.rows) and self.rows[i] != "\n":
            # replace '*' with space to keep only numbers and spaces
            sanitized = self.rows[i].replace("*", " ").rstrip("\n")
            lines.append(sanitized)
            i += 1
        return "\n".join(lines)

    def _extract_mumatrix_text(self) -> str:
        """Extract the item-by-item weak monotonicity coefficient matrix as numeric-only lines."""
        # Find the section header
        try:
            start = next(i for i, r in enumerate(self.rows) if "COEFFICIENTS OF WEAK MONOTONICITY" in r and "ITEMS" in self.rows[i+1])
        except StopIteration:
            return ""
        i = start
        lines: List[str] = []
        border_chars = ["║", "º", "|", "│", "¦"]
        # Scan forward to collect numeric lines after a border
        while i < len(self.rows):
            row = self.rows[i]
            payload = None
            for bc in border_chars:
                if bc in row:
                    payload = row.split(bc, 1)[-1].rstrip("\n")
                    break
            if payload is not None:
                # capture only lines that contain numeric content
                if re.search(r"\d", payload):
                    candidate = payload.strip()
                    if candidate and all(ch.isdigit() or ch.isspace() or ch in ".+-" for ch in candidate):
                        lines.append(payload.rstrip())
            # Heuristic stop: once we've collected at least one line and hit a blank
            if lines and row == "\n":
                break
            i += 1
        return "\n".join(lines)

    def _extract_item_factor_text(self) -> str:
        """Extract the per-item coefficients J,L,X,Y,P,Q as numeric-only lines (omit item index)."""
        # Find the section header
        try:
            start = next(i for i, r in enumerate(self.rows) if "COEFFICIENT OF WEAK MONOTONICITY BETWEEN EACH OBSERVED ITEM AND THE FACTORS" in r)
        except StopIteration:
            return ""
        # Skip down past column headers (there are a few fixed lines)
        i = start + 1
        # advance until we reach the line that starts the table header 'ITEM'
        while i < len(self.rows) and "ITEM" not in self.rows[i]:
            i += 1
        # skip the two header lines ('ITEM...' and '----...')
        i += 2
        lines: List[str] = []
        pattern = re.compile(r"^\s*\d+\s+(.*\S)\s*$")
        while i < len(self.rows):
            row = self.rows[i]
            if row.strip() == "":
                break
            m = pattern.match(row)
            if m:
                payload = m.group(1)
                # keep only lines that look numeric-only with signs, dots and spaces
                candidate = payload.strip()
                if candidate and all(ch.isdigit() or ch.isspace() or ch in ".+-" for ch in candidate):
                    lines.append(payload.rstrip())
            i += 1
        return "\n".join(lines)

    def get_output(self):
        return {
            "out_coords": self.out_graph_coords,
            "psc_solution": self.psc_solution_text,
            "psc_mumatrix": self.psc_mumatrix_text,
            "psc_item_fact": self.psc_item_fact_text,
        }

    @staticmethod
    def replace_input_data(output_path : str,
                           new_input_data_path : str) -> None:
        output_lines : List[str] = []
        INPUT_STRING = "INPUT FILE .................."
        with open(output_path, 'r', encoding='latin-1') as file:
            for line in file:
                if INPUT_STRING in line:
                    # replace everything after INPUT_STRING
                    line = line.split(INPUT_STRING)[0] + INPUT_STRING + new_input_data_path + "\n"
                output_lines.append(line)
        with open(output_path, 'w', encoding='latin-1') as file:
            file.writelines(output_lines)


    @staticmethod
    def reset_instance():
        OutputParser._instance = None

    @staticmethod
    def parse_output(file_path : str, reset : bool = False):
        if reset or OutputParser._instance is None:
            OutputParser._instance = OutputParser(file_path)
        return OutputParser._instance.get_output()

if __name__ == '__main__':
    output_path = r"C:\Users\raz3z\Projects\Shmuel\posac\tests\jneeds\output\job1.pos"
    parsed = OutputParser.parse_output(output_path)
    print(json.dumps(parsed, sort_keys=True, indent=4))
    print(parsed['psc_item_fact'])
    print("done")
    # OutputParser.replace_input_data(output_path, r"C:\Users\raz3z\Projects\Shmuel\posac\tests\jneeds\input\job1.prn")

