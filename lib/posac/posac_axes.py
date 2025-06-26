"""
SET_A: For X,Y recode 0 thru 25=1, 26 thru 50=2,51 thru 75=3,76 thru 100=4;
For J,L recode 0 thru 50=1, 51 thru 100=2,101 thru 150=3,151 thru 200=4.

SET_B: For X,Y recode 0 thru 10=1, 11 thru 20=2,21 thru 30=3, 31 thru 40=4,
41 thru 50=5,51 thru 60=6,61 thru 70=7, 71 thru 80=8,81 thru 90=9, 91 thru 100=10.
For J,L recode 0 thru 20=1, 21 thru 40=2,41 thru 60=3,61 thru 80=4, 81 thru 100=5,
101 thru 120=6,121 thru 140=7, 141 thru 160=8,161 thru 180=9, 181 thru 200=10


86.36     13.64              100.00    172.73
4   1   2   4

"""


from typing import List, Tuple
import numpy as np
from lib.posac.posac_output_parser import OutputParser
from loguru import logger

class PosacAxesError(Exception):
    pass

def bin(x : int, mode : int) -> int:
    """
    returns the bin of the x value.
    """
    return int((abs(x-1) // mode) + 1)

class PosacAxes:
    def __init__(self):
        pass

    def _recode_x_y(self, x : List[float],
                     y : List[float],
                     set_b : bool = False) -> Tuple[int, int]:
        """
        recodes the x and y values according to the set_b flag.
        """
        if set_b:
            return bin(x, 10), bin(y, 10)
        return bin(x, 25), bin(y, 25)

    def _recode_j_l(self, j : List[float],
                     l : List[float],
                       set_b : bool = False) -> Tuple[int, int]:
        """
        recodes the j and l values according to the set_b flag.
        """
        if set_b:
            return bin(j, 20), bin(l, 20)
        return bin(j, 50), bin(l, 50)

    def _create_profiles_bins_dict(self, x_coords : List[float],
                                           y_coords : List[float],
                                           profiles : List[str],
                                           set_b : bool = False) -> dict:
        """
        Args:
            x = [100.0, 33.33, 66.67, 0.0]
            y = [100.0, 66.67, 33.33, 0.0]
            profiles = [' 2 2', ' 2 1', ' 1 2', ' 1 1']
        Returns:
            profiles_bins is a dictionary, where the key is the profile number
            and the value is a list of [bin(x), bin(y), bin(l), bin(j)]
            if set_b is True, the bins are recoded according to the set_b flag.
            where:
            l = 100 - (y - x)
            j = x + y
            e.g:
            profiles_coordinates = {
                ' 2 2': [2, 2, 0, 2],
                ' 2 1': [1, 2, 3, 1],
                ' 1 2': [2, 1, 3, 1],
                ' 1 1': [1, 1, 1, 1],
        """
        profiles_bins = {}
        for i, profile in enumerate(profiles):
            x, y = self._recode_x_y(x_coords[i], y_coords[i], set_b)
            j, l = self._recode_j_l(x_coords[i] + y_coords[i], 100 - (y_coords[i] - x_coords[i]), set_b)
            profiles_bins[profile.replace(" ", "")] = [x, y, j, l]
        return profiles_bins

    def _create_posac_axes_list(self, profiles_coordinates : dict,
                                 input_data : np.ndarray,
                                 internal_variables_num : int,
                                 failed_rows : List[int]) -> List[str]:
        """
        creates a list of rows containing for each row in the input data,
        the corresponding profile coordinates.
        Args:
            profiles_coordinates : dict
            input_data : np.ndarray
            internal_variables_num : int
            failed_rows : list[int] in [1-based index]
        Returns:
            posac_axes_list : list

            e.g:
                2  2  2  3
                4  1  3  4
                4  1  2  4
                2  3  2  2
        """
        posac_axes_list = []
        for i, row in enumerate(input_data):
            str_row = "".join(map(str, input_data[i][:internal_variables_num]))
            try:
                posac_axes_list.append(profiles_coordinates[str_row])
            except KeyError:
                logger.info(f"Profile {str_row} not found in output profiles coordinates")
                posac_axes_list.append([0, 0, 0, 0])
        # now to add [0, 0, 0, 0] for the failed rows
        if failed_rows:
            for i in sorted(failed_rows):
                posac_axes_list.insert(i-1, [0, 0, 0, 0])
            logger.info(f"Added [0, 0, 0, 0] for {len(failed_rows)} failed rows")
        return posac_axes_list

    def _create_posac_axes_file(self, input_data_file : str,
                                 posac_axes_list : List[str],
                                 output_path : str) -> None:
        """
        creates a file with the posac axes list.
            e.g:
                5431245321335554113411
                2  2  2  3
                5321455422245554311511
                4  1  3  4
                5321445423455543123511
                4  1  2  4
                4433334222245543333331
                2  3  2  2
        """
        with open(input_data_file, 'r') as file:
            input_data_lines = file.readlines()
        if len(input_data_lines) != len(posac_axes_list):
            raise PosacAxesError(f"Input data file and posac axes list have different lengths: {len(input_data_lines)} != {len(posac_axes_list)}")
        with open(output_path, 'w') as file:
            for i, row in enumerate(posac_axes_list):
                if i != 0:
                    file.write("\n")
                file.write(input_data_lines[i])
                file.write(f"{row[0]:3}{row[1]:3}{row[2]:3}{row[3]:3}")

    ##################
    # PUBLIC METHODS #
    ##################

    def run(self,
            active_data_matrix : np.ndarray,
            internal_variables_num : int,
            failed_rows : List[int],
            input_data_file : str,
            posac_output_path : str,
            set_b : bool = False,
            output_path : str = None):
        try:
            output : dict = OutputParser.parse_output(posac_output_path)
        except Exception as e:
            raise PosacAxesError(f"Error parsing posac output: {e}")

        profiles_coordinates : dict = self._create_profiles_bins_dict(
            output['out_coords']['x'],
            output['out_coords']['y'],
            output['out_coords']['profiles'],
            set_b
        )
        posac_axes_lines : list = self._create_posac_axes_list(
            profiles_coordinates=profiles_coordinates,
            input_data=active_data_matrix,
            internal_variables_num=internal_variables_num,
            failed_rows=failed_rows
        )
        self._create_posac_axes_file(input_data_file, posac_axes_lines, output_path)


if __name__ == "__main__":
    input_data_path = r"C:\Users\raz3z\Projects\Shmuel\posac\tests\posac_axes\dj_all.prn"
    input_data = np.loadtxt(input_data_path, dtype=str)
    posac_output_path = r"C:\Users\raz3z\Projects\Shmuel\posac\tests\dj\output\dj_all-testpos.pos"
    set_b = False
    output_path = r"C:\Users\raz3z\Projects\Shmuel\posac\tests\posac_axes\dj_all_axes.prn"
    posac_axes = PosacAxes()
    posac_axes.run(input_data, posac_output_path, set_b, output_path)