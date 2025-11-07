"""Unit tests for Pydantic schemas."""

import pytest
from pydantic import ValidationError

from src.models.schemas import (
    AnalysisResponse,
    BuildingRecord,
    DateRange,
    GrowthMetrics,
    InflationRecord,
    PortfolioSummary,
    RentalIncome,
    RentalRecord,
)


class TestRentalRecord:
    """Tests for RentalRecord model."""

    def test_valid_rental_record(self):
        """Test creating a valid rental record."""
        record = RentalRecord(
            building_id="B001",
            tenant_id="T001",
            country_code="US",
            month=1,
            year=2020,
            rental_amount=5000.00,
            currency="USD",
        )
        assert record.building_id == "B001"
        assert record.tenant_id == "T001"
        assert record.country_code == "US"
        assert record.month == 1
        assert record.year == 2020
        assert record.rental_amount == 5000.00
        assert record.currency == "USD"

    def test_country_code_uppercase_conversion(self):
        """Test country code is converted to uppercase."""
        record = RentalRecord(
            building_id="B001",
            tenant_id="T001",
            country_code="us",
            month=1,
            year=2020,
            rental_amount=5000.00,
            currency="usd",
        )
        assert record.country_code == "US"
        assert record.currency == "USD"

    def test_invalid_month(self):
        """Test validation fails for invalid month."""
        with pytest.raises(ValidationError):
            RentalRecord(
                building_id="B001",
                tenant_id="T001",
                country_code="US",
                month=13,
                year=2020,
                rental_amount=5000.00,
                currency="USD",
            )

    def test_invalid_year(self):
        """Test validation fails for invalid year."""
        with pytest.raises(ValidationError):
            RentalRecord(
                building_id="B001",
                tenant_id="T001",
                country_code="US",
                month=1,
                year=1999,
                rental_amount=5000.00,
                currency="USD",
            )

    def test_negative_rental_amount(self):
        """Test validation fails for negative rental amount."""
        with pytest.raises(ValidationError):
            RentalRecord(
                building_id="B001",
                tenant_id="T001",
                country_code="US",
                month=1,
                year=2020,
                rental_amount=-100.00,
                currency="USD",
            )

    def test_invalid_country_code_length(self):
        """Test validation fails for invalid country code length."""
        with pytest.raises(ValidationError):
            RentalRecord(
                building_id="B001",
                tenant_id="T001",
                country_code="USA",
                month=1,
                year=2020,
                rental_amount=5000.00,
                currency="USD",
            )


class TestInflationRecord:
    """Tests for InflationRecord model."""

    def test_valid_inflation_record(self):
        """Test creating a valid inflation record."""
        record = InflationRecord(
            country_code="US", year=2020, month=1, inflation_rate=0.0021
        )
        assert record.country_code == "US"
        assert record.year == 2020
        assert record.month == 1
        assert record.inflation_rate == 0.0021

    def test_country_code_uppercase_conversion(self):
        """Test country code is converted to uppercase."""
        record = InflationRecord(
            country_code="gb", year=2020, month=1, inflation_rate=0.0018
        )
        assert record.country_code == "GB"

    def test_negative_inflation_rate(self):
        """Test negative inflation rate is allowed (deflation)."""
        record = InflationRecord(
            country_code="US", year=2020, month=1, inflation_rate=-0.001
        )
        assert record.inflation_rate == -0.001


class TestBuildingRecord:
    """Tests for BuildingRecord model."""

    def test_valid_building_record(self):
        """Test creating a valid building record."""
        record = BuildingRecord(
            building_id="B001",
            country_code="US",
            name="Downtown Plaza",
            property_type="Office",
            city="New York",
        )
        assert record.building_id == "B001"
        assert record.country_code == "US"
        assert record.name == "Downtown Plaza"
        assert record.property_type == "Office"
        assert record.city == "New York"

    def test_country_code_uppercase_conversion(self):
        """Test country code is converted to uppercase."""
        record = BuildingRecord(
            building_id="B001",
            country_code="de",
            name="Berlin Tower",
            property_type="Office",
            city="Berlin",
        )
        assert record.country_code == "DE"


class TestDateRange:
    """Tests for DateRange model."""

    def test_valid_date_range(self):
        """Test creating a valid date range."""
        date_range = DateRange(start_date="2019-01", end_date="2024-01")
        assert date_range.start_date == "2019-01"
        assert date_range.end_date == "2024-01"


class TestRentalIncome:
    """Tests for RentalIncome model."""

    def test_valid_rental_income(self):
        """Test creating valid rental income summary."""
        income = RentalIncome(
            start_period_total=1250000.00, end_period_total=1450000.00, currency="USD"
        )
        assert income.start_period_total == 1250000.00
        assert income.end_period_total == 1450000.00
        assert income.currency == "USD"

    def test_negative_rental_income_fails(self):
        """Test validation fails for negative rental income."""
        with pytest.raises(ValidationError):
            RentalIncome(
                start_period_total=-100.00, end_period_total=1450000.00, currency="USD"
            )


class TestGrowthMetrics:
    """Tests for GrowthMetrics model."""

    def test_valid_growth_metrics(self):
        """Test creating valid growth metrics."""
        metrics = GrowthMetrics(
            nominal_cagr_percent=3.02,
            cumulative_inflation_percent=12.5,
            real_cagr_percent=-1.8,
        )
        assert metrics.nominal_cagr_percent == 3.02
        assert metrics.cumulative_inflation_percent == 12.5
        assert metrics.real_cagr_percent == -1.8

    def test_negative_growth_allowed(self):
        """Test negative growth rates are allowed."""
        metrics = GrowthMetrics(
            nominal_cagr_percent=-2.5,
            cumulative_inflation_percent=5.0,
            real_cagr_percent=-7.0,
        )
        assert metrics.nominal_cagr_percent == -2.5


class TestPortfolioSummary:
    """Tests for PortfolioSummary model."""

    def test_valid_portfolio_summary(self):
        """Test creating valid portfolio summary."""
        summary = PortfolioSummary(buildings_analyzed=45, total_months=60)
        assert summary.buildings_analyzed == 45
        assert summary.total_months == 60

    def test_negative_values_fail(self):
        """Test validation fails for negative values."""
        with pytest.raises(ValidationError):
            PortfolioSummary(buildings_analyzed=-1, total_months=60)


class TestAnalysisResponse:
    """Tests for AnalysisResponse model."""

    def test_valid_analysis_response(self):
        """Test creating a complete valid analysis response."""
        response = AnalysisResponse(
            country_code="US",
            analysis_period_years=5,
            date_range=DateRange(start_date="2019-01", end_date="2024-01"),
            rental_income=RentalIncome(
                start_period_total=1250000.00,
                end_period_total=1450000.00,
                currency="USD",
            ),
            growth_metrics=GrowthMetrics(
                nominal_cagr_percent=3.02,
                cumulative_inflation_percent=12.5,
                real_cagr_percent=-1.8,
            ),
            portfolio_summary=PortfolioSummary(buildings_analyzed=45, total_months=60),
        )
        assert response.country_code == "US"
        assert response.analysis_period_years == 5
        assert response.date_range.start_date == "2019-01"
        assert response.rental_income.start_period_total == 1250000.00
        assert response.growth_metrics.nominal_cagr_percent == 3.02
        assert response.portfolio_summary.buildings_analyzed == 45

    def test_invalid_analysis_period(self):
        """Test validation fails for invalid analysis period."""
        with pytest.raises(ValidationError):
            AnalysisResponse(
                country_code="US",
                analysis_period_years=7,  # Not in [1, 3, 5, 10]
                date_range=DateRange(start_date="2019-01", end_date="2024-01"),
                rental_income=RentalIncome(
                    start_period_total=1250000.00,
                    end_period_total=1450000.00,
                    currency="USD",
                ),
                growth_metrics=GrowthMetrics(
                    nominal_cagr_percent=3.02,
                    cumulative_inflation_percent=12.5,
                    real_cagr_percent=-1.8,
                ),
                portfolio_summary=PortfolioSummary(
                    buildings_analyzed=45, total_months=60
                ),
            )
