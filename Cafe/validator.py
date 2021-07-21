from django.core.exceptions import ValidationError


def discount_validator(value):
    if value < 0 or value > 100:
        raise ValidationError('enter a number between 0 and 100')