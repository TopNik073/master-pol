from typing import Annotated, Literal, Any

from fastapi import Depends, Query


class PaginatedRequestSchema:
    def __init__(
        self,
        page: int = Query(1, gt=0),
        per_page: int = Query(10, gt=0, le=100),
        search_query: str | None = Query(None),
        order_by: str | None = Query(None),
        order_direction: Literal["asc", "desc"] = Query("asc"),
    ):
        self.page = page
        self.per_page = per_page
        self.search_query: str | None = search_query
        self.order_by: str | None = order_by
        self.order_direction: Literal["asc", "desc"] = order_direction

    def dump_to_dict(self) -> dict[str, Any]:
        return self.__dict__


PAGINATED_REQUEST_DEP = Annotated[PaginatedRequestSchema, Depends(PaginatedRequestSchema)]
