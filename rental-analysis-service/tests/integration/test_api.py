"""Integration tests for FastAPI endpoints."""

import pytest
from fastapi.testclient import TestClient

from src.api.main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


class TestHealthEndpoint:
    """Test health check endpoint."""

    def test_health_endpoint_exists(self, client):
        """Test that health endpoint exists."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_endpoint_returns_json(self, client):
        """Test that health endpoint returns JSON."""
        response = client.get("/health")
        assert response.headers["content-type"] == "application/json"

    def test_health_endpoint_has_status(self, client):
        """Test that health endpoint returns status."""
        response = client.get("/health")
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"


class TestAnalysisEndpoint:
    """Test analysis endpoint."""

    def test_analysis_endpoint_exists(self, client):
        """Test that analysis endpoint exists."""
        response = client.get("/analysis/US?years=5")
        assert response.status_code in [200, 400, 404, 422]

    def test_analysis_endpoint_valid_request(self, client):
        """Test analysis endpoint with valid request."""
        response = client.get("/analysis/US?years=5")
        assert response.status_code == 200

    def test_analysis_endpoint_returns_json(self, client):
        """Test that analysis endpoint returns JSON."""
        response = client.get("/analysis/US?years=5")
        assert response.headers["content-type"] == "application/json"

    def test_analysis_endpoint_response_structure(self, client):
        """Test that response has expected structure."""
        response = client.get("/analysis/GB?years=3")
        assert response.status_code == 200
        data = response.json()
        
        # Check top-level fields
        assert "country_code" in data
        assert "analysis_period_years" in data
        assert "date_range" in data
        assert "rental_income" in data
        assert "growth_metrics" in data
        assert "portfolio_summary" in data

    def test_analysis_endpoint_date_range_structure(self, client):
        """Test date_range structure in response."""
        response = client.get("/analysis/DE?years=1")
        assert response.status_code == 200
        data = response.json()
        
        assert "start_date" in data["date_range"]
        assert "end_date" in data["date_range"]

    def test_analysis_endpoint_rental_income_structure(self, client):
        """Test rental_income structure in response."""
        response = client.get("/analysis/FR?years=3")
        assert response.status_code == 200
        data = response.json()
        
        assert "start_period_total" in data["rental_income"]
        assert "end_period_total" in data["rental_income"]
        assert "currency" in data["rental_income"]

    def test_analysis_endpoint_growth_metrics_structure(self, client):
        """Test growth_metrics structure in response."""
        response = client.get("/analysis/JP?years=5")
        assert response.status_code == 200
        data = response.json()
        
        assert "nominal_cagr_percent" in data["growth_metrics"]
        assert "cumulative_inflation_percent" in data["growth_metrics"]
        assert "real_cagr_percent" in data["growth_metrics"]

    def test_analysis_endpoint_portfolio_summary_structure(self, client):
        """Test portfolio_summary structure in response."""
        response = client.get("/analysis/US?years=1")
        assert response.status_code == 200
        data = response.json()
        
        assert "buildings_analyzed" in data["portfolio_summary"]
        assert "total_months" in data["portfolio_summary"]

    def test_analysis_endpoint_all_valid_periods(self, client):
        """Test analysis endpoint with all valid periods."""
        for years in [1, 3, 5, 10]:
            response = client.get(f"/analysis/US?years={years}")
            assert response.status_code == 200
            data = response.json()
            assert data["analysis_period_years"] == years

    def test_analysis_endpoint_all_countries(self, client):
        """Test analysis endpoint with all test countries."""
        countries = ["US", "GB", "DE", "FR", "JP"]
        for country in countries:
            response = client.get(f"/analysis/{country}?years=5")
            assert response.status_code == 200
            data = response.json()
            assert data["country_code"] == country

    def test_analysis_endpoint_lowercase_country(self, client):
        """Test that lowercase country code is accepted."""
        response = client.get("/analysis/us?years=5")
        assert response.status_code == 200
        data = response.json()
        assert data["country_code"] == "US"

    def test_analysis_endpoint_invalid_country(self, client):
        """Test analysis endpoint with invalid country."""
        response = client.get("/analysis/XX?years=5")
        assert response.status_code == 404

    def test_analysis_endpoint_invalid_country_error_message(self, client):
        """Test error message for invalid country."""
        response = client.get("/analysis/XX?years=5")
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data

    def test_analysis_endpoint_invalid_years(self, client):
        """Test analysis endpoint with invalid years parameter."""
        response = client.get("/analysis/US?years=7")
        assert response.status_code == 400

    def test_analysis_endpoint_invalid_years_error_message(self, client):
        """Test error message for invalid years."""
        response = client.get("/analysis/US?years=7")
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data

    def test_analysis_endpoint_missing_years(self, client):
        """Test analysis endpoint without years parameter."""
        response = client.get("/analysis/US")
        assert response.status_code == 422  # Unprocessable Entity

    def test_analysis_endpoint_non_numeric_years(self, client):
        """Test analysis endpoint with non-numeric years."""
        response = client.get("/analysis/US?years=abc")
        assert response.status_code == 422

    def test_analysis_endpoint_negative_years(self, client):
        """Test analysis endpoint with negative years."""
        response = client.get("/analysis/US?years=-5")
        assert response.status_code == 400

    def test_analysis_endpoint_zero_years(self, client):
        """Test analysis endpoint with zero years."""
        response = client.get("/analysis/US?years=0")
        assert response.status_code == 400

    def test_analysis_endpoint_country_too_short(self, client):
        """Test analysis endpoint with country code too short."""
        response = client.get("/analysis/U?years=5")
        assert response.status_code == 422

    def test_analysis_endpoint_country_too_long(self, client):
        """Test analysis endpoint with country code too long."""
        response = client.get("/analysis/USA?years=5")
        assert response.status_code == 422

    def test_analysis_endpoint_response_values_positive(self, client):
        """Test that response values are positive where expected."""
        response = client.get("/analysis/GB?years=5")
        assert response.status_code == 200
        data = response.json()
        
        assert data["rental_income"]["start_period_total"] > 0
        assert data["rental_income"]["end_period_total"] > 0
        assert data["portfolio_summary"]["buildings_analyzed"] > 0
        assert data["portfolio_summary"]["total_months"] > 0

    def test_analysis_endpoint_consistent_results(self, client):
        """Test that repeated requests return consistent results."""
        response1 = client.get("/analysis/DE?years=3")
        response2 = client.get("/analysis/DE?years=3")
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        data1 = response1.json()
        data2 = response2.json()
        
        assert data1 == data2


class TestOpenAPIDocumentation:
    """Test OpenAPI documentation."""

    def test_openapi_json_exists(self, client):
        """Test that OpenAPI JSON is available."""
        response = client.get("/openapi.json")
        assert response.status_code == 200

    def test_openapi_json_is_valid(self, client):
        """Test that OpenAPI JSON is valid."""
        response = client.get("/openapi.json")
        data = response.json()
        
        assert "openapi" in data
        assert "info" in data
        assert "paths" in data

    def test_docs_endpoint_exists(self, client):
        """Test that Swagger docs endpoint exists."""
        response = client.get("/docs")
        assert response.status_code == 200

    def test_redoc_endpoint_exists(self, client):
        """Test that ReDoc endpoint exists."""
        response = client.get("/redoc")
        assert response.status_code == 200
