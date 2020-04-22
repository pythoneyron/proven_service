from django.core.exceptions import ValidationError


def validate_even_number(value):
    if value > 5:
        raise ValidationError(
            'Значение не может быть больше 5',
            params={'value': value},
        )
