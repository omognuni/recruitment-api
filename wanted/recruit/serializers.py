from rest_framework import serializers

from core.models import Recruit


class RecruitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recruit
        fields = ['id', 'title','position', 'company', 'reward', 'stack']
        read_only_fields = ['id']

class RecruitDetailSerializer(RecruitSerializer):

    class Meta(RecruitSerializer.Meta):
        fields = RecruitSerializer.Meta.fields + ['description']