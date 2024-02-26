from django.core.management.base import BaseCommand
from base.logger import Logger
from base.serializers.model_serializers import CronJobSerializer
from base.models import CronJob


class Command(BaseCommand):
    help = "Creates new parsing job"

    def add_arguments(self, parser):
        parser.add_argument('--job_id', type=int, help="Job id. If specified, job will be update instead of creation")
        parser.add_argument('--search', type=str, help="String to search in rsya section on keys.so")
        parser.add_argument('--sheet_id', type=str, help="Google sheet id to parse to")
        parser.add_argument('--share', type=str, help="Email or domain to share sheet to")
        parser.add_argument('--is_enabled', type=bool, help="Is job enabled after creation", nargs='?', default=True)

    def handle(self, *args, **options):
        try:
            self.__validate_options(options)

            serializer = CronJobSerializer(data=self.__get_job_data(options))
            serializer.is_valid(raise_exception=True)

            if options.get('job_id') is not None:
                job = CronJob.get_by_id(options['job_id'])
                if job is None: raise Exception("Invalid job id")
                serializer.instance = job

            job = serializer.save()

            self.stdout.write(f'Job edited successfully.\n {job}')

        except Exception as e:
            self.stdout.write(f"Error occured: {str(e)}")
            Logger.error('Update job error', {'message': str(e)})
            raise e

    def __get_job_data(self, options: dict) -> dict:
        return {
            'job_type': CronJob.JobType.KEYS_SO_PARSING,
            'job_data': {
                'search': options['search'],
                'sheet_id': options['sheet_id'],
                'share': options.get('share'),
            },
            'is_enabled': options['is_enabled']
        }

    def __validate_options(self, options: dict) -> None:
        required_options = ['search', 'sheet_id']
        for option in required_options:
            if options.get(option) is None:
                raise Exception(f'Invalid args: {option} field is required')
