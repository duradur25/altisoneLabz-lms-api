from fastapi import Query

class Pagination:
    def __init__(
        self,
        page: int = Query(default=1, ge=1, description="Which page"),
        limit: int = Query(default=10, ge=1, le=100, description="Amount data per page")
    ):
        self.page = page
        self.limit = limit
        self.offset = (page - 1) * limit