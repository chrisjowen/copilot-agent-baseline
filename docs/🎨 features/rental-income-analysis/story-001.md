# Story 001: Rental Income Analysis Service

## Story Information
- **Story Number**: 001
- **Title**: Build REST API for Commercial Real Estate Rental Income Analysis
- **Priority**: High
- **Estimated Effort**: Large
- **Status**: Planning

## Description
Build a REST API service that analyzes rental income growth from a commercial real estate portfolio across multiple countries and compares it against inflation rates to calculate real returns. The service will process CSV data for ~1,400 buildings across ~20 countries and provide on-demand analysis for specified time periods.

## User Stories
- As a **portfolio manager**, I want to analyze rental income growth for a specific country over a defined period so that I can assess investment performance
- As an **investment analyst**, I want to compare nominal rental growth against inflation so that I can understand real returns
- As an **executive**, I want to query country-level performance metrics so that I can make data-driven portfolio decisions

## Acceptance Criteria
- [ ] API accepts GET requests with country code and analysis period (1, 3, 5, or 10 years)
- [ ] Service loads rental, inflation, and building data from CSV files
- [ ] Service calculates nominal CAGR for rental income over the specified period
- [ ] Service calculates cumulative inflation for the specified period
- [ ] Service calculates real (inflation-adjusted) CAGR
- [ ] API returns JSON response with all calculated metrics
- [ ] Response includes start/end period rental totals, growth rates, and portfolio summary
- [ ] Service handles requests for any of the 20 countries in the portfolio
- [ ] All calculations use monthly data granularity
- [ ] Test data generated for 50 buildings across 5 countries

## Business Context

### Problem Statement
Portfolio managers need to understand how rental income is performing relative to inflation in each country. Without this analysis, it's difficult to:
- Identify markets with strong real returns
- Detect markets where inflation is eroding returns
- Make informed investment and divestment decisions
- Report accurate performance metrics to stakeholders

### Success Metrics
- API responds within 2 seconds for any country analysis
- Accurate CAGR calculations matching financial standards
- Correct inflation adjustment methodology
- Complete data coverage for requested time periods
- 100% test coverage for calculation logic

### Assumptions
- Complete monthly data available for all requested time periods
- All rental amounts in local currency for each country
- Monthly inflation rates provided (not annualized)
- No currency conversion needed (analysis per country in local currency)
- Buildings with multiple tenants aggregate to building-level income

## Technical Requirements

### Functional Requirements
1. **API Endpoint**: `GET /analysis/{country_code}?years={1|3|5|10}`
2. **Data Loading**: Read and parse three CSV files (rentals, inflation, buildings)
3. **Data Filtering**: Filter data by country code and date range
4. **Rental Aggregation**: Sum all tenant rental income by month
5. **CAGR Calculation**: Calculate compound annual growth rate from start to end period
6. **Inflation Calculation**: Compound monthly inflation rates over the period
7. **Real Return Calculation**: Adjust nominal CAGR by cumulative inflation
8. **Response Formatting**: Return structured JSON with all metrics

### Non-Functional Requirements
- **Performance**: Response time < 2 seconds per request
- **Accuracy**: Financial calculations accurate to 2 decimal places
- **Reliability**: Handle missing or malformed data gracefully
- **Maintainability**: Clean, well-tested, documented code
- **Scalability**: Support 1,400 buildings, 20 countries, 10 years of data

## Dependencies

### Internal Dependencies
- [ ] Python 3.11+ environment
- [ ] FastAPI framework
- [ ] Pandas for data processing
- [ ] Pydantic for data validation

### External Dependencies
- [ ] CSV data files (rentals, inflation, buildings)
- [ ] Test data generation for 50 buildings, 5 countries

## Risks and Considerations

### Technical Risks
- **Data Volume**: Processing 10 years of monthly data for 1,400 buildings could impact performance
  - *Mitigation*: Use Pandas for efficient filtering, implement caching if needed
- **Calculation Accuracy**: CAGR and inflation compounding must be precise
  - *Mitigation*: Use proven financial formulas, extensive unit testing
- **Data Quality**: Missing or inconsistent CSV data could cause errors
  - *Mitigation*: Implement validation, assume complete data for initial version

### Business Risks
- **Incomplete Data**: Real-world data may have gaps not present in test data
  - *Impact*: Analysis results may be inaccurate or unavailable
  - *Mitigation*: Document data completeness assumptions, plan for future enhancement

## Definition of Done
- [ ] All acceptance criteria met
- [ ] All tests pass (unit, integration, e2e)
- [ ] Test coverage > 80%
- [ ] Code review completed
- [ ] API documentation complete
- [ ] Architecture documentation updated
- [ ] Test data generated and validated
- [ ] Service can be run locally and responds to requests
- [ ] All calculations verified against manual calculations

## Notes

### Data Schema Confirmed
**Rental CSV**: `building_id, tenant_id, country_code, month, year, rental_amount, currency`
**Inflation CSV**: `country_code, year, month, inflation_rate` (monthly rate)
**Building CSV**: `building_id, country_code, name, property_type, city`

### Calculation Methodology
- **CAGR Formula**: `((End Value / Start Value) ^ (1 / Years)) - 1`
- **Cumulative Inflation**: Compound monthly rates over period
- **Real CAGR**: `((1 + Nominal CAGR) / (1 + Cumulative Inflation)) - 1`

### Test Data Scope
- 5 countries (e.g., US, GB, DE, FR, JP)
- 50 buildings (10 per country)
- 10 years of monthly data (2015-2024)
- 3-5 tenants per building on average
- Realistic rental amounts and inflation rates
