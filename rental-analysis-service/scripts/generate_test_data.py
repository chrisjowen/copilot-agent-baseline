"""Generate test data for rental income analysis service.

Creates CSV files with realistic test data:
- 50 buildings across 5 countries (US, GB, DE, FR, JP)
- 10 years of monthly rental data (2015-2024)
- 10 years of monthly inflation data per country
- 3-5 tenants per building on average
"""

import csv
import random
from datetime import datetime
from pathlib import Path

# Configuration
COUNTRIES = {
    "US": {"currency": "USD", "avg_rent": 5000, "avg_inflation": 0.0020},
    "GB": {"currency": "GBP", "avg_rent": 4000, "avg_inflation": 0.0018},
    "DE": {"currency": "EUR", "avg_rent": 3500, "avg_inflation": 0.0015},
    "FR": {"currency": "EUR", "avg_rent": 3800, "avg_inflation": 0.0016},
    "JP": {"currency": "JPY", "avg_rent": 500000, "avg_inflation": 0.0005},
}

PROPERTY_TYPES = ["Office", "Retail", "Industrial", "Mixed Use"]
CITIES = {
    "US": ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"],
    "GB": ["London", "Manchester", "Birmingham", "Leeds", "Glasgow"],
    "DE": ["Berlin", "Munich", "Hamburg", "Frankfurt", "Cologne"],
    "FR": ["Paris", "Lyon", "Marseille", "Toulouse", "Nice"],
    "JP": ["Tokyo", "Osaka", "Yokohama", "Nagoya", "Sapporo"],
}

BUILDINGS_PER_COUNTRY = 10
START_YEAR = 2015
END_YEAR = 2024
TENANTS_PER_BUILDING_MIN = 3
TENANTS_PER_BUILDING_MAX = 5


def generate_buildings() -> list[dict]:
    """Generate building records."""
    buildings = []
    building_counter = 1

    for country_code in COUNTRIES.keys():
        for i in range(BUILDINGS_PER_COUNTRY):
            building_id = f"B{building_counter:03d}"
            buildings.append(
                {
                    "building_id": building_id,
                    "country_code": country_code,
                    "name": f"{random.choice(CITIES[country_code])} {random.choice(['Tower', 'Plaza', 'Center', 'Building'])} {i+1}",
                    "property_type": random.choice(PROPERTY_TYPES),
                    "city": random.choice(CITIES[country_code]),
                }
            )
            building_counter += 1

    return buildings


def generate_rentals(buildings: list[dict]) -> list[dict]:
    """Generate rental records for all buildings and time periods."""
    rentals = []
    tenant_counter = 1

    for building in buildings:
        country_code = building["country_code"]
        country_info = COUNTRIES[country_code]
        num_tenants = random.randint(TENANTS_PER_BUILDING_MIN, TENANTS_PER_BUILDING_MAX)

        # Generate tenants for this building
        for tenant_num in range(num_tenants):
            tenant_id = f"T{tenant_counter:04d}"
            tenant_counter += 1

            # Base rental amount with some variation
            base_rent = country_info["avg_rent"] * random.uniform(0.7, 1.3)

            # Generate monthly records for entire period
            for year in range(START_YEAR, END_YEAR + 1):
                for month in range(1, 13):
                    # Add some growth and variation over time
                    years_elapsed = year - START_YEAR + (month - 1) / 12
                    growth_factor = 1 + (0.02 * years_elapsed)  # 2% annual growth
                    monthly_variation = random.uniform(0.98, 1.02)
                    rental_amount = base_rent * growth_factor * monthly_variation

                    rentals.append(
                        {
                            "building_id": building["building_id"],
                            "tenant_id": tenant_id,
                            "country_code": country_code,
                            "month": month,
                            "year": year,
                            "rental_amount": round(rental_amount, 2),
                            "currency": country_info["currency"],
                        }
                    )

    return rentals


def generate_inflation() -> list[dict]:
    """Generate monthly inflation rates for all countries."""
    inflation_records = []

    for country_code, country_info in COUNTRIES.items():
        base_inflation = country_info["avg_inflation"]

        for year in range(START_YEAR, END_YEAR + 1):
            for month in range(1, 13):
                # Add some variation to inflation rates
                variation = random.uniform(0.7, 1.3)
                # Add some cyclical patterns
                seasonal_factor = 1 + 0.2 * (month - 6.5) / 6.5
                inflation_rate = base_inflation * variation * seasonal_factor

                inflation_records.append(
                    {
                        "country_code": country_code,
                        "year": year,
                        "month": month,
                        "inflation_rate": round(inflation_rate, 6),
                    }
                )

    return inflation_records


def write_csv(filename: str, data: list[dict], fieldnames: list[str]) -> None:
    """Write data to CSV file."""
    filepath = Path(__file__).parent.parent / "data" / filename
    filepath.parent.mkdir(parents=True, exist_ok=True)

    with open(filepath, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    print(f"✅ Generated {filename}: {len(data)} records")


def main():
    """Generate all test data files."""
    print("Generating test data...")
    print(f"Configuration:")
    print(f"  - Countries: {len(COUNTRIES)}")
    print(f"  - Buildings per country: {BUILDINGS_PER_COUNTRY}")
    print(f"  - Total buildings: {len(COUNTRIES) * BUILDINGS_PER_COUNTRY}")
    print(f"  - Time period: {START_YEAR}-{END_YEAR}")
    print(f"  - Tenants per building: {TENANTS_PER_BUILDING_MIN}-{TENANTS_PER_BUILDING_MAX}")
    print()

    # Generate buildings
    buildings = generate_buildings()
    write_csv(
        "buildings.csv",
        buildings,
        ["building_id", "country_code", "name", "property_type", "city"],
    )

    # Generate rentals
    rentals = generate_rentals(buildings)
    write_csv(
        "rentals.csv",
        rentals,
        ["building_id", "tenant_id", "country_code", "month", "year", "rental_amount", "currency"],
    )

    # Generate inflation
    inflation = generate_inflation()
    write_csv(
        "inflation.csv",
        inflation,
        ["country_code", "year", "month", "inflation_rate"],
    )

    print()
    print("✅ Test data generation complete!")
    print()
    print("Summary:")
    print(f"  - Buildings: {len(buildings)}")
    print(f"  - Rental records: {len(rentals)}")
    print(f"  - Inflation records: {len(inflation)}")


if __name__ == "__main__":
    main()
