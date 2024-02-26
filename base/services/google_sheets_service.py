from base.api.google_sheets_api import GoogleSheetsApi
from base.models import Ads
from datetime import datetime
from django.utils.timezone import get_current_timezone


class GoogleSheetsService:
    def __init__(self, sheet_id: str):
        self.__worksheet_title = self.__get_worksheet_name()
        self.__api = GoogleSheetsApi(sheet_id, self.__worksheet_title)

    def update_ads_worksheet(self, new_ads_ids: list[int]) -> None:
        rows = self.__get_social_network_ads(new_ads_ids)
        rows += self.__get_ads_by_domain(new_ads_ids)
        self.__set_headers()
        self.__add_rows_to_worksheet(self.__worksheet_title, rows)
    
    def __get_worksheet_name(self) -> str:
        return datetime.today().strftime('%Y-%m-%d')

    def __get_social_network_ads(self, new_ads_ids: list) -> list:
        social_network_ads = Ads.query_by_parsed_at(datetime.now(tz=get_current_timezone())) \
            .filter(domain__in=Ads.SOCIAL_NETWORK_DOMAINS) \
            .filter(id__in=new_ads_ids) \
            .all()
        return [
            self.__get_ad_sheet_data(social_network_ad)
            for social_network_ad in social_network_ads
        ]

    def __get_ads_by_domain(self, new_ads_ids: list) -> list:
        ads = Ads.query_by_parsed_at(datetime.now(tz=get_current_timezone())) \
            .exclude(domain__in=Ads.SOCIAL_NETWORK_DOMAINS) \
            .filter(id__in=new_ads_ids) \
            .all()
        return [self.__get_ad_sheet_data(ad_data) for ad_data in ads]

    def __set_headers(self) -> None:
        self.__api.set_row(1, [
            'keyword',
            'domain',
            'url',
            'title',
            'description',
            'founded_at',
            'parsed_at',
        ])

    def __set_worksheet_rows(self, worksheet_title: str, rows: list):
        self.set_worksheet(worksheet_title)
        self.__api.clear_worksheet(start='A2')
        self.__api.add_rows(rows)

    def __add_rows_to_worksheet(self, worksheet_title: str, rows: list) -> None:
        self.set_worksheet(worksheet_title)

        if self.__api.get_rows_count() <= self.__api.get_first_empty_row() + len(rows):
            self.__api.increase_rows_count(len(rows))

        self.__api.add_rows(rows)

    def set_worksheet(self, title: str) -> None:
        self.__api.set_worksheet(title)

    def share(self, email_or_domain: str) -> None:
        self.__api.share(email_or_domain)

    def __get_ad_sheet_data(self, ad: Ads) -> list:
        return [
            ad.target_word,
            ad.domain,
            ad.url,
            ad.title,
            ad.description,
            ad.founded_at.strftime("%Y-%m-%d %H:%M"),
            ad.parsed_at.strftime("%Y-%m-%d %H:%M:%S"),
        ]
