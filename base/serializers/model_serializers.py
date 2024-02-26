from rest_framework import serializers
from base.models import Ads, CronJob


class AdsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ads
        fields = '__all__'

    def create(self, validated_data):
        return Ads.objects.create(**validated_data)


class CronJobSerializer(serializers.ModelSerializer): # TODO serializer for job_data field
    class Meta:
        model = CronJob
        fields = '__all__'

    def create(self, validated_data):
        return CronJob.objects.create(**validated_data)

