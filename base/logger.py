from logging import getLogger


class Logger:
    @classmethod
    def error(cls, message: str, extra: dict|None = None) -> None:
        getLogger('django-with-data').error(message, extra={'data': extra})
