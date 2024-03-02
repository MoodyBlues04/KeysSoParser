from .google_sheets_service import GoogleSheetsService
from .ads_service import AdsService
from base.api.iterators import RsyaAdsSearchIterator
from base.api.api import KeysSoApi
from base.api.request import RsyaAdsRequest, FilterRequest


class KeysSoParsingService:
    @classmethod
    def execute(cls, search: str, sheet_id: str, stop_words: list = [], share: str|None = None) -> None:
        keys_so_api_iterator = cls.__get_rsya_search_iterator(search, stop_words)
        new_ads_ids = AdsService.save_ads(keys_so_api_iterator)

        print("New ads count:", len(new_ads_ids))

        google_sheets_service = GoogleSheetsService(sheet_id)
        google_sheets_service.update_ads_worksheet(new_ads_ids)
        if share is not None:
            google_sheets_service.share(share)

    @classmethod
    def __get_rsya_search_iterator(cls, search_target: str, stop_words: list) -> RsyaAdsSearchIterator:
        api = KeysSoApi()
        filter_request = FilterRequest('title', FilterRequest.LIKE, search_target)
        for stop_word in stop_words:
            if len(stop_word):
                filter_request.and_filter('title', FilterRequest.NOT_LIKE, stop_word)
        request = RsyaAdsRequest(filter=filter_request)
        return RsyaAdsSearchIterator(api, request)
