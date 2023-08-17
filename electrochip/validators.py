from django.core.exceptions import ValidationError
import re

def validate_phone_number(value):
    # Remove any non-digit characters from the input
    clean_value = re.sub(r'\D', '', value)

    # Check if the phone number starts with '+' or '0'
    if not clean_value.startswith(('+', '0')):
        raise ValidationError("Phone number must start with + or 0")

    # Check if the phone number contains at least 7 digits
    if len(clean_value) < 8:
        raise ValidationError("Phone number must contain at least 7 digits after the first symbol")

    # Check if the phone number contains more than 12 digits
    if len(clean_value) > 12:
        raise ValidationError("Phone number cannot contain more than 12 digits")

    # If all checks pass, return the cleaned value
    return clean_value
