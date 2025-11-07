"""FastAPI application for rental income analysis."""

from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse

from src.models.schemas import AnalysisResponse
from src.services.analyzer import Analyzer
from src.services.calculator import Calculator
from src.services.data_loader import DataLoader

# Initialize FastAPI app
app = FastAPI(
    title="Rental Income Analysis API",
    description="Analyze rental income growth vs inflation for commercial real estate portfolios",
    version="1.0.0",
)

# Initialize services
data_dir = Path(__file__).parent.parent.parent / "data"
data_loader = DataLoader(data_dir)
calculator = Calculator()
analyzer = Analyzer(data_loader, calculator)


@app.get("/health")
async def health_check():
    """Health check endpoint.

    Returns:
        Status information
    """
    return {"status": "healthy"}


@app.get("/analysis/{country_code}", response_model=AnalysisResponse)
async def analyze_rental_income(
    country_code: str,
    years: int = Query(..., description="Analysis period in years (1, 3, 5, or 10)"),
):
    """Analyze rental income growth vs inflation for a country.

    Args:
        country_code: ISO 2-letter country code (e.g., 'US', 'GB')
        years: Analysis period in years (must be 1, 3, 5, or 10)

    Returns:
        AnalysisResponse with complete analysis results

    Raises:
        HTTPException: 400 for invalid parameters, 404 for country not found
    """
    # Validate country code format
    if len(country_code) != 2:
        raise HTTPException(
            status_code=422,
            detail="Country code must be exactly 2 characters",
        )

    # Validate years parameter
    if years not in [1, 3, 5, 10]:
        raise HTTPException(
            status_code=400,
            detail=f"Years must be one of [1, 3, 5, 10], got {years}",
        )

    try:
        # Perform analysis
        result = analyzer.analyze(country_code.upper(), years)
        return result

    except ValueError as e:
        error_msg = str(e)
        
        # Check if it's a "not found" error
        if "No data found" in error_msg or "Insufficient data" in error_msg:
            raise HTTPException(status_code=404, detail=error_msg)
        
        # Otherwise it's a bad request
        raise HTTPException(status_code=400, detail=error_msg)

    except Exception as e:
        # Unexpected error
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}",
        )
