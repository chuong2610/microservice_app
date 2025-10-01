class BaseResponse:
    status_code: int
    message: str
    data: dict | list | None = None