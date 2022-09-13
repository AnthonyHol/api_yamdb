import re

from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_category(value):
    if re.search(r'^[a-zA-Z][a-zA-Z0-9-_\.]$', value) is None:
        raise ValidationError(
            (f'Не допустимые символы <{value}> в названии Категория!'),
            params={'value': value},
        )


def validate_year(value):
    now = timezone.now().year
    if value > now:
        raise ValidationError(
            f'{value} не может быть больше {now}!',
            params={'value': value, 'now': now},
        )


def validate_rating(value):
    if value not in range(0, 11):
        raise ValidationError(
            f'{value} не может быть оценкой! Оценка должна быть от 0 до 10!'
        )
