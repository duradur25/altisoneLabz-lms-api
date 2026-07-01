from fastapi import Query

class Pagination:
    def __init__(
        self,
        page: int = Query(default=1, ge=1, description="Halaman ke berapa"),
        limit: int = Query(default=10, ge=1, le=100, description="Jumlah data per halaman")
    ):
        self.page = page
        self.limit = limit
        self.offset = (page - 1) * limit