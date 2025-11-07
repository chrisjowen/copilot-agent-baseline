"""Data loader service for CSV files."""

from pathlib import Path
from typing import Optional

import pandas as pd


class DataLoader:
    """Loads and filters data from CSV files."""

    def __init__(self, data_dir: Path):
        """Initialize DataLoader with data directory.

        Args:
            data_dir: Path to directory containing CSV files

        Raises:
            ValueError: If data directory does not exist
        """
        if not data_dir.exists() or not data_dir.is_dir():
            raise ValueError(f"Data directory does not exist: {data_dir}")
        self.data_dir = data_dir

    def load_rentals(
        self,
        country_code: Optional[str] = None,
        start_year: Optional[int] = None,
        end_year: Optional[int] = None,
    ) -> pd.DataFrame:
        """Load rental data from CSV with optional filtering.

        Args:
            country_code: Filter by country code (e.g., 'US')
            start_year: Filter by start year (inclusive)
            end_year: Filter by end year (inclusive)

        Returns:
            DataFrame with rental records

        Raises:
            FileNotFoundError: If rentals.csv not found
        """
        rentals_path = self.data_dir / "rentals.csv"
        if not rentals_path.exists():
            raise FileNotFoundError(f"rentals.csv not found at {rentals_path}")

        df = pd.read_csv(rentals_path)

        if country_code:
            df = df[df["country_code"] == country_code.upper()]

        if start_year is not None:
            df = df[df["year"] >= start_year]

        if end_year is not None:
            df = df[df["year"] <= end_year]

        return df

    def load_inflation(
        self,
        country_code: Optional[str] = None,
        start_year: Optional[int] = None,
        end_year: Optional[int] = None,
    ) -> pd.DataFrame:
        """Load inflation data from CSV with optional filtering.

        Args:
            country_code: Filter by country code (e.g., 'US')
            start_year: Filter by start year (inclusive)
            end_year: Filter by end year (inclusive)

        Returns:
            DataFrame with inflation records

        Raises:
            FileNotFoundError: If inflation.csv not found
        """
        inflation_path = self.data_dir / "inflation.csv"
        if not inflation_path.exists():
            raise FileNotFoundError(f"inflation.csv not found at {inflation_path}")

        df = pd.read_csv(inflation_path)

        if country_code:
            df = df[df["country_code"] == country_code.upper()]

        if start_year is not None:
            df = df[df["year"] >= start_year]

        if end_year is not None:
            df = df[df["year"] <= end_year]

        return df

    def load_buildings(self, country_code: Optional[str] = None) -> pd.DataFrame:
        """Load building data from CSV with optional filtering.

        Args:
            country_code: Filter by country code (e.g., 'US')

        Returns:
            DataFrame with building records

        Raises:
            FileNotFoundError: If buildings.csv not found
        """
        buildings_path = self.data_dir / "buildings.csv"
        if not buildings_path.exists():
            raise FileNotFoundError(f"buildings.csv not found at {buildings_path}")

        df = pd.read_csv(buildings_path)

        if country_code:
            df = df[df["country_code"] == country_code.upper()]

        return df

    def get_available_countries(self) -> list[str]:
        """Get list of available country codes from building data.

        Returns:
            Sorted list of unique country codes
        """
        df = self.load_buildings()
        countries = sorted(df["country_code"].unique().tolist())
        return countries

    def get_date_range(self, country_code: Optional[str] = None) -> tuple[int, int]:
        """Get available date range from rental data.

        Args:
            country_code: Optional country code to filter by

        Returns:
            Tuple of (start_year, end_year)
        """
        df = self.load_rentals(country_code=country_code)
        start_year = int(df["year"].min())
        end_year = int(df["year"].max())
        return start_year, end_year
