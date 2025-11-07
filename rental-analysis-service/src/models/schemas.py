"""Pydantic models and data schemas for rental income analysis."""

from datetime import date
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class RentalRecord(BaseModel):
    """Represents a single rental payment record from CSV."""

    building_id: str = Field(..., description="Unique building identifier")
    tenant_id: str = Field(..., description="Unique tenant identifier")
    country_code: str = Field(..., min_length=2, max_length=2, description="ISO country code")
    month: int = Field(..., ge=1, le=12, description="Month (1-12)")
    year: int = Field(..., ge=2000, le=2100, description="Year")
    rental_amount: float = Field(..., ge=0, description="Rental amount in local currency")
    currency: str = Field(..., min_length=3, max_length=3, description="ISO currency code")

    @field_validator("country_code")
    @classmethod
    def country_code_uppercase(cls, v: str) -> str:
        """Ensure country code is uppercase."""
        return v.upper()

    @field_validator("currency")
    @classmethod
    def currency_uppercase(cls, v: str) -> str:
        """Ensure currency code is uppercase."""
        return v.upper()


class InflationRecord(BaseModel):
    """Represents monthly inflation rate for a country."""

    country_code: str = Field(..., min_length=2, max_length=2, description="ISO country code")
    year: int = Field(..., ge=2000, le=2100, description="Year")
    month: int = Field(..., ge=1, le=12, description="Month (1-12)")
    inflation_rate: float = Field(..., description="Monthly inflation rate (e.g., 0.0021 = 0.21%)")

    @field_validator("country_code")
    @classmethod
    def country_code_uppercase(cls, v: str) -> str:
        """Ensure country code is uppercase."""
        return v.upper()


class BuildingRecord(BaseModel):
    """Represents a building in the portfolio."""

    building_id: str = Field(..., description="Unique building identifier")
    country_code: str = Field(..., min_length=2, max_length=2, description="ISO country code")
    name: str = Field(..., description="Building name")
    property_type: str = Field(..., description="Property type (e.g., Office, Retail, Industrial)")
    city: str = Field(..., description="City location")

    @field_validator("country_code")
    @classmethod
    def country_code_uppercase(cls, v: str) -> str:
        """Ensure country code is uppercase."""
        return v.upper()


class DateRange(BaseModel):
    """Date range for analysis period."""

    start_date: str = Field(..., description="Start date in YYYY-MM format")
    end_date: str = Field(..., description="End date in YYYY-MM format")


class RentalIncome(BaseModel):
    """Rental income summary for analysis period."""

    start_period_total: float = Field(..., ge=0, description="Total rental income at start of period")
    end_period_total: float = Field(..., ge=0, description="Total rental income at end of period")
    currency: str = Field(..., min_length=3, max_length=3, description="ISO currency code")


class GrowthMetrics(BaseModel):
    """Growth and inflation metrics."""

    nominal_cagr_percent: float = Field(..., description="Nominal CAGR as percentage")
    cumulative_inflation_percent: float = Field(..., description="Cumulative inflation as percentage")
    real_cagr_percent: float = Field(..., description="Real (inflation-adjusted) CAGR as percentage")


class PortfolioSummary(BaseModel):
    """Summary of portfolio analyzed."""

    buildings_analyzed: int = Field(..., ge=0, description="Number of buildings in analysis")
    total_months: int = Field(..., ge=0, description="Number of months analyzed")


class AnalysisResponse(BaseModel):
    """Complete analysis response."""

    country_code: str = Field(..., min_length=2, max_length=2, description="ISO country code")
    analysis_period_years: Literal[1, 3, 5, 10] = Field(..., description="Analysis period in years")
    date_range: DateRange = Field(..., description="Date range analyzed")
    rental_income: RentalIncome = Field(..., description="Rental income summary")
    growth_metrics: GrowthMetrics = Field(..., description="Growth and inflation metrics")
    portfolio_summary: PortfolioSummary = Field(..., description="Portfolio summary")

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "country_code": "US",
                "analysis_period_years": 5,
                "date_range": {"start_date": "2019-01", "end_date": "2024-01"},
                "rental_income": {
                    "start_period_total": 1250000.00,
                    "end_period_total": 1450000.00,
                    "currency": "USD",
                },
                "growth_metrics": {
                    "nominal_cagr_percent": 3.02,
                    "cumulative_inflation_percent": 12.5,
                    "real_cagr_percent": -1.8,
                },
                "portfolio_summary": {"buildings_analyzed": 45, "total_months": 60},
            }
        }
