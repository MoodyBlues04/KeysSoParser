from __future__ import annotations
from django.db import models
from base.helpers.url_helper import UrlHelper


class Ads(models.Model):
    SOCIAL_NETWORK_DOMAINS = (
        't.me',
        'www.facebook.com',
        'facebook.com',
        'myspace.com',
        'vk.com',
        'twitter.com',
        'www.twitter.com',
        'www.linkedin.com',
        'linkedin.com',
        'www.instagram.com',
        'instagram.com',
        'ru.pinterest.com',
        'pinterest.com',
        'www.reddit.com',
        'www.tiktok.com',
        'www.youtube.com',
        'ok.ru',
        'whatsapp.com',
    )

    target_word = models.CharField(max_length=255)
    url = models.TextField()
    domain = models.TextField()
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    remote_id = models.CharField(max_length=55, unique=True)
    parsed_at = models.DateTimeField()
    founded_at = models.DateTimeField()

    @classmethod
    def get_by_remote_id(cls, remote_id: str) -> Ads | None:
        return Ads.objects.filter(remote_id=remote_id).first()

    @classmethod
    def get_by_id(cls, id: int) -> Ads | None:
        return Ads.objects.filter(id=id).first()

    @classmethod
    def is_url_to_save(cls, url: str) -> bool:
        url_helper = UrlHelper(url)
        domain = url_helper.get_domain()
        clear_url = url_helper.remove_query_params()

        return (domain in Ads.SOCIAL_NETWORK_DOMAINS and Ads.objects.filter(url=clear_url).first() is None
                or Ads.objects.filter(domain=domain).first() is None)

    @classmethod
    def query_by_parsed_at(cls, parsed_at):
        return Ads.objects \
            .filter(parsed_at__year=parsed_at.year,
                    parsed_at__month=parsed_at.month,
                    parsed_at__day=parsed_at.day)


class CronJob(models.Model):
    class JobType(models.TextChoices):
        KEYS_SO_PARSING = "1", "keys_so_parsing"

    job_type = models.CharField(max_length=55, choices=JobType, default=JobType.KEYS_SO_PARSING)
    job_data = models.JSONField(null=True)
    is_enabled = models.BooleanField(default=False)
    last_exec_time = models.DateTimeField(null=True)

    @classmethod
    def get_by_id(cls, id: int) -> CronJob | None:
        return CronJob.objects.filter(id=id).first()

    def __str__(self):
        return f"Job: {self.id}, {self.job_type}, {self.job_data}, {self.is_enabled}, {self.last_exec_time}"
