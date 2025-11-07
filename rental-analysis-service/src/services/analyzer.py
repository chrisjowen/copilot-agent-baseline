"""Analysis engine for rental income analysis."""

from datetime import date
from typing import Literal

import pandas as pd

from src.models.schemas import (
    AnalysisResponse,
    DateRange,
    GrowthMetrics,
    PortfolioSummary,
    RentalIncome,
)
from src.services.calculator import Calculator
from src.services.data_loader import DataLoader


class Analyzer:
    """Analyzes rental income growth vs inflation for a country portfolio."""

    def __init__(self, data_loader: DataLoader, calculator: Calculator):
        """Initialize Analyzer with dependencies.

        Args:
            data_loader: DataLoader instance for loading CSV data
            calculator: Calculator instance for financial calculations
        """
        self.data_loader = data_loader
        self.calculator = calculator

    def analyze(
        self, country_code: str, years: Literal[1, 3, 5, 10]
    ) -> AnalysisResponse:
        """Perform complete rental income analysis for a country.

        Args:
            country_code: ISO country code (e.g., 'US')
            years: Analysis period in years (1, 3, 5, or 10)

        Returns:
            AnalysisResponse with complete analysis results

        Raises:
            ValueError: If country_code or years are invalid
        """
        if years not in [1, 3, 5, 10]:
            raise ValueError(f"Years must be one of [1, 3, 5, 10], got {years}")

        country_code = country_code.upper()

        # Calculate period dates
        start_date, end_date = self._calculate_period_dates(country_code, years)

        # Aggregate rental income
        rental_data = self._aggregate_rental_income(country_code, start_date, end_date)

        # Get inflation data
        inflation_rates = self._get_inflation_data(country_code, start_date, end_date)

        # Calculate metrics
        nominal_cagr = self.calculator.calculate_cagr(
            rental_data["start_period_total"],
            rental_data["end_period_total"],
            years,
        )

        cumulative_inflation = self.calculator.calculate_cumulative_inflation(
            inflation_rates
        )

        real_cagr = self.calculator.calculate_real_cagr(
            nominal_cagr, cumulative_inflation
        )

        # Get building count
        building_count = self._get_building_count(country_code)

        # Build response
        return AnalysisResponse(
            country_code=country_code,
            analysis_period_years=years,
            date_range=DateRange(
                start_date=start_date.strftime("%Y-%m"),
                end_date=end_date.strftime("%Y-%m"),
            ),
            rental_income=RentalIncome(
                start_period_total=rental_data["start_period_total"],
                end_period_total=rental_data["end_period_total"],
                currency=rental_data["currency"],
            ),
            growth_metrics=GrowthMetrics(
                nominal_cagr_percent=nominal_cagr * 100,
                cumulative_inflation_percent=cumulative_inflation * 100,
                real_cagr_percent=real_cagr * 100,
            ),
            portfolio_summary=PortfolioSummary(
                buildings_analyzed=building_count,
                total_months=rental_data["total_months"],
            ),
        )

    def _calculate_period_dates(
        self, country_code: str, years: int
    ) -> tuple[date, date]:
        """Calculate start and end dates for analysis period.

        Args:
            country_code: ISO country code
            years: Number of years to analyze

        Returns:
            Tuple of (start_date, end_date)

        Raises:
            ValueError: If insufficient data for requested period or country not found
        """
        # Get available date range for country
        try:
            data_start_year, data_end_year = self.data_loader.get_date_range(
                country_code
            )
        except Exception:
            raise ValueError(f"No data found for country {country_code}")

        # Calculate period dates (use most recent data)
        # For N years, we want N complete years: e.g., 1 year = 2024-01 to 2024-12
        end_date = date(data_end_year, 12, 31)
        start_date = date(data_end_year - years + 1, 1, 1)

        # Validate we have enough data
        if start_date.year < data_start_year:
            raise ValueError(
                f"Insufficient data for {years}-year analysis. "
                f"Data available from {data_start_year} to {data_end_year}"
            )

        return start_date, end_date

    def _aggregate_rental_income(
        self, country_code: str, start_date: date, end_date: date
    ) -> dict:
        """Aggregate rental income for the analysis period.

        Args:
            country_code: ISO country code
            start_date: Start date of analysis
            end_date: End date of analysis

        Returns:
            Dictionary with aggregated rental data
        """
        # Load rental data for period
        df = self.data_loader.load_rentals(
            country_code=country_code,
            start_year=start_date.year,
            end_year=end_date.year,
        )

        if df.empty:
            raise ValueError(f"No data found for country {country_code}")

        # Filter to exact date range
        df = df[
            (df["year"] >= start_date.year) & (df["year"] <= end_date.year)
        ].copy()

        # Calculate start period (first month)
        start_month_df = df[(df["year"] == start_date.year) & (df["month"] == 1)]
        start_period_total = start_month_df["rental_amount"].sum()

        # Calculate end period (last month)
        end_month_df = df[(df["year"] == end_date.year) & (df["month"] == 12)]
        end_period_total = end_month_df["rental_amount"].sum()

        # Validate we have data for both periods
        if start_period_total == 0:
            raise ValueError(
                f"No rental data found for {country_code} in {start_date.year}-01"
            )
        if end_period_total == 0:
            raise ValueError(
                f"No rental data found for {country_code} in {end_date.year}-12"
            )

        # Get currency (assume consistent across country)
        currency = df["currency"].iloc[0] if not df.empty else "USD"

        # Calculate total months
        total_months = len(df[["year", "month"]].drop_duplicates())

        return {
            "start_period_total": float(start_period_total),
            "end_period_total": float(end_period_total),
            "currency": currency,
            "total_months": total_months,
        }

    def _get_inflation_data(
        self, country_code: str, start_date: date, end_date: date
    ) -> list[float]:
        """Get monthly inflation rates for the analysis period.

        Args:
            country_code: ISO country code
            start_date: Start date of analysis
            end_date: End date of analysis

        Returns:
            List of monthly inflation rates
        """
        df = self.data_loader.load_inflation(
            country_code=country_code,
            start_year=start_date.year,
            end_year=end_date.year,
        )

        # Sort by year and month
        df = df.sort_values(["year", "month"])

        # Extract rates as list
        rates = df["inflation_rate"].tolist()

        return rates

    def _get_building_count(self, country_code: str) -> int:
        """Get count of buildings for a country.

        Args:
            country_code: ISO country code

        Returns:
            Number of buildings
        """
        df = self.data_loader.load_buildings(country_code=country_code)
        return len(df)
