import os
from unittest.mock import MagicMock, patch

import numpy as np
import pytest

from lib.posac.posac_axes import PosacAxes


class TestPosacAxesRecoding:
    def test_set_b_uses_ten_intervals_for_x_y(self):
        axes = PosacAxes()
        set_a = axes._create_profiles_bins_dict([100.0], [100.0], ["11"], set_b=False)
        set_b = axes._create_profiles_bins_dict([100.0], [100.0], ["11"], set_b=True)

        assert max(set_a["11"]) <= 4
        assert max(set_b["11"]) == 10

    def test_set_b_differs_from_set_a_for_same_coordinates(self):
        axes = PosacAxes()
        x_coords = [86.36, 13.64, 50.0]
        y_coords = [13.64, 86.36, 50.0]
        profiles = ["22", "11", "12"]

        set_a = axes._create_profiles_bins_dict(x_coords, y_coords, profiles, set_b=False)
        set_b = axes._create_profiles_bins_dict(x_coords, y_coords, profiles, set_b=True)

        assert set_a != set_b
