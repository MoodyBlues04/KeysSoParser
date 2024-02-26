from .api import KeysSoApi
from .request import RsyaAdsRequest
from .response import RsyaAdsResponse


class RsyaAdsSearchIterator:
    def __init__(self, api: KeysSoApi, request: RsyaAdsRequest):
        self.__api = api
        self.__request = request
        self.__current_page: RsyaAdsResponse | None = None
        self.__item_idx = 0

    def __iter__(self):
        """Initializes iterator"""
        self.__current_page = self.__api.get_rsya_ads(self.__request)
        self.__request.page += 1
        self.__item_idx = 0
        return self

    def __next__(self) -> dict:
        """Next iteration"""
        if self.__item_idx >= len(self.__current_page.data):
            if self.__request.page > self.__current_page.last_page:
                raise StopIteration
            self.__iter__()

        res = self.__current_page.data[self.__item_idx]
        self.__item_idx += 1
        return res

    def next(self):
        """Python 2.0 compatibility"""
        return self.__next__()

    def get_request(self) -> RsyaAdsRequest:
        return self.__request
