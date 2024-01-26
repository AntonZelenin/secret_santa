from abc import ABC
from dataclasses import dataclass
from typing import TypeVar, Generic

from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse

T = TypeVar('T')


class Result(ABC, Generic[T]):
    def __init__(self):
        raise NotImplementedError()


@dataclass
class Ok(Result[T]):
    value: T = None


@dataclass
class Err(Result[T]):
    error: str

    def __str__(self):
        return self.error


class ErrJsonResponse(JsonResponse):
    def __init__(
            self,
            err,
            encoder=DjangoJSONEncoder,
            safe=True,
            json_dumps_params=None,
            **kwargs,
    ):
        super().__init__(
            data={'error': err},
            encoder=encoder,
            safe=safe,
            json_dumps_params=json_dumps_params,
            **kwargs,
        )
