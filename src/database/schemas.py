from datetime import datetime

from humps import camelize
from pydantic import BaseModel, SecretStr


def to_camel(key: str) -> str:
    return camelize(key)


class MyBase(BaseModel):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True
        anystr_strip_whitespace = True
        arbitrary_types_allowed = True
        orm_mode = True
        validate_assignment = True

        json_encoders = {
            # custom output conversion for datetime
            datetime: lambda v: v.strftime("%Y-%m-%dT%H:%M:%SZ") if v else None,
            SecretStr: lambda v: v.get_secret_value() if v else None,
        }
