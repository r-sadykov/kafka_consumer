import dateutil.parser
from typing import Any, List, TypeVar, Type, cast, Callable
from enum import Enum
from datetime import datetime

T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)

def from_str(x: Any) -> str:
    if isinstance(x, str):
        return x
    else:
        return str(x)

def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x

def from_float(x: Any) -> float:
    assert isinstance(x, float) and not isinstance(x, bool)
    return x

def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x

def from_none(x: Any) -> Any:
    assert x is None
    return x

def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False

def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value

def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()

def from_stringified_bool(x: str) -> bool:
    if x == "true":
        return True
    else:
        return False

def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    if isinstance(x, list):
        return [f(y) for y in x]
    else:
        return [f(x)]   

def is_type(t: Type[T], x: Any) -> T:
    assert isinstance(x, t)
    return x

def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)