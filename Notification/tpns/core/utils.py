def remove_null_values(dictionary: dict) -> dict:
    """Create a new dictionary without keys mapped to null values.

    Args:
        dictionary: The dictionary potentially containing keys mapped to values of None.

    Returns:
        A dict with no keys mapped to None.
    """
    if isinstance(dictionary, dict):
        return {k: v for (k, v) in dictionary.items() if v is not None}
    return dictionary


def cleanup_values(dictionary: dict) -> dict:
    """Create a new dictionary with boolean values converted to strings.

    Ex. true -> 'true', false -> 'false'.
    { 'key': true } -> { 'key': 'true' }

    Args:
        dictionary: The dictionary with keys mapped to booleans.

    Returns:
        The dictionary with certain keys mapped to s and not booleans.
    """
    if isinstance(dictionary, dict):
        return {k: cleanup_value(v) for (k, v) in dictionary.items()}
    return dictionary


def cleanup_value(value: any) -> any:
    """Convert a boolean value to string."""
    if isinstance(value, bool):
        return 'true' if value else 'false'
    return value


def strip_extra_slashes(value: str) -> str:
    """Combine multiple trailing slashes to a single slash"""
    if value.endswith('//'):
        return value.rstrip('/') + '/'
    return value


def merge_params(data: dict, params: dict):
    if params is not None and isinstance(params, dict):
        data.update(params)
