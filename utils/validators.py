"""
validators.py
─────────────
Input validation functions. Called before simulation starts.
Raises ValueError with clear, user-friendly messages on bad input.
"""

MAX_CACHE_SIZE   = 20
MAX_REFERENCES   = 100


def validate_cache_size(value: str) -> int:
    """
    Validates and converts cache size input.

    Args:
        value (str): Raw string from the GUI entry field

    Returns:
        int: Validated cache size

    Raises:
        ValueError: With a descriptive message for the user
    """
    value = value.strip()

    if not value:
        raise ValueError("Cache size cannot be empty.")

    if not value.isdigit():
        raise ValueError("Cache size must be a positive integer (e.g. 3).")

    size = int(value)

    if size < 1:
        raise ValueError("Cache size must be at least 1.")

    if size > MAX_CACHE_SIZE:
        raise ValueError(f"Cache size cannot exceed {MAX_CACHE_SIZE}.")

    return size


def validate_reference_string(value: str) -> list:
    """
    Validates and converts the reference string input.

    Args:
        value (str): Space-separated page numbers from GUI entry

    Returns:
        list[int]: Validated list of page integers

    Raises:
        ValueError: With a descriptive message for the user
    """
    value = value.strip()

    if not value:
        raise ValueError("Reference string cannot be empty.")

    tokens = value.split()

    if len(tokens) > MAX_REFERENCES:
        raise ValueError(
            f"Reference string is too long. Maximum {MAX_REFERENCES} references allowed."
        )

    pages = []
    for i, token in enumerate(tokens):
        if not token.lstrip('-').isdigit():
            raise ValueError(
                f"Invalid value '{token}' at position {i + 1}. "
                f"All values must be integers."
            )
        num = int(token)
        if num < 0:
            raise ValueError(
                f"Page number at position {i + 1} must be non-negative."
            )
        pages.append(num)

    return pages
