from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict

T = TypeVar("T")


class APIModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class APIResponse(APIModel, Generic[T]):
    code: int = 0
    message: str = "ok"
    data: T


class PaginationData(APIModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    page_size: int


def success_response(data: Any, message: str = "ok") -> dict[str, Any]:
    return {"code": 0, "message": message, "data": data}
