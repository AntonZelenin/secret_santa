import json
import random

from django.http import HttpRequest


def load_json(request: HttpRequest) -> dict | list:
    raw_json = request.body.decode('utf-8')
    return json.loads(raw_json)


def generate_6_digit_code() -> str:
    return str(random.randint(1000000, 9999999) // 10)
