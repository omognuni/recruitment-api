from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.authentication import BasicAuthentication
from core.models import Recruit, Company, Apply
from recruit import serializers


class BaseRecruitAttrViewSet(viewsets.ModelViewSet):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]


class RecruitViewSet(BaseRecruitAttrViewSet):
    serializer_class = serializers.RecruitDetailSerializer
    queryset = Recruit.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.RecruitSerializer
        return self.serializer_class


class CompanyViewSet(BaseRecruitAttrViewSet):
    serializer_class = serializers.CompanySerializer
    queryset = Company.objects.all()
