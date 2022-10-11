from rest_framework import serializers

from django.db.models import Q

from core.models import Recruit


class RecruitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recruit
        fields = ['id', 'title', 'position', 'company', 'reward', 'stack']
        read_only_fields = ['id']


class RecruitDetailSerializer(RecruitSerializer):
    related_ad = serializers.SerializerMethodField(
        method_name='get_related_ad')

    def get_related_ad(self, obj):
        recruits = Recruit.objects.filter(
            company=obj.company.id).filter(~Q(id=obj.id)).values('id')

        data = [recruit['id'] for recruit in recruits]

        return data

    class Meta(RecruitSerializer.Meta):
        fields = RecruitSerializer.Meta.fields + ['description', 'related_ad']
