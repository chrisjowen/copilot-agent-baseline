"""Unit tests for analysis engine."""

from datetime import date
from pathlib import Path

import pytest

from src.services.analyzer import Analyzer
from src.services.calculator import Calculator
from src.services.data_loader import DataLoader


@pytest.fixture
def data_loader():
    """Create a DataLoader instance with test data directory."""
    data_dir = Path(__file__).parent.parent.parent / "data"
    return DataLoader(data_dir)


@pytest.fixture
def analyzer(data_loader):
    """Create an Analyzer instance."""
    calculator = Calculator()
    return Analyzer(data_loader, calculator)


class TestAnalyzerInitialization:
    """Test Analyzer initialization."""

    def test_init_with_valid_dependencies(self, data_loader):
        """Test initialization with valid dependencies."""
        calculator = Calculator()
        analyzer = Analyzer(data_loader, calculator)
        assert analyzer.data_loader == data_loader
        assert analyzer.calculator == calculator


class TestCalculatePeriodDates:
    """Test period date calculation."""

    def test_calculate_period_dates_one_year(self, analyzer):
        """Test calculating period dates for 1 year."""
        start_date, end_date = analyzer._calculate_period_dates("US", 1)
        assert isinstance(start_date, date)
        assert isinstance(end_date, date)
        # Should be approximately 1 year apart
        years_diff = (end_date.year - start_date.year)
        assert years_diff == 1 or years_diff == 0  # Could be same year if near end

    def test_calculate_period_dates_three_years(self, analyzer):
        """Test calculating period dates for 3 years."""
        start_date, end_date = analyzer._calculate_period_dates("GB", 3)
        years_diff = end_date.year - start_date.year
        assert years_diff >= 2 and years_diff <= 3

    def test_calculate_period_dates_five_years(self, analyzer):
        """Test calculating period dates for 5 years."""
        start_date, end_date = analyzer._calculate_period_dates("DE", 5)
        years_diff = end_date.year - start_date.year
        assert years_diff >= 4 and years_diff <= 5

    def test_calculate_period_dates_ten_years(self, analyzer):
        """Test calculating period dates for 10 years."""
        # Test data spans 10 years (2015-2024), so 10-year analysis now works
        start_date, end_date = analyzer._calculate_period_dates("FR", 10)
        years_diff = end_date.year - start_date.year
        assert years_diff >= 9 and years_diff <= 10

    def test_calculate_period_dates_end_after_start(self, analyzer):
        """Test that end date is after start date."""
        start_date, end_date = analyzer._calculate_period_dates("JP", 5)
        assert end_date > start_date


class TestAggregateRentalIncome:
    """Test rental income aggregation."""

    def test_aggregate_rental_income_returns_dict(self, analyzer):
        """Test that aggregation returns a dictionary."""
        start_date = date(2020, 1, 1)
        end_date = date(2020, 12, 31)
        result = analyzer._aggregate_rental_income("US", start_date, end_date)
        assert isinstance(result, dict)

    def test_aggregate_rental_income_has_required_keys(self, analyzer):
        """Test that aggregation result has required keys."""
        start_date = date(2020, 1, 1)
        end_date = date(2020, 12, 31)
        result = analyzer._aggregate_rental_income("US", start_date, end_date)
        assert "start_period_total" in result
        assert "end_period_total" in result
        assert "currency" in result
        assert "total_months" in result

    def test_aggregate_rental_income_positive_values(self, analyzer):
        """Test that aggregated values are positive."""
        start_date = date(2020, 1, 1)
        end_date = date(2020, 12, 31)
        result = analyzer._aggregate_rental_income("GB", start_date, end_date)
        assert result["start_period_total"] > 0
        assert result["end_period_total"] > 0

    def test_aggregate_rental_income_growth_over_time(self, analyzer):
        """Test that rental income shows growth over time."""
        start_date = date(2015, 1, 1)
        end_date = date(2024, 12, 31)
        result = analyzer._aggregate_rental_income("DE", start_date, end_date)
        # With inflation and growth, end should be higher than start
        assert result["end_period_total"] >= result["start_period_total"]

    def test_aggregate_rental_income_correct_month_count(self, analyzer):
        """Test that month count is correct."""
        start_date = date(2020, 1, 1)
        end_date = date(2020, 12, 31)
        result = analyzer._aggregate_rental_income("FR", start_date, end_date)
        assert result["total_months"] == 12

    def test_aggregate_rental_income_multi_year(self, analyzer):
        """Test aggregation over multiple years."""
        start_date = date(2020, 1, 1)
        end_date = date(2022, 12, 31)
        result = analyzer._aggregate_rental_income("JP", start_date, end_date)
        assert result["total_months"] == 36


class TestGetInflationData:
    """Test inflation data retrieval."""

    def test_get_inflation_data_returns_list(self, analyzer):
        """Test that inflation data returns a list."""
        start_date = date(2020, 1, 1)
        end_date = date(2020, 12, 31)
        rates = analyzer._get_inflation_data("US", start_date, end_date)
        assert isinstance(rates, list)

    def test_get_inflation_data_correct_length(self, analyzer):
        """Test that inflation data has correct number of months."""
        start_date = date(2020, 1, 1)
        end_date = date(2020, 12, 31)
        rates = analyzer._get_inflation_data("GB", start_date, end_date)
        assert len(rates) == 12

    def test_get_inflation_data_multi_year(self, analyzer):
        """Test inflation data over multiple years."""
        start_date = date(2020, 1, 1)
        end_date = date(2022, 12, 31)
        rates = analyzer._get_inflation_data("DE", start_date, end_date)
        assert len(rates) == 36

    def test_get_inflation_data_values_are_floats(self, analyzer):
        """Test that inflation rates are floats."""
        start_date = date(2020, 1, 1)
        end_date = date(2020, 12, 31)
        rates = analyzer._get_inflation_data("FR", start_date, end_date)
        assert all(isinstance(rate, float) for rate in rates)


class TestGetBuildingCount:
    """Test building count retrieval."""

    def test_get_building_count_returns_int(self, analyzer):
        """Test that building count returns an integer."""
        count = analyzer._get_building_count("US")
        assert isinstance(count, int)

    def test_get_building_count_positive(self, analyzer):
        """Test that building count is positive."""
        count = analyzer._get_building_count("GB")
        assert count > 0

    def test_get_building_count_expected_value(self, analyzer):
        """Test that building count matches expected test data."""
        # Test data has 10 buildings per country
        count = analyzer._get_building_count("DE")
        assert count == 10


class TestAnalyze:
    """Test complete analysis workflow."""

    def test_analyze_returns_response_model(self, analyzer):
        """Test that analyze returns AnalysisResponse model."""
        from src.models.schemas import AnalysisResponse

        result = analyzer.analyze("US", 1)
        assert isinstance(result, AnalysisResponse)

    def test_analyze_has_correct_country_code(self, analyzer):
        """Test that response has correct country code."""
        result = analyzer.analyze("GB", 3)
        assert result.country_code == "GB"

    def test_analyze_has_correct_period(self, analyzer):
        """Test that response has correct analysis period."""
        result = analyzer.analyze("DE", 5)
        assert result.analysis_period_years == 5

    def test_analyze_has_date_range(self, analyzer):
        """Test that response includes date range."""
        result = analyzer.analyze("FR", 1)
        assert result.date_range.start_date is not None
        assert result.date_range.end_date is not None
        assert result.date_range.end_date > result.date_range.start_date

    def test_analyze_has_rental_income(self, analyzer):
        """Test that response includes rental income data."""
        result = analyzer.analyze("JP", 3)
        assert result.rental_income.start_period_total > 0
        assert result.rental_income.end_period_total > 0
        assert result.rental_income.currency is not None

    def test_analyze_has_growth_metrics(self, analyzer):
        """Test that response includes growth metrics."""
        result = analyzer.analyze("US", 5)
        assert result.growth_metrics.nominal_cagr_percent is not None
        assert result.growth_metrics.cumulative_inflation_percent is not None
        assert result.growth_metrics.real_cagr_percent is not None

    def test_analyze_has_portfolio_summary(self, analyzer):
        """Test that response includes portfolio summary."""
        result = analyzer.analyze("GB", 5)
        assert result.portfolio_summary.buildings_analyzed > 0
        assert result.portfolio_summary.total_months > 0

    def test_analyze_all_periods(self, analyzer):
        """Test analysis for all valid periods."""
        # Test data spans 2015-2024 (10 years), all periods work
        for years in [1, 3, 5, 10]:
            result = analyzer.analyze("DE", years)
            assert result.analysis_period_years == years

    def test_analyze_all_countries(self, analyzer):
        """Test analysis for all test countries."""
        countries = ["US", "GB", "DE", "FR", "JP"]
        for country in countries:
            result = analyzer.analyze(country, 5)
            assert result.country_code == country

    def test_analyze_invalid_country(self, analyzer):
        """Test analysis with invalid country raises error."""
        with pytest.raises(ValueError):
            analyzer.analyze("XX", 5)

    def test_analyze_invalid_period(self, analyzer):
        """Test analysis with invalid period raises error."""
        with pytest.raises(ValueError, match="Years must be one of"):
            analyzer.analyze("US", 7)

    def test_analyze_growth_calculation_accuracy(self, analyzer):
        """Test that growth calculations are reasonable."""
        result = analyzer.analyze("US", 5)
        # Nominal CAGR should be positive (rental growth)
        assert result.growth_metrics.nominal_cagr_percent > 0
        # Cumulative inflation should be positive
        assert result.growth_metrics.cumulative_inflation_percent > 0
        # Real CAGR could be positive or negative depending on growth vs inflation
        assert result.growth_metrics.real_cagr_percent is not None

    def test_analyze_consistent_results(self, analyzer):
        """Test that repeated analysis gives consistent results."""
        result1 = analyzer.analyze("GB", 5)
        result2 = analyzer.analyze("GB", 5)
        assert result1.rental_income.start_period_total == result2.rental_income.start_period_total
        assert result1.rental_income.end_period_total == result2.rental_income.end_period_total
        assert result1.growth_metrics.nominal_cagr_percent == result2.growth_metrics.nominal_cagr_percent
