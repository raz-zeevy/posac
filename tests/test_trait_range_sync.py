"""
Test trait range synchronization with external variable ranges.
"""
import pytest
from lib.gui.tabs.traits_tab import parse_range, clip_range_to_valid


class TestRangeHelpers:
    """Test the helper functions for range parsing and clipping."""

    def test_parse_range_valid(self):
        """Test parsing valid range strings."""
        assert parse_range("1-9") == (1, 9)
        assert parse_range("3-5") == (3, 5)
        assert parse_range("10-20") == (10, 20)

    def test_parse_range_invalid(self):
        """Test parsing invalid range strings."""
        assert parse_range("") is None
        assert parse_range("abc") is None
        assert parse_range("1-") is None
        assert parse_range("-5") is None
        assert parse_range("1") is None

    def test_clip_range_full_overlap(self):
        """Test clipping when trait range is fully within external range."""
        # Trait 1-5 fully within external 1-9
        result = clip_range_to_valid("1-5", ["1-9"])
        assert result == ["1-5"]

    def test_clip_range_partial_overlap(self):
        """Test clipping when trait range partially overlaps external range."""
        # Trait 3-7 with external 1-2, 4-6 should clip to 4-6
        result = clip_range_to_valid("3-7", ["1-2", "4-6"])
        assert result == ["4-6"]

        # Trait 0-10 with external 1-2, 4-6 should clip to both ranges
        result = clip_range_to_valid("0-10", ["1-2", "4-6"])
        assert result == ["1-2", "4-6"]

    def test_clip_range_no_overlap(self):
        """Test clipping when trait range has no overlap."""
        # Trait 8-9 with external 1-2, 4-6 should return empty
        result = clip_range_to_valid("8-9", ["1-2", "4-6"])
        assert result == []

    def test_clip_range_exact_match(self):
        """Test clipping when trait range exactly matches external range."""
        result = clip_range_to_valid("1-9", ["1-9"])
        assert result == ["1-9"]

    def test_clip_range_multiple_overlaps(self):
        """Test clipping with multiple external ranges."""
        # Trait 1-3 overlaps with both 1-2 and 3-5
        result = clip_range_to_valid("1-3", ["1-2", "3-5"])
        assert set(result) == {"1-2", "3-3"}

    def test_clip_range_single_value(self):
        """Test clipping with single-value ranges."""
        result = clip_range_to_valid("5-5", ["1-2", "4-6"])
        assert result == ["5-5"]

        result = clip_range_to_valid("3-3", ["1-2", "4-6"])
        assert result == []


class TestTraitRangeValidation:
    """Test trait range validation against external ranges."""

    def test_validate_trait_within_external(self):
        """Test validation when trait is within external range."""
        from lib.controller.validator import Validator

        # Trait 2-5 within external 1-9
        assert Validator.validate_trait_range_against_external("2-5", ["1-9"]) is True

    def test_validate_trait_outside_external(self):
        """Test validation when trait is outside external range."""
        from lib.controller.validator import Validator

        # Trait 8-9 not within external 1-2, 4-6
        assert Validator.validate_trait_range_against_external("8-9", ["1-2", "4-6"]) is False

    def test_validate_trait_partial_overlap(self):
        """Test validation when trait partially overlaps."""
        from lib.controller.validator import Validator

        # Trait 3-5 partially overlaps with 4-6, but not fully within
        assert Validator.validate_trait_range_against_external("3-5", ["4-6"]) is False

        # But trait 4-5 is fully within 4-6
        assert Validator.validate_trait_range_against_external("4-5", ["4-6"]) is True

    def test_validate_empty_trait_range(self):
        """Test validation with empty trait range."""
        from lib.controller.validator import Validator

        assert Validator.validate_trait_range_against_external("", ["1-9"]) is True
        assert Validator.validate_trait_range_against_external(None, ["1-9"]) is True

    def test_validate_invalid_format(self):
        """Test validation with invalid range format."""
        from lib.controller.validator import Validator

        assert Validator.validate_trait_range_against_external("abc", ["1-9"]) is False
        assert Validator.validate_trait_range_against_external("1", ["1-9"]) is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

