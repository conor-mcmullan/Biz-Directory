import re

def sanitize_string(input_str: str) -> str:
    """
    Sanitizes the input string by:
    - Replacing spaces with underscores
    - Converting to lowercase
    - Removing special characters not allowed in collection names

    Args:
        input_str (str): The string to sanitize.

    Returns:
        str: The sanitized string.
    """
    # Replace spaces with underscores
    sanitized = input_str.replace(' ', '_').lower()
    
    # Remove special characters except underscores, hyphens, and alphanumeric characters
    sanitized = re.sub(r'[^a-zA-Z0-9_]', '', sanitized)
    
    return sanitized
