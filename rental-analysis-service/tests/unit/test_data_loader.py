"""Unit tests for data loader service."""

import pandas as pd
import pytest
from pathlib import Path

from src.services.data_loader import DataLoader


@pytest.fixture
def data_loader():
    """Create a DataLoader instance with test data directory."""
    data_dir = Path(__file__).parent.parent.parent / "data"
    return DataLoader(data_dir)


class TestDataLoaderInitialization:
    """Test DataLoader initialization."""

    def test_init_with_valid_directory(self, data_loader):
        """Test initialization with valid data directory."""
        assert data_loader.data_dir.exists()
        assert data_loader.data_dir.is_dir()

    def test_init_with_invalid_directory(self):
        """Test initialization with non-existent directory."""
        with pytest.raises(ValueError, match="Data directory does not exist"):
            DataLoader(Path("/nonexistent/path"))


class TestLoadRentals:
    """Test loading rental data."""

    def test_load_rentals_returns_dataframe(self, data_loader):
        """Test that load_rentals returns a DataFrame."""
        df = data_loader.load_rentals()
        assert isinstance(df, pd.DataFrame)

    def test_load_rentals_has_expected_columns(self, data_loader):
        """Test that rental data has all expected columns."""
        df = data_loader.load_rentals()
        expected_columns = [
            "building_id",
            "tenant_id",
            "country_code",
            "month",
            "year",
            "rental_amount",
            "currency",
        ]
        assert all(col in df.columns for col in expected_columns)

    def test_load_rentals_not_empty(self, data_loader):
        """Test that rental data is not empty."""
        df = data_loader.load_rentals()
        assert len(df) > 0

    def test_load_rentals_with_country_filter(self, data_loader):
        """Test filtering rentals by country code."""
        df = data_loader.load_rentals(country_code="US")
        assert len(df) > 0
        assert all(df["country_code"] == "US")

    def test_load_rentals_with_invalid_country(self, data_loader):
        """Test filtering with non-existent country returns empty DataFrame."""
        df = data_loader.load_rentals(country_code="XX")
        assert len(df) == 0

    def test_load_rentals_with_date_range(self, data_loader):
        """Test filtering rentals by date range."""
        df = data_loader.load_rentals(start_year=2020, end_year=2022)
        assert len(df) > 0
        assert all(df["year"] >= 2020)
        assert all(df["year"] <= 2022)

    def test_load_rentals_with_country_and_date_range(self, data_loader):
        """Test filtering rentals by both country and date range."""
        df = data_loader.load_rentals(country_code="GB", start_year=2020, end_year=2022)
        assert len(df) > 0
        assert all(df["country_code"] == "GB")
        assert all(df["year"] >= 2020)
        assert all(df["year"] <= 2022)

    def test_load_rentals_missing_file(self, tmp_path):
        """Test error handling when rentals file is missing."""
        loader = DataLoader(tmp_path)
        with pytest.raises(FileNotFoundError, match="rentals.csv not found"):
            loader.load_rentals()


class TestLoadInflation:
    """Test loading inflation data."""

    def test_load_inflation_returns_dataframe(self, data_loader):
        """Test that load_inflation returns a DataFrame."""
        df = data_loader.load_inflation()
        assert isinstance(df, pd.DataFrame)

    def test_load_inflation_has_expected_columns(self, data_loader):
        """Test that inflation data has all expected columns."""
        df = data_loader.load_inflation()
        expected_columns = ["country_code", "year", "month", "inflation_rate"]
        assert all(col in df.columns for col in expected_columns)

    def test_load_inflation_not_empty(self, data_loader):
        """Test that inflation data is not empty."""
        df = data_loader.load_inflation()
        assert len(df) > 0

    def test_load_inflation_with_country_filter(self, data_loader):
        """Test filtering inflation by country code."""
        df = data_loader.load_inflation(country_code="US")
        assert len(df) > 0
        assert all(df["country_code"] == "US")

    def test_load_inflation_with_date_range(self, data_loader):
        """Test filtering inflation by date range."""
        df = data_loader.load_inflation(start_year=2020, end_year=2022)
        assert len(df) > 0
        assert all(df["year"] >= 2020)
        assert all(df["year"] <= 2022)

    def test_load_inflation_with_country_and_date_range(self, data_loader):
        """Test filtering inflation by both country and date range."""
        df = data_loader.load_inflation(country_code="DE", start_year=2020, end_year=2022)
        assert len(df) > 0
        assert all(df["country_code"] == "DE")
        assert all(df["year"] >= 2020)
        assert all(df["year"] <= 2022)

    def test_load_inflation_missing_file(self, tmp_path):
        """Test error handling when inflation file is missing."""
        loader = DataLoader(tmp_path)
        with pytest.raises(FileNotFoundError, match="inflation.csv not found"):
            loader.load_inflation()


class TestLoadBuildings:
    """Test loading building data."""

    def test_load_buildings_returns_dataframe(self, data_loader):
        """Test that load_buildings returns a DataFrame."""
        df = data_loader.load_buildings()
        assert isinstance(df, pd.DataFrame)

    def test_load_buildings_has_expected_columns(self, data_loader):
        """Test that building data has all expected columns."""
        df = data_loader.load_buildings()
        expected_columns = ["building_id", "country_code", "name", "property_type", "city"]
        assert all(col in df.columns for col in expected_columns)

    def test_load_buildings_not_empty(self, data_loader):
        """Test that building data is not empty."""
        df = data_loader.load_buildings()
        assert len(df) > 0

    def test_load_buildings_with_country_filter(self, data_loader):
        """Test filtering buildings by country code."""
        df = data_loader.load_buildings(country_code="FR")
        assert len(df) > 0
        assert all(df["country_code"] == "FR")

    def test_load_buildings_missing_file(self, tmp_path):
        """Test error handling when buildings file is missing."""
        loader = DataLoader(tmp_path)
        with pytest.raises(FileNotFoundError, match="buildings.csv not found"):
            loader.load_buildings()


class TestGetAvailableCountries:
    """Test getting list of available countries."""

    def test_get_available_countries_returns_list(self, data_loader):
        """Test that get_available_countries returns a list."""
        countries = data_loader.get_available_countries()
        assert isinstance(countries, list)

    def test_get_available_countries_not_empty(self, data_loader):
        """Test that available countries list is not empty."""
        countries = data_loader.get_available_countries()
        assert len(countries) > 0

    def test_get_available_countries_contains_expected(self, data_loader):
        """Test that available countries includes expected test countries."""
        countries = data_loader.get_available_countries()
        expected_countries = ["US", "GB", "DE", "FR", "JP"]
        for country in expected_countries:
            assert country in countries

    def test_get_available_countries_sorted(self, data_loader):
        """Test that available countries are sorted."""
        countries = data_loader.get_available_countries()
        assert countries == sorted(countries)


class TestGetDateRange:
    """Test getting available date range."""

    def test_get_date_range_returns_tuple(self, data_loader):
        """Test that get_date_range returns a tuple."""
        date_range = data_loader.get_date_range()
        assert isinstance(date_range, tuple)
        assert len(date_range) == 2

    def test_get_date_range_valid_years(self, data_loader):
        """Test that date range contains valid years."""
        start_year, end_year = data_loader.get_date_range()
        assert isinstance(start_year, int)
        assert isinstance(end_year, int)
        assert start_year <= end_year
        assert start_year >= 2000
        assert end_year <= 2100

    def test_get_date_range_with_country_filter(self, data_loader):
        """Test getting date range for specific country."""
        start_year, end_year = data_loader.get_date_range(country_code="JP")
        assert isinstance(start_year, int)
        assert isinstance(end_year, int)
        assert start_year <= end_year
