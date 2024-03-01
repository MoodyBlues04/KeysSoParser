import logging

from django.core.management.base import BaseCommand
from base.logger import Logger
from base.services.keys_so_parsing_service import KeysSoParsingService


class Command(BaseCommand):
    help = "Parses keys.so website."

    def add_arguments(self, parser):
        parser.add_argument('--search', type=str, help="String to search in rsya section on keys.so. Can be separated by: ','")
        parser.add_argument('--sheet_id', type=str, help="Google sheet id to parse to")
        parser.add_argument('--share', type=str, help="Email or domain to share sheet to")

    def handle(self, *args, **options):
        self.stdout.write('parsing keys.so ...')

        self.__validate_options(options)

        for search_str in options['search'].split(','):
            try:
                if not len(search_str):
                    continue
                KeysSoParsingService.execute(
                    search_str,
                    options['sheet_id'],
                    options.get('share')
                )
            except Exception as e:
                self.stdout.write(f"Error occured: {str(e)}")
                Logger.error('Rsya parse error', {'message': str(e)})

        self.stdout.write('Parsing done successfully.')

    def __validate_options(self, options: dict) -> None:
        required_options = ['search', 'sheet_id']
        for option in required_options:
            if options.get(option) is None:
                raise Exception(f'Invalid args: {option} field is required')
