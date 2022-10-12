from django.urls import (
    path,
    include
)

from rest_framework.routers import DefaultRouter

from recruit import views

router = DefaultRouter()

router.register('recruits', views.RecruitViewSet)
router.register('companies', views.CompanyViewSet)
router.register('applies', views.ApplyViewSet)

app_name = 'recruit'

urlpatterns = [
    path('', include(router.urls)),
]
