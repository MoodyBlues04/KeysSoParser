from abc import ABC
from base.models import CronJob
from .keys_so_parsing_service import KeysSoParsingService


class CronJobExecutor(ABC):
    @classmethod
    def execute(cls, job: CronJob) -> None:
        pass


class KeysSoParsingExecutor(CronJobExecutor):
    @classmethod
    def execute(cls, job: CronJob) -> None:
        KeysSoParsingService.execute(
            job.job_data['search'],
            job.job_data['sheet_id'],
            job.job_data.get('share')
        )
