from base.api.iterators import RsyaAdsSearchIterator
from base.serializers.api_serializers import KeysSoRsyaSerializer
from base.serializers.model_serializers import AdsSerializer
from base.models import Ads
from base.logger import Logger


class AdsService:
    @classmethod
    def save_ads(cls, iterator: RsyaAdsSearchIterator) -> list[int]:
        """ Saves not existed ads to DB and returns their IDs """

        new_ads = []
        for idx, item in enumerate(iterator):
            if idx % 100 == 0:
                print(idx)

            item['found_at'] = cls.__get_4_digit_year(item['found_at'])
            item['updated_at'] = cls.__get_4_digit_year(item['updated_at'])

            api_serializer = KeysSoRsyaSerializer(data=item)
            if not api_serializer.is_valid():
                Logger.error('Rsya invalid api data', api_serializer.errors)
                continue

            ad_url = api_serializer.validated_data['target_url']
            if not Ads.is_url_to_save(ad_url) or Ads.get_by_remote_id(api_serializer.validated_data['id']) is not None:
                continue

            ads_data = api_serializer.get_rsya_ads_data(iterator.get_request().filter.target)
            model_serializer = AdsSerializer(data=ads_data)
            if not model_serializer.is_valid():
                Logger.error('Rsya invalid model data to save', model_serializer.errors)
                print(model_serializer.errors)
                continue
            ad = model_serializer.save()
            new_ads.append(ad.id)

        return new_ads

    @classmethod
    def __get_4_digit_year(cls, date: str) -> str:
        date_parts = date.split('.')
        return f"{date_parts[0]}.{date_parts[1]}.20{date_parts[2]}"
