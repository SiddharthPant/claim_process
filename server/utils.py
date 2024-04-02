from typing import Annotated

from pydantic import ValidationError, WrapValidator


def validate_timestamp(v, handler):
    if isinstance(v, str):
        return float(v.strip().replace("$", ""))
    try:
        return handler(v)
    except ValidationError:
        # validation failed, in this case we want to return a default value
        return 0.0


Float = Annotated[float, WrapValidator(validate_timestamp)]
