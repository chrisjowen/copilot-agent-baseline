"""Calculator service for CAGR and inflation calculations."""

from typing import Sequence


class Calculator:
    """Provides financial calculation methods for rental income analysis."""

    @staticmethod
    def calculate_cagr(start_value: float, end_value: float, years: int) -> float:
        """Calculate Compound Annual Growth Rate (CAGR).

        Formula: CAGR = ((End_Value / Start_Value) ^ (1 / Years)) - 1

        Args:
            start_value: Starting value (must be > 0)
            end_value: Ending value (must be >= 0)
            years: Number of years (must be > 0)

        Returns:
            CAGR as decimal (e.g., 0.0845 = 8.45%)

        Raises:
            ValueError: If inputs are invalid
        """
        if start_value <= 0:
            raise ValueError("Start value must be greater than zero")
        if end_value < 0:
            raise ValueError("End value cannot be negative")
        if years <= 0:
            raise ValueError("Years must be greater than zero")

        if end_value == 0:
            return -1.0  # Complete loss

        cagr = (end_value / start_value) ** (1 / years) - 1
        return cagr

    @staticmethod
    def calculate_cumulative_inflation(monthly_rates: Sequence[float]) -> float:
        """Calculate cumulative inflation from monthly rates.

        Formula: Cumulative = ((1 + r1) * (1 + r2) * ... * (1 + rN)) - 1

        Args:
            monthly_rates: List of monthly inflation rates as decimals

        Returns:
            Cumulative inflation as decimal

        Raises:
            ValueError: If monthly_rates is empty
        """
        if not monthly_rates:
            raise ValueError("Monthly rates list cannot be empty")

        cumulative = 1.0
        for rate in monthly_rates:
            cumulative *= 1 + rate

        return cumulative - 1

    @staticmethod
    def calculate_real_cagr(nominal_cagr: float, cumulative_inflation: float) -> float:
        """Calculate real (inflation-adjusted) CAGR.

        Formula: Real_CAGR = ((1 + Nominal_CAGR) / (1 + Cumulative_Inflation)) - 1

        Args:
            nominal_cagr: Nominal CAGR as decimal
            cumulative_inflation: Cumulative inflation as decimal

        Returns:
            Real CAGR as decimal

        Raises:
            ValueError: If cumulative_inflation < -1 (invalid)
        """
        if cumulative_inflation < -1:
            raise ValueError("Cumulative inflation cannot be less than -1")

        real_cagr = ((1 + nominal_cagr) / (1 + cumulative_inflation)) - 1
        return real_cagr

    @staticmethod
    def format_percentage(value: float, decimals: int = 2) -> str:
        """Format decimal value as percentage string.

        Args:
            value: Decimal value (e.g., 0.0845)
            decimals: Number of decimal places (default: 2)

        Returns:
            Formatted percentage string (e.g., "8.45%")
        """
        percentage = value * 100
        return f"{percentage:.{decimals}f}%"
