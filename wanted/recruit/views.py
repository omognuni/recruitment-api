from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework import filters

from core.models import Recruit, Company, Apply
from recruit import serializers


class BaseRecruitAttrViewSet(viewsets.ModelViewSet):
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]


class RecruitViewSet(BaseRecruitAttrViewSet):
    serializer_class = serializers.RecruitDetailSerializer
    queryset = Recruit.objects.all().select_related('company_id')
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'position', 'company_id__name', 'stack']

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.RecruitSerializer
        return self.serializer_class

    # def company_name(self, obj):
    #     return obj.company_id.name


class CompanyViewSet(BaseRecruitAttrViewSet):
    serializer_class = serializers.CompanySerializer
    queryset = Company.objects.all()


class ApplyViewSet(BaseRecruitAttrViewSet):
    serializer_class = serializers.ApplySerializer
    queryset = Apply.objects.all()
