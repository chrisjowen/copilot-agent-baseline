# Business Overview

## Project Name
Commercial Real Estate Portfolio Analysis Service

## Business Context

### Problem Statement
Our organization manages a commercial real estate portfolio spanning approximately 20 countries with around 1,400 buildings. We need to analyze rental income growth over time and compare it against inflation rates in each country to understand real returns on our investments.

Currently, there is no systematic way to:
- Track rental income growth across multiple countries
- Compare nominal growth against inflation
- Calculate real (inflation-adjusted) returns
- Analyze performance over standard time periods (1, 3, 5, and 10 years)

### Business Goals
1. **Performance Analysis**: Understand how rental income is growing relative to inflation in each country
2. **Investment Decisions**: Identify countries where real returns are strongest or weakest
3. **Portfolio Optimization**: Make data-driven decisions about where to invest or divest
4. **Stakeholder Reporting**: Provide clear metrics on portfolio performance

### Success Metrics
- Ability to analyze any country in the portfolio on-demand
- Calculate accurate CAGR (Compound Annual Growth Rate) for rental income
- Compare nominal vs real (inflation-adjusted) growth rates
- Support standard analysis periods: 1, 3, 5, and 10 years
- Process data for 1,400+ buildings across 20 countries

## Target Users

### Primary Users
- **Portfolio Managers**: Need to assess country-level performance
- **Investment Analysts**: Require detailed growth and inflation comparisons
- **Executive Leadership**: Need high-level portfolio performance metrics

### Use Cases
1. **Country Performance Review**: Analyze a specific country's rental income growth over a defined period
2. **Comparative Analysis**: Compare multiple countries' real returns
3. **Investment Planning**: Identify markets with strong real growth for expansion
4. **Risk Assessment**: Identify markets where inflation is eroding returns

## Business Rules

### Data Scope
- **Portfolio Size**: ~1,400 buildings across ~20 countries
- **Tenant Structure**: Multiple tenants per building
- **Data Granularity**: Monthly rental income per tenant
- **Time Periods**: 1, 3, 5, and 10-year analysis windows

### Calculation Methodology
- **Growth Calculation**: CAGR from start to end of period
- **Inflation Adjustment**: Monthly inflation rates compounded over period
- **Real Growth**: Nominal CAGR adjusted for cumulative inflation
- **Currency**: Analysis performed in local currency per country

### Data Assumptions
- Complete data availability for requested time periods
- Monthly rental data for all active tenants
- Monthly inflation rates for all countries
- Consistent currency per country

## Business Constraints

### Data Sources
- **Rental Data**: Provided via CSV files (monthly tenant-level data)
- **Inflation Data**: Provided via CSV files (monthly country-level rates)
- **Building Data**: Provided via CSV files (building metadata)

### Technical Constraints
- File-based data storage (no database required initially)
- REST API interface (no UI)
- Service-oriented architecture
- Python-based implementation

### Operational Constraints
- Analysis on-demand (not scheduled/batch)
- Country-specific queries only
- Standard time periods only (1, 3, 5, 10 years)

## Future Considerations

### Potential Enhancements
- Property type segmentation (retail, office, industrial)
- City or region-level analysis
- Vacancy rate impact analysis
- Currency conversion for cross-country comparisons
- Predictive analytics and forecasting
- Automated reporting and alerts
- Historical trend visualization
- Benchmark comparisons against market indices

### Scalability Needs
- Support for portfolio growth beyond 1,400 buildings
- Additional countries beyond current 20
- More granular time period analysis
- Integration with property management systems
- Real-time data updates

---

**Document Owner**: Development Team  
**Last Updated**: 2025-11-07  
**Next Review**: After initial implementation
