# Commercial Real Estate Rental Income Analysis Service

REST API service for analyzing rental income growth from a commercial real estate portfolio across multiple countries, comparing growth against inflation rates to calculate real returns.

## Features

- Analyze rental income growth for any country in the portfolio
- Calculate Compound Annual Growth Rate (CAGR) for rental income
- Compare nominal growth against inflation
- Calculate real (inflation-adjusted) returns
- Support for 1, 3, 5, and 10-year analysis periods

## Technology Stack

- **Python**: 3.11+
- **Framework**: FastAPI
- **Data Processing**: Pandas, NumPy
- **Validation**: Pydantic
- **Testing**: Pytest

## Setup

### Prerequisites

- Python 3.11 or higher
- pip

### Installation

1. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Service

Start the development server:
```bash
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

Interactive API documentation: `http://localhost:8000/docs`

## API Usage

### Analyze Rental Income

```bash
GET /analysis/{country_code}?years={1|3|5|10}
```

**Example:**
```bash
curl "http://localhost:8000/analysis/US?years=5"
```

**Response:**
```json
{
  "country_code": "US",
  "analysis_period_years": 5,
  "date_range": {
    "start_date": "2019-01",
    "end_date": "2024-01"
  },
  "rental_income": {
    "start_period_total": 1250000.00,
    "end_period_total": 1450000.00,
    "currency": "USD"
  },
  "growth_metrics": {
    "nominal_cagr_percent": 3.02,
    "cumulative_inflation_percent": 12.5,
    "real_cagr_percent": -1.8
  },
  "portfolio_summary": {
    "buildings_analyzed": 45,
    "total_months": 60
  }
}
```

## Testing

Run all tests:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=src --cov-report=html
```

## Development

### Code Formatting
```bash
black src/ tests/
```

### Linting
```bash
ruff check src/ tests/
```

### Type Checking
```bash
mypy src/
```

## Project Structure

```
rental-analysis-service/
├── src/
│   ├── api/              # FastAPI application and routes
│   ├── services/         # Business logic (data loading, analysis, calculations)
│   ├── models/           # Pydantic models and schemas
│   └── utils/            # Utility functions and validators
├── tests/
│   ├── unit/             # Unit tests
│   ├── integration/      # Integration tests
│   └── fixtures/         # Test fixtures and data
├── data/                 # CSV data files
├── scripts/              # Utility scripts (e.g., test data generation)
└── docs/                 # Additional documentation
```

## Data Format

### Rental Data (rentals.csv)
```csv
building_id,tenant_id,country_code,month,year,rental_amount,currency
B001,T001,US,1,2020,5000.00,USD
```

### Inflation Data (inflation.csv)
```csv
country_code,year,month,inflation_rate
US,2020,1,0.0021
```

### Building Data (buildings.csv)
```csv
building_id,country_code,name,property_type,city
B001,US,Downtown Plaza,Office,New York
```

## License

Proprietary - Internal Use Only
