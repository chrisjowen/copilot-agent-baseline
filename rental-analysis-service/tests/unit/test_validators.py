"""Unit tests for input validators."""

import pytest

from src.utils.validators import ValidationError, validate_country_code, validate_years


class TestValidateCountryCode:
    """Test country code validation."""

    def test_validate_country_code_valid_uppercase(self):
        """Test validation with valid uppercase country code."""
        result = validate_country_code("US")
        assert result == "US"

    def test_validate_country_code_valid_lowercase(self):
        """Test validation with valid lowercase country code."""
        result = validate_country_code("gb")
        assert result == "GB"

    def test_validate_country_code_valid_mixed_case(self):
        """Test validation with mixed case country code."""
        result = validate_country_code("De")
        assert result == "DE"

    def test_validate_country_code_empty_string(self):
        """Test validation with empty string."""
        with pytest.raises(ValidationError, match="cannot be empty"):
            validate_country_code("")

    def test_validate_country_code_too_short(self):
        """Test validation with too short country code."""
        with pytest.raises(ValidationError, match="exactly 2 characters"):
            validate_country_code("U")

    def test_validate_country_code_too_long(self):
        """Test validation with too long country code."""
        with pytest.raises(ValidationError, match="exactly 2 characters"):
            validate_country_code("USA")

    def test_validate_country_code_with_numbers(self):
        """Test validation with numbers in country code."""
        with pytest.raises(ValidationError, match="only letters"):
            validate_country_code("U1")

    def test_validate_country_code_with_special_chars(self):
        """Test validation with special characters."""
        with pytest.raises(ValidationError, match="only letters"):
            validate_country_code("U$")

    def test_validate_country_code_with_spaces(self):
        """Test validation with spaces."""
        with pytest.raises(ValidationError, match="only letters"):
            validate_country_code("U ")

    def test_validate_country_code_non_string(self):
        """Test validation with non-string input."""
        with pytest.raises(ValidationError, match="must be a string"):
            validate_country_code(123)


class TestValidateYears:
    """Test years validation."""

    def test_validate_years_one(self):
        """Test validation with 1 year."""
        result = validate_years(1)
        assert result == 1

    def test_validate_years_three(self):
        """Test validation with 3 years."""
        result = validate_years(3)
        assert result == 3

    def test_validate_years_five(self):
        """Test validation with 5 years."""
        result = validate_years(5)
        assert result == 5

    def test_validate_years_ten(self):
        """Test validation with 10 years."""
        result = validate_years(10)
        assert result == 10

    def test_validate_years_invalid_value(self):
        """Test validation with invalid years value."""
        with pytest.raises(ValidationError, match="must be one of"):
            validate_years(7)

    def test_validate_years_zero(self):
        """Test validation with zero years."""
        with pytest.raises(ValidationError, match="must be one of"):
            validate_years(0)

    def test_validate_years_negative(self):
        """Test validation with negative years."""
        with pytest.raises(ValidationError, match="must be one of"):
            validate_years(-5)

    def test_validate_years_non_integer(self):
        """Test validation with non-integer input."""
        with pytest.raises(ValidationError, match="must be an integer"):
            validate_years("5")

    def test_validate_years_float(self):
        """Test validation with float input."""
        with pytest.raises(ValidationError, match="must be an integer"):
            validate_years(5.0)
