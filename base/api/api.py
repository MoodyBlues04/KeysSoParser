import requests
from abc import ABC
from os import getenv
from .response import RsyaAdsResponse
from .request import RsyaAdsRequest


class Api(ABC):
    def get(self, url: str, params: dict | None = None, headers: dict | None = None) -> dict:
        return requests.get(url, params=params, headers=headers).json()

    def post(self, url: str, data: dict | None = None, headers: dict | None = None) -> dict:
        return requests.post(url, data=data, headers=headers).json()


class KeysSoApi(Api):
    __BASE_URL = 'https://api.keys.so'

    def __init__(self):
        self.__api_token = getenv('KEYS_SO_API_KEY')

    def get_rsya_ads(self, request: RsyaAdsRequest) -> RsyaAdsResponse:
        url = f"{self.__BASE_URL}/report/ads/rsya"

        print(request.get_request())
        response = self.get(url, params=request.get_request(), headers=self.__get_auth_headers())
        return RsyaAdsResponse(response)

    def __get_auth_headers(self) -> dict:
        return {'X-Keyso-TOKEN': self.__api_token}
