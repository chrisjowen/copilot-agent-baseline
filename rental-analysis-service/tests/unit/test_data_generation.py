"""Tests to validate generated test data."""

import csv
from pathlib import Path

import pytest


@pytest.fixture
def data_dir():
    """Get path to data directory."""
    return Path(__file__).parent.parent.parent / "data"


class TestBuildingsData:
    """Tests for buildings.csv."""

    def test_buildings_file_exists(self, data_dir):
        """Test buildings.csv file exists."""
        assert (data_dir / "buildings.csv").exists()

    def test_buildings_count(self, data_dir):
        """Test correct number of buildings (50)."""
        with open(data_dir / "buildings.csv", "r") as f:
            reader = csv.DictReader(f)
            buildings = list(reader)
        assert len(buildings) == 50

    def test_buildings_structure(self, data_dir):
        """Test buildings have correct fields."""
        with open(data_dir / "buildings.csv", "r") as f:
            reader = csv.DictReader(f)
            building = next(reader)
        
        required_fields = ["building_id", "country_code", "name", "property_type", "city"]
        for field in required_fields:
            assert field in building
            assert building[field]  # Not empty

    def test_buildings_countries(self, data_dir):
        """Test buildings span 5 countries."""
        with open(data_dir / "buildings.csv", "r") as f:
            reader = csv.DictReader(f)
            countries = {row["country_code"] for row in reader}
        
        assert len(countries) == 5
        assert countries == {"US", "GB", "DE", "FR", "JP"}

    def test_buildings_per_country(self, data_dir):
        """Test 10 buildings per country."""
        with open(data_dir / "buildings.csv", "r") as f:
            reader = csv.DictReader(f)
            country_counts = {}
            for row in reader:
                country = row["country_code"]
                country_counts[country] = country_counts.get(country, 0) + 1
        
        for country, count in country_counts.items():
            assert count == 10, f"Country {country} has {count} buildings, expected 10"


class TestRentalsData:
    """Tests for rentals.csv."""

    def test_rentals_file_exists(self, data_dir):
        """Test rentals.csv file exists."""
        assert (data_dir / "rentals.csv").exists()

    def test_rentals_structure(self, data_dir):
        """Test rentals have correct fields."""
        with open(data_dir / "rentals.csv", "r") as f:
            reader = csv.DictReader(f)
            rental = next(reader)
        
        required_fields = [
            "building_id",
            "tenant_id",
            "country_code",
            "month",
            "year",
            "rental_amount",
            "currency",
        ]
        for field in required_fields:
            assert field in rental
            assert rental[field]  # Not empty

    def test_rentals_time_range(self, data_dir):
        """Test rentals span 2015-2024."""
        with open(data_dir / "rentals.csv", "r") as f:
            reader = csv.DictReader(f)
            years = {int(row["year"]) for row in reader}
        
        assert min(years) == 2015
        assert max(years) == 2024
        assert len(years) == 10  # All years present

    def test_rentals_months(self, data_dir):
        """Test rentals include all months."""
        with open(data_dir / "rentals.csv", "r") as f:
            reader = csv.DictReader(f)
            months = {int(row["month"]) for row in reader}
        
        assert months == set(range(1, 13))

    def test_rental_amounts_positive(self, data_dir):
        """Test all rental amounts are positive."""
        with open(data_dir / "rentals.csv", "r") as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                if i > 100:  # Sample first 100 rows
                    break
                assert float(row["rental_amount"]) > 0


class TestInflationData:
    """Tests for inflation.csv."""

    def test_inflation_file_exists(self, data_dir):
        """Test inflation.csv file exists."""
        assert (data_dir / "inflation.csv").exists()

    def test_inflation_count(self, data_dir):
        """Test correct number of inflation records (5 countries × 10 years × 12 months)."""
        with open(data_dir / "inflation.csv", "r") as f:
            reader = csv.DictReader(f)
            records = list(reader)
        assert len(records) == 600  # 5 × 10 × 12

    def test_inflation_structure(self, data_dir):
        """Test inflation records have correct fields."""
        with open(data_dir / "inflation.csv", "r") as f:
            reader = csv.DictReader(f)
            record = next(reader)
        
        required_fields = ["country_code", "year", "month", "inflation_rate"]
        for field in required_fields:
            assert field in record
            assert record[field]  # Not empty

    def test_inflation_countries(self, data_dir):
        """Test inflation data for all 5 countries."""
        with open(data_dir / "inflation.csv", "r") as f:
            reader = csv.DictReader(f)
            countries = {row["country_code"] for row in reader}
        
        assert countries == {"US", "GB", "DE", "FR", "JP"}

    def test_inflation_time_range(self, data_dir):
        """Test inflation data spans 2015-2024."""
        with open(data_dir / "inflation.csv", "r") as f:
            reader = csv.DictReader(f)
            years = {int(row["year"]) for row in reader}
        
        assert min(years) == 2015
        assert max(years) == 2024
        assert len(years) == 10


class TestDataConsistency:
    """Tests for data consistency across files."""

    def test_rental_buildings_exist(self, data_dir):
        """Test all buildings in rentals.csv exist in buildings.csv."""
        # Load building IDs
        with open(data_dir / "buildings.csv", "r") as f:
            reader = csv.DictReader(f)
            building_ids = {row["building_id"] for row in reader}
        
        # Check rental building IDs
        with open(data_dir / "rentals.csv", "r") as f:
            reader = csv.DictReader(f)
            rental_building_ids = {row["building_id"] for row in reader}
        
        assert rental_building_ids.issubset(building_ids)

    def test_country_codes_consistent(self, data_dir):
        """Test country codes are consistent across all files."""
        # Get countries from buildings
        with open(data_dir / "buildings.csv", "r") as f:
            reader = csv.DictReader(f)
            building_countries = {row["country_code"] for row in reader}
        
        # Get countries from rentals
        with open(data_dir / "rentals.csv", "r") as f:
            reader = csv.DictReader(f)
            rental_countries = {row["country_code"] for row in reader}
        
        # Get countries from inflation
        with open(data_dir / "inflation.csv", "r") as f:
            reader = csv.DictReader(f)
            inflation_countries = {row["country_code"] for row in reader}
        
        assert building_countries == rental_countries == inflation_countries
