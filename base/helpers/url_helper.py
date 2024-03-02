from urllib.parse import urlparse


class UrlHelper:
    def __init__(self, url: str) -> None:
        self.__url = url
        self.__parsed_url = urlparse(url)

    def remove_query_params(self) -> str:
        return f"{self.__parsed_url.scheme}://{self.__parsed_url.netloc}{self.__parsed_url.path}"

    def get_domain(self) -> str:
        return self.__parsed_url.netloc
