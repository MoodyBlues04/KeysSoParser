class FilterRequest:
    def __init__(self, target: str, filter_field: str, filter_type: str = 'LIKE'):
        self.target = target
        self.filter_field = filter_field
        self.filter_type = filter_type

    def get_request_str(self) -> str:
        return f"{self.filter_field}{self.filter_type}{self.target}"


class RsyaAdsRequest:
    def __init__(self, sort: str = '', page: int = 1, per_page: int = 100, filter: FilterRequest|None = None) -> None:
        self.sort = sort
        self.page = page
        self.per_page = per_page
        self.filter = filter

    def get_request(self) -> dict:
        return {
            'sort': self.sort,
            'page': self.page,
            'per_page': self.per_page,
            'filter': '' if self.filter is None else self.filter.get_request_str()
        }
