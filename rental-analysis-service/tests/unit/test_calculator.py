"""Unit tests for CAGR calculator service."""

import pytest

from src.services.calculator import Calculator


class TestCalculateCAGR:
    """Test CAGR calculation."""

    def test_calculate_cagr_positive_growth(self):
        """Test CAGR calculation with positive growth."""
        start_value = 1000.0
        end_value = 1500.0
        years = 5
        cagr = Calculator.calculate_cagr(start_value, end_value, years)
        # Expected: ((1500/1000)^(1/5)) - 1 = 0.0845 or 8.45%
        assert abs(cagr - 0.0845) < 0.0001

    def test_calculate_cagr_zero_growth(self):
        """Test CAGR calculation with zero growth."""
        start_value = 1000.0
        end_value = 1000.0
        years = 5
        cagr = Calculator.calculate_cagr(start_value, end_value, years)
        assert cagr == 0.0

    def test_calculate_cagr_negative_growth(self):
        """Test CAGR calculation with negative growth."""
        start_value = 1000.0
        end_value = 800.0
        years = 3
        cagr = Calculator.calculate_cagr(start_value, end_value, years)
        # Expected: ((800/1000)^(1/3)) - 1 = -0.0717 or -7.17%
        assert abs(cagr - (-0.0717)) < 0.001

    def test_calculate_cagr_one_year(self):
        """Test CAGR calculation for one year period."""
        start_value = 1000.0
        end_value = 1100.0
        years = 1
        cagr = Calculator.calculate_cagr(start_value, end_value, years)
        # Expected: ((1100/1000)^(1/1)) - 1 = 0.1 or 10%
        assert abs(cagr - 0.1) < 0.0001

    def test_calculate_cagr_ten_years(self):
        """Test CAGR calculation for ten year period."""
        start_value = 1000.0
        end_value = 2000.0
        years = 10
        cagr = Calculator.calculate_cagr(start_value, end_value, years)
        # Expected: ((2000/1000)^(1/10)) - 1 = 0.0718 or 7.18%
        assert abs(cagr - 0.0718) < 0.0001

    def test_calculate_cagr_zero_start_value(self):
        """Test CAGR calculation with zero start value raises error."""
        with pytest.raises(ValueError, match="Start value must be greater than zero"):
            Calculator.calculate_cagr(0.0, 1000.0, 5)

    def test_calculate_cagr_negative_start_value(self):
        """Test CAGR calculation with negative start value raises error."""
        with pytest.raises(ValueError, match="Start value must be greater than zero"):
            Calculator.calculate_cagr(-1000.0, 1500.0, 5)

    def test_calculate_cagr_negative_end_value(self):
        """Test CAGR calculation with negative end value raises error."""
        with pytest.raises(ValueError, match="End value cannot be negative"):
            Calculator.calculate_cagr(1000.0, -500.0, 5)

    def test_calculate_cagr_zero_years(self):
        """Test CAGR calculation with zero years raises error."""
        with pytest.raises(ValueError, match="Years must be greater than zero"):
            Calculator.calculate_cagr(1000.0, 1500.0, 0)

    def test_calculate_cagr_negative_years(self):
        """Test CAGR calculation with negative years raises error."""
        with pytest.raises(ValueError, match="Years must be greater than zero"):
            Calculator.calculate_cagr(1000.0, 1500.0, -5)


class TestCalculateCumulativeInflation:
    """Test cumulative inflation calculation."""

    def test_calculate_cumulative_inflation_positive_rates(self):
        """Test cumulative inflation with positive monthly rates."""
        monthly_rates = [0.002, 0.003, 0.0025, 0.0015]  # 4 months
        cumulative = Calculator.calculate_cumulative_inflation(monthly_rates)
        # Expected: (1.002 * 1.003 * 1.0025 * 1.0015) - 1 = 0.00902
        assert abs(cumulative - 0.00902) < 0.00001

    def test_calculate_cumulative_inflation_zero_rates(self):
        """Test cumulative inflation with zero rates."""
        monthly_rates = [0.0, 0.0, 0.0]
        cumulative = Calculator.calculate_cumulative_inflation(monthly_rates)
        assert cumulative == 0.0

    def test_calculate_cumulative_inflation_mixed_rates(self):
        """Test cumulative inflation with mixed positive and negative rates."""
        monthly_rates = [0.002, -0.001, 0.003]
        cumulative = Calculator.calculate_cumulative_inflation(monthly_rates)
        # Expected: (1.002 * 0.999 * 1.003) - 1 = 0.00401
        assert abs(cumulative - 0.00401) < 0.00001

    def test_calculate_cumulative_inflation_one_month(self):
        """Test cumulative inflation with single month."""
        monthly_rates = [0.002]
        cumulative = Calculator.calculate_cumulative_inflation(monthly_rates)
        assert abs(cumulative - 0.002) < 0.00001

    def test_calculate_cumulative_inflation_twelve_months(self):
        """Test cumulative inflation with twelve months (one year)."""
        monthly_rates = [0.002] * 12  # 0.2% per month
        cumulative = Calculator.calculate_cumulative_inflation(monthly_rates)
        # Expected: (1.002^12) - 1 = 0.02427
        assert abs(cumulative - 0.02427) < 0.00001

    def test_calculate_cumulative_inflation_empty_list(self):
        """Test cumulative inflation with empty list raises error."""
        with pytest.raises(ValueError, match="Monthly rates list cannot be empty"):
            Calculator.calculate_cumulative_inflation([])

    def test_calculate_cumulative_inflation_realistic_scenario(self):
        """Test cumulative inflation with realistic 10-year scenario."""
        # 120 months of 0.2% monthly inflation
        monthly_rates = [0.002] * 120
        cumulative = Calculator.calculate_cumulative_inflation(monthly_rates)
        # Expected: (1.002^120) - 1 = 0.2709 or 27.09%
        assert abs(cumulative - 0.2709) < 0.001


class TestCalculateRealCAGR:
    """Test real (inflation-adjusted) CAGR calculation."""

    def test_calculate_real_cagr_positive_growth_positive_inflation(self):
        """Test real CAGR with positive growth and positive inflation."""
        nominal_cagr = 0.08  # 8% nominal growth
        cumulative_inflation = 0.20  # 20% cumulative inflation
        real_cagr = Calculator.calculate_real_cagr(nominal_cagr, cumulative_inflation)
        # Expected: ((1.08) / (1.20)) - 1 = -0.1 or -10%
        assert abs(real_cagr - (-0.1)) < 0.0001

    def test_calculate_real_cagr_growth_exceeds_inflation(self):
        """Test real CAGR when growth exceeds inflation."""
        nominal_cagr = 0.30  # 30% nominal growth
        cumulative_inflation = 0.20  # 20% cumulative inflation
        real_cagr = Calculator.calculate_real_cagr(nominal_cagr, cumulative_inflation)
        # Expected: ((1.30) / (1.20)) - 1 = 0.0833 or 8.33%
        assert abs(real_cagr - 0.0833) < 0.0001

    def test_calculate_real_cagr_zero_inflation(self):
        """Test real CAGR with zero inflation."""
        nominal_cagr = 0.08
        cumulative_inflation = 0.0
        real_cagr = Calculator.calculate_real_cagr(nominal_cagr, cumulative_inflation)
        # Real CAGR should equal nominal CAGR
        assert abs(real_cagr - 0.08) < 0.0001

    def test_calculate_real_cagr_zero_growth(self):
        """Test real CAGR with zero nominal growth."""
        nominal_cagr = 0.0
        cumulative_inflation = 0.20
        real_cagr = Calculator.calculate_real_cagr(nominal_cagr, cumulative_inflation)
        # Expected: ((1.0) / (1.20)) - 1 = -0.1667 or -16.67%
        assert abs(real_cagr - (-0.1667)) < 0.0001

    def test_calculate_real_cagr_negative_growth(self):
        """Test real CAGR with negative nominal growth."""
        nominal_cagr = -0.05  # -5% nominal growth
        cumulative_inflation = 0.10  # 10% cumulative inflation
        real_cagr = Calculator.calculate_real_cagr(nominal_cagr, cumulative_inflation)
        # Expected: ((0.95) / (1.10)) - 1 = -0.1364 or -13.64%
        assert abs(real_cagr - (-0.1364)) < 0.0001

    def test_calculate_real_cagr_negative_inflation(self):
        """Test real CAGR with deflation (negative inflation)."""
        nominal_cagr = 0.05
        cumulative_inflation = -0.05  # Deflation
        real_cagr = Calculator.calculate_real_cagr(nominal_cagr, cumulative_inflation)
        # Expected: ((1.05) / (0.95)) - 1 = 0.1053 or 10.53%
        assert abs(real_cagr - 0.1053) < 0.0001

    def test_calculate_real_cagr_invalid_inflation(self):
        """Test real CAGR with invalid inflation (< -1) raises error."""
        with pytest.raises(
            ValueError, match="Cumulative inflation cannot be less than -1"
        ):
            Calculator.calculate_real_cagr(0.05, -1.5)


class TestFormatPercentage:
    """Test percentage formatting."""

    def test_format_percentage_positive(self):
        """Test formatting positive percentage."""
        result = Calculator.format_percentage(0.0845)
        assert result == "8.45%"

    def test_format_percentage_negative(self):
        """Test formatting negative percentage."""
        result = Calculator.format_percentage(-0.0718)
        assert result == "-7.18%"

    def test_format_percentage_zero(self):
        """Test formatting zero percentage."""
        result = Calculator.format_percentage(0.0)
        assert result == "0.00%"

    def test_format_percentage_large_value(self):
        """Test formatting large percentage."""
        result = Calculator.format_percentage(1.5)
        assert result == "150.00%"

    def test_format_percentage_small_value(self):
        """Test formatting small percentage."""
        result = Calculator.format_percentage(0.0001)
        assert result == "0.01%"

    def test_format_percentage_custom_decimals(self):
        """Test formatting with custom decimal places."""
        result = Calculator.format_percentage(0.08456, decimals=3)
        assert result == "8.456%"

    def test_format_percentage_rounding(self):
        """Test percentage rounding."""
        result = Calculator.format_percentage(0.08456, decimals=1)
        assert result == "8.5%"
