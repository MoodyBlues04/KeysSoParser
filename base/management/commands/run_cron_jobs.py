from django.core.management.base import BaseCommand
from base.logger import Logger
from base.services.cron_job_executors import KeysSoParsingExecutor
from base.models import CronJob


class Command(BaseCommand):
    help = "Runs all cron jobs"

    def add_arguments(self, parser):
        parser.add_argument('--job_type', type=str, help="Job type. If specified, only such jobs executes")

    def handle(self, *args, **options):
        try:
            jobs = self.__get_jobs(options)
            for job in jobs:
                self.__exec_job(job)

            self.stdout.write(f'Jobs ran successfully.')

        except Exception as e:
            self.stdout.write(f"Error occured: {str(e)}")
            Logger.error('Rsya parse error', {'message': str(e)})
            raise e

    def __get_jobs(self, options: dict) -> list:
        if options.get('job_type'):
            return CronJob.objects.filter(job_type=options['job_type']).all()
        else:
            return CronJob.objects.all()

    def __exec_job(self, job: CronJob):
        if job.job_type == CronJob.JobType.KEYS_SO_PARSING:
            KeysSoParsingExecutor.execute(job)
            return
        raise Exception(f"Invalid job type: {job.job_type}")