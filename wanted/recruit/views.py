from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.authentication import BasicAuthentication
from core.models import Recruit, Company
from recruit import serializers


class RecruitViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.RecruitDetailSerializer
    queryset = Recruit.objects.all()
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.RecruitSerializer
        return self.serializer_class


class CompanyViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CompanySerializer
    queryset = Company.objects.all()
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]