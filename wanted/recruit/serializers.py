from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from django.db.models import Q

from core.models import Recruit, Company, Apply


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = ['id', 'name', 'country', 'city']
        read_only_fields = ['id']


class RecruitSerializer(serializers.ModelSerializer):
    # company_name = serializers.CharField(source='company.name')
    class Meta:
        model = Recruit
        fields = ['id', 'title', 'position', 'company', 'reward', 'stack']
        read_only_fields = ['id']


class RecruitDetailSerializer(RecruitSerializer):
    related_ad = serializers.SerializerMethodField(
        method_name='get_related_ad')

    def get_related_ad(self, obj):
        recruits = Recruit.objects.filter(
            company=obj.company).filter(~Q(id=obj.id)).values('id')

        data = [recruit['id'] for recruit in recruits]

        return data

    class Meta(RecruitSerializer.Meta):
        fields = RecruitSerializer.Meta.fields + ['description', 'related_ad']


class ApplySerializer(serializers.ModelSerializer):

    class Meta:
        model = Apply
        fields = ['recruit', 'user']
        validators = [
            UniqueTogetherValidator(
                queryset=Apply.objects.all(),
                fields=['recruit', 'user']
            )
        ]
