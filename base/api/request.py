class FilterRequest:
    LIKE = 'LIKE'
    NOT_LIKE = 'NOT LIKE'
    AND = '^'
    OR = '^OR'

    __filters: list
    __operands: list

    def __init__(self, filter_field: str, filter_type: str, target: str):
        self.__filters = []
        self.__operands = []
        self.__add_filter(filter_field, filter_type, target)

    @property
    def target(self) -> str:
        return self.__filters[0]['target']

    def and_filter(self, filter_field: str, filter_type: str, target: str) -> None:
        self.__add_filter(filter_field, filter_type, target)
        self.__operands.append(self.AND)

    def or_filter(self, filter_field: str, filter_type: str, target: str) -> None:
        self.__add_filter(filter_field, filter_type, target)
        self.__operands.append(self.OR)

    def get_request_str(self) -> str:
        query = self.__get_filter_str(0)
        for index in range(1, len(self.__filters)):
            query += self.__operands[index - 1]
            query += self.__get_filter_str(index)
        return query

    def __get_filter_str(self, index: int) -> str:
        filters = self.__filters[index]
        return f"{filters['filter_field']}{filters['filter_type']}{filters['target']}"

    def __add_filter(self, filter_field: str, filter_type: str, target: str) -> None:
        self.__filters.append({
            'target': target,
            'filter_field': filter_field,
            'filter_type': filter_type,
        })


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
