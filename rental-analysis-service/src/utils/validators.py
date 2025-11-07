"""Input validation utilities."""

from typing import Literal


class ValidationError(ValueError):
    """Custom validation error."""

    pass


def validate_country_code(country_code: str) -> str:
    """Validate and normalize country code.

    Args:
        country_code: Country code to validate

    Returns:
        Normalized (uppercase) country code

    Raises:
        ValidationError: If country code is invalid
    """
    if not country_code:
        raise ValidationError("Country code cannot be empty")

    if not isinstance(country_code, str):
        raise ValidationError("Country code must be a string")

    if len(country_code) != 2:
        raise ValidationError(
            f"Country code must be exactly 2 characters, got {len(country_code)}"
        )

    if not country_code.isalpha():
        raise ValidationError("Country code must contain only letters")

    return country_code.upper()


def validate_years(years: int) -> Literal[1, 3, 5, 10]:
    """Validate years parameter.

    Args:
        years: Years to validate

    Returns:
        Validated years value

    Raises:
        ValidationError: If years is invalid
    """
    if not isinstance(years, int):
        raise ValidationError("Years must be an integer")

    if years not in [1, 3, 5, 10]:
        raise ValidationError(
            f"Years must be one of [1, 3, 5, 10], got {years}"
        )

    return years
