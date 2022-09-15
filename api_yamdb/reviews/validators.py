import re

from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_category(value):
    if re.search(r"^[a-zA-Z][a-zA-Z0-9-_\.]$", value) is None:
        raise ValidationError(
            (f"Не допустимые символы <{value}> в названии Категория!"),
            params={"value": value},
        )


def validate_year(value):
    now = timezone.now().year
    if value > now:
        raise ValidationError(
            f"{value} не может быть больше {now}!",
            params={"value": value, "now": now},
        )


def validate_username(value):
    if re.search(r"^[a-zA-Z0-9_-]{3,16}$", value) is None or value == "me":
        raise ValidationError(
            (f"Не допустимый username: <{value}>!"),
            params={"value": value},
        )
