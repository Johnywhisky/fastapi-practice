from pydantic.errors import PydanticValueError


class ExistsError(PydanticValueError):
    code = "exists"
    msg_template = "{msg}"


class NotFoundError(PydanticValueError):
    code = "not_found"
    msg_template = "{msg}"
