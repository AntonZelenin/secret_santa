from typing import List

from tools.types import Err, Ok


def foo():
    return Err('foo')


match foo():
    case Err(error):
        print(error)
    case Ok():
        print('ok')
