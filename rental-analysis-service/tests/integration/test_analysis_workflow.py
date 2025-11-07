"""End-to-end workflow tests for rental income analysis."""

import pytest
from fastapi.testclient import TestClient

from src.api.main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


class TestCompleteAnalysisWorkflow:
    """Test complete analysis workflow from request to response."""

    def test_workflow_us_one_year(self, client):
        """Test complete workflow for US with 1-year analysis."""
        response = client.get("/analysis/US?years=1")
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify country and period
        assert data["country_code"] == "US"
        assert data["analysis_period_years"] == 1
        
        # Verify date range
        assert data["date_range"]["start_date"] == "2024-01"
        assert data["date_range"]["end_date"] == "2024-12"
        
        # Verify rental income
        assert data["rental_income"]["start_period_total"] > 0
        assert data["rental_income"]["end_period_total"] > 0
        assert data["rental_income"]["currency"] == "USD"
        
        # Verify growth metrics
        assert "nominal_cagr_percent" in data["growth_metrics"]
        assert "cumulative_inflation_percent" in data["growth_metrics"]
        assert "real_cagr_percent" in data["growth_metrics"]
        
        # Verify portfolio summary
        assert data["portfolio_summary"]["buildings_analyzed"] == 10
        assert data["portfolio_summary"]["total_months"] == 12

    def test_workflow_gb_three_years(self, client):
        """Test complete workflow for GB with 3-year analysis."""
        response = client.get("/analysis/GB?years=3")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["country_code"] == "GB"
        assert data["analysis_period_years"] == 3
        assert data["date_range"]["start_date"] == "2022-01"
        assert data["date_range"]["end_date"] == "2024-12"
        assert data["rental_income"]["currency"] == "GBP"
        assert data["portfolio_summary"]["buildings_analyzed"] == 10
        assert data["portfolio_summary"]["total_months"] == 36

    def test_workflow_de_five_years(self, client):
        """Test complete workflow for DE with 5-year analysis."""
        response = client.get("/analysis/DE?years=5")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["country_code"] == "DE"
        assert data["analysis_period_years"] == 5
        assert data["date_range"]["start_date"] == "2020-01"
        assert data["date_range"]["end_date"] == "2024-12"
        assert data["rental_income"]["currency"] == "EUR"
        assert data["portfolio_summary"]["buildings_analyzed"] == 10
        assert data["portfolio_summary"]["total_months"] == 60

    def test_workflow_all_countries_five_years(self, client):
        """Test workflow for all countries with 5-year analysis."""
        countries = {
            "US": "USD",
            "GB": "GBP",
            "DE": "EUR",
            "FR": "EUR",
            "JP": "JPY",
        }
        
        for country, currency in countries.items():
            response = client.get(f"/analysis/{country}?years=5")
            assert response.status_code == 200
            
            data = response.json()
            assert data["country_code"] == country
            assert data["rental_income"]["currency"] == currency
            assert data["portfolio_summary"]["buildings_analyzed"] == 10

    def test_workflow_growth_calculations_reasonable(self, client):
        """Test that growth calculations produce reasonable results."""
        response = client.get("/analysis/US?years=5")
        
        assert response.status_code == 200
        data = response.json()
        
        # Nominal CAGR should be positive (rental growth)
        nominal_cagr = data["growth_metrics"]["nominal_cagr_percent"]
        assert nominal_cagr > 0
        assert nominal_cagr < 50  # Reasonable upper bound
        
        # Cumulative inflation should be positive
        inflation = data["growth_metrics"]["cumulative_inflation_percent"]
        assert inflation > 0
        assert inflation < 100  # Reasonable upper bound
        
        # Real CAGR should be less than nominal (inflation-adjusted)
        real_cagr = data["growth_metrics"]["real_cagr_percent"]
        assert real_cagr < nominal_cagr

    def test_workflow_rental_income_growth(self, client):
        """Test that rental income shows growth over time."""
        response = client.get("/analysis/GB?years=5")
        
        assert response.status_code == 200
        data = response.json()
        
        start_total = data["rental_income"]["start_period_total"]
        end_total = data["rental_income"]["end_period_total"]
        
        # End should be greater than start (with growth)
        assert end_total > start_total
        
        # Growth should be reasonable (not more than 2x in 5 years)
        assert end_total < start_total * 2

    def test_workflow_manual_verification_us_five_years(self, client):
        """Manual verification test for US 5-year analysis.
        
        This test documents expected values for manual verification.
        """
        response = client.get("/analysis/US?years=5")
        
        assert response.status_code == 200
        data = response.json()
        
        # Document the results for manual verification
        print("\n=== Manual Verification: US 5-Year Analysis ===")
        print(f"Country: {data['country_code']}")
        print(f"Period: {data['analysis_period_years']} years")
        print(f"Date Range: {data['date_range']['start_date']} to {data['date_range']['end_date']}")
        print(f"\nRental Income:")
        print(f"  Start: {data['rental_income']['start_period_total']:,.2f} {data['rental_income']['currency']}")
        print(f"  End: {data['rental_income']['end_period_total']:,.2f} {data['rental_income']['currency']}")
        print(f"\nGrowth Metrics:")
        print(f"  Nominal CAGR: {data['growth_metrics']['nominal_cagr_percent']:.2f}%")
        print(f"  Cumulative Inflation: {data['growth_metrics']['cumulative_inflation_percent']:.2f}%")
        print(f"  Real CAGR: {data['growth_metrics']['real_cagr_percent']:.2f}%")
        print(f"\nPortfolio:")
        print(f"  Buildings: {data['portfolio_summary']['buildings_analyzed']}")
        print(f"  Months: {data['portfolio_summary']['total_months']}")
        
        # Basic sanity checks
        assert data["country_code"] == "US"
        assert data["analysis_period_years"] == 5
        assert data["portfolio_summary"]["buildings_analyzed"] == 10
        assert data["portfolio_summary"]["total_months"] == 60


class TestPerformance:
    """Test API performance."""

    def test_response_time_under_two_seconds(self, client):
        """Test that response time is under 2 seconds."""
        import time
        
        start_time = time.time()
        response = client.get("/analysis/US?years=5")
        end_time = time.time()
        
        assert response.status_code == 200
        
        response_time = end_time - start_time
        assert response_time < 2.0, f"Response time {response_time:.2f}s exceeds 2s limit"

    def test_multiple_requests_performance(self, client):
        """Test performance with multiple sequential requests."""
        import time
        
        start_time = time.time()
        
        for _ in range(5):
            response = client.get("/analysis/GB?years=3")
            assert response.status_code == 200
        
        end_time = time.time()
        total_time = end_time - start_time
        avg_time = total_time / 5
        
        assert avg_time < 2.0, f"Average response time {avg_time:.2f}s exceeds 2s limit"


class TestErrorScenarios:
    """Test error handling in complete workflows."""

    def test_workflow_invalid_country_full_error(self, client):
        """Test complete error workflow for invalid country."""
        response = client.get("/analysis/XX?years=5")
        
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "No data found" in data["detail"]

    def test_workflow_invalid_years_full_error(self, client):
        """Test complete error workflow for invalid years."""
        response = client.get("/analysis/US?years=7")
        
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "must be one of" in data["detail"]

    def test_workflow_insufficient_data_error(self, client):
        """Test error workflow for insufficient data period."""
        # With corrected calculation, 10-year analysis now works (2015-2024)
        # This test now verifies that 10-year analysis succeeds
        response = client.get("/analysis/US?years=10")
        
        assert response.status_code == 200
        data = response.json()
        assert data["analysis_period_years"] == 10
        assert data["portfolio_summary"]["total_months"] == 120


class TestDataConsistency:
    """Test data consistency across requests."""

    def test_same_request_same_result(self, client):
        """Test that identical requests return identical results."""
        response1 = client.get("/analysis/FR?years=3")
        response2 = client.get("/analysis/FR?years=3")
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        data1 = response1.json()
        data2 = response2.json()
        
        # Results should be identical
        assert data1 == data2

    def test_different_periods_different_results(self, client):
        """Test that different periods return different results."""
        response1 = client.get("/analysis/JP?years=1")
        response3 = client.get("/analysis/JP?years=3")
        response5 = client.get("/analysis/JP?years=5")
        
        assert response1.status_code == 200
        assert response3.status_code == 200
        assert response5.status_code == 200
        
        data1 = response1.json()
        data3 = response3.json()
        data5 = response5.json()
        
        # Different periods should have different metrics
        assert data1["growth_metrics"] != data3["growth_metrics"]
        assert data3["growth_metrics"] != data5["growth_metrics"]
        assert data1["growth_metrics"] != data5["growth_metrics"]
