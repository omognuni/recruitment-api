from rest_framework import viewsets

from core.models import Recruit
from recruit import serializers


class RecruitViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.RecruitDetailSerializer
    queryset = Recruit.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.RecruitSerializer
        return self.serializer_class