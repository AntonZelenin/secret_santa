import json
import random

from django.http import HttpRequest


# todo delete?
def load_json(request: HttpRequest) -> dict | list:
    if not request.body:
        return {}

    raw_json = request.body.decode('utf-8')
    return json.loads(raw_json)


def generate_6_digit_code() -> str:
    return str(random.randint(1000000, 9999999) // 10)


def generate_random_string(length: int = 64) -> str:
    return ''.join(random.choice('0123456789abcdef') for _ in range(length))
