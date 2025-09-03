import os
from typing import Dict, List, Tuple

from lib.common import parse_range_string
from lib.utils import *

SHEMOR_DIRECTIVES = {
    "A": """FOR X,Y RECODE 0 THRU  25 = 1,  26 THRU  50 = 2,
              51 THRU  75 = 3,  76 THRU 100 = 4.
FOR J,L RECODE 0 THRU  50 = 1,  51 THRU 100 = 2,
             101 THRU 150 = 3, 151 THRU 200 = 4.""",
    "B": """FOR X,Y RECODE  0 THRU 45 = 1, 46 THRU 75 = 2, 76 THRU 100 = 3.
            FOR J RECODE 0 THRU 60 = 1, 61 THRU 110 = 2, 111 THRU 150 = 3,
            151 THRU 200 = 4.
            FOR L  RECODE 0 THRU 100 =1 , 101 THRU 200 = 2.""",
}


class PosacInputWriter:
    def __init__(self):
        pass

    def create_posac_input_file(
        self,
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
        min_category: int = 4,
        max_category: int = 4,
        nd1: int = None,
        nd2: int = None,
        variable_labels=None,
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
        if not os.path.exists(RUN_FILES_DIR):
            os.makedirs(RUN_FILES_DIR)

        self.ex_var_first_i = num_variables - nxt + 1

        with open(f"{RUN_FILES_DIR}/{DRV_IN_NAME}", "w") as f:
            self.write_title_card(f, job_name)
            self.write_parameter_card(
                f,
                num_variables,
                idata,
                lowfreq,
                missing,
                ipower,
                itemdplt,
                nlab,
                nxt,
                map_,
                iextdiag,
                itable,
                initx,
                iboxstrng,
                iff,
                itrm,
                iwrtfls,
                ifshmr,
                ifrqone,
            )
            self.write_input_format(
                f, variables_details, case_id_location, subject_type, missing
            )
            if missing != 0 or True:
                self.write_min_max_category(f, min_category, max_category)
            if ipower != 0:
                self.write_nd_values(f, nd1, nd2)
            if nlab != 0:
                self.write_variable_labels(f, variables_details)
            if nxt != 0:
                self.write_ext_var_ranges(f, ext_var_ranges)
            if map_ != 0:
                self.write_traits(f, traits)
            if initx != 0:
                self.write_initial_approx(f, init_approx_format, init_approx)
            if iboxstrng != 0:
                self.write_boxstring(f, boxstring)
            if iff != 0:
                self.write_form_feed(f, form_feed)
            if ifshmr != 0:
                self.write_shemor_directives(f, record_length, shemor_directives_key)

    def write_title_card(self, f, job_name: str):
        f.write(f"{job_name}\n")

    def write_parameter_card(
        self,
        f,
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
    ):
        params = [
            num_variables,
            idata,
            lowfreq,
            missing,
            ipower,
            itemdplt,
            nlab,
            nxt,
            map_,
            iextdiag,
            itable,
            initx,
            iboxstrng,
            iff,
            itrm,
            iwrtfls,
            ifshmr,
            ifrqone,
        ]
        f.write("".join([f"{param:4}" for param in params]) + "\n")

    def write_input_format(
        self,
        f,
        variables_details: List[Dict],
        case_id_location: Tuple[int, int],
        subject_type: str,
        missing: int,
    ):
        """Write the input format string where all variables are on the same line.
        Each variable takes 2 characters and position is based on its index.

        Example:
            For variables with indices 1,2,3 the format will be:
            "(T1,I1,T3,I1,T5,I1)"
        """
        input_format = "("
        if subject_type in ["P", "I"]:
            last_var_index = variables_details[-1]["index"]
            input_format += f"T{int(last_var_index) * 2 + 1},A{case_id_location[1] - case_id_location[0] + 1},"
        input_format += ",".join(
            [f"T{(int(var['index']) - 1) * 2 + 1},I2" for var in variables_details]
        )
        input_format += ")"
        f.write(f"{input_format}\n")
        # write the valid values
        if missing == 1:
            valid_lows = []
            valid_highs = []
            for var in variables_details:
                valid_lows.append(var["valid_low"])
                valid_highs.append(var["valid_high"])
            valid_values_string = (
                "".join([f"{val:>4}" for val in valid_lows])
                + "\n"
                + "".join([f"{val:>4}" for val in valid_highs])
                + "\n"
            )
            f.write(valid_values_string)

    def write_legacy_input_format(self, f, variables_details: List[Dict]):
        """Legacy method for backward compatibility.
        Uses explicit column and width from variables_details.
        """
        input_format = (
            "("
            + ",".join([f"T{var['col']},I{var['width']}" for var in variables_details])
            + ")"
        )
        f.write(f"{input_format}\n")

    def write_min_max_category(self, f, min_category: int, max_category: int):
        if min_category or max_category:
            f.write(f"{min_category:4}{max_category:4}\n")

    def write_nd_values(self, f, nd1: int, nd2: int):
        f.write(f"{nd1:4}{nd2:4}\n")

    def write_variable_labels(self, f, var_details: List[Dict]):
        var_label_str = ""
        for var in var_details:
            var_label_str += f"{int(var['index']):4}      {var['label']}\n"
        f.write(var_label_str)

    def write_ext_var_ranges(self, f, ext_var_ranges: List[List[str]]):
        for i, var_ranges in enumerate(ext_var_ranges):
            f.write(f"{i+self.ex_var_first_i:4}{len(var_ranges):4}")
            for v_range in var_ranges:
                l, h = parse_range_string(v_range)
                f.write(f"{l:4}{h:4}\n")

    def write_traits(self, f, traits: List[Dict]):
        traits_str = ""
        for trait in traits:
            traits_str += f"{trait['label']}\n"
            for i, ext_var in enumerate(trait['data']):
                traits_str += f"{i+self.ex_var_first_i:4}"
                traits_str += f"{len(trait['data']):4}"
                l, h = parse_range_string(ext_var)
                traits_str += f"{l:4}{h:4}"
                traits_str += "\n"
        f.write(traits_str)

    def write_initial_approx(self, f, init_approx_format: str,
                             init_approx: List[List[float]]):
        f.write(f"{init_approx_format}\n")
        for approx in init_approx:
            f.write("   ".join([f"{a:3.1f}" for a in approx]) + "\n")

    def write_boxstring(self, f, boxstring: str):
        f.write(f"{boxstring}\n")

    def write_form_feed(self, f, form_feed: str):
        f.write(f"{form_feed}\n")

    def write_shemor_directives(self, f, record_length : int, shemor_directives_key: List[str]):
        f.write("SHEMOR\n")
        f.write(f"RECORD LENGTH  {record_length}\n")
        f.write(f"{SHEMOR_DIRECTIVES[shemor_directives_key]}\n")


# Example usage
if __name__ == "__main__":
    writer = PosacInputWriter()
    writer.create_posac_input_file(
        job_name="POSAC ON 6 VARIABLES (ITEMS)",
        num_variables=6,
        idata=0,
        lowfreq=0,
        missing=0,
        ipower=0,
        itemdplt=0,
        nlab=6,
        nxt=2,
        map_=4,
        iextdiag=0,
        itable=0,
        initx=0,
        iboxstrng=0,
        iff=0,
        itrm=0,
        iwrtfls=0,
        ifshmr=0,
        ifrqone=0,
        input_format="(91X,4I1,2X,2I1,/)",
        min_category=4,
        max_category=4,
        nd1=None,
        nd2=None,
        variable_labels=[
            {'index': 1, 'label': 'Variable 1'},
            {'index': 2, 'label': 'Variable 2'},
            {'index': 3, 'label': 'Variable 3'},
            {'index': 4, 'label': 'Variable 4'},
            {'index': 5, 'label': 'Variable 5'},
            {'index': 6, 'label': 'Variable 6'}
        ],
        external_variables=[
            [8, 1, 0, 9],
            [9, 1, 0, 9]
        ],
        traits=[
            {'label': 'MALES UNDER 40 Y. OF AGE',
             'external_vars': [[8, 1, 1, 1], [9, 1, 1, 4]]},
            {'label': 'MALES OVER 40 Y. OF AGE',
             'external_vars': [[8, 1, 1, 1], [9, 1, 5, 9]]},
            {'label': 'FEM. UNDER 40 Y. OF AGE',
             'external_vars': [[8, 1, 2, 2], [9, 1, 1, 4]]},
            {'label': 'FEM. OVER 40 Y. OF AGE',
             'external_vars': [[8, 1, 2, 2], [9, 1, 5, 9]]}
        ],
        init_approx_format=None,
        init_approx=None,
        boxstring=None,
        form_feed=None,
        shemor_directives_key=None
    )
