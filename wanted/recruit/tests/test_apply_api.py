from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from recruit.serializers import RecruitSerializer

from core.models import Company, Recruit, Apply


APPLY_URL = reverse('recruit:apply-list')


def create_company(**params):
    defaults = {
        'name': 'testname',
        'country': 'Korea',
        'city': 'Seoul',
    }

    defaults.update(params)
    return Company.objects.create(**defaults)


def create_recruit(company, **params):
    defaults = {
        'title': 'sample title',
        'position': 'Front',
        'reward': 10000,
        'description': '원티드랩에서 프론트엔드 주니어 개발자를 채용합니다. 자격요건은..',
        'stack': 'Python'
    }

    defaults.update(params)
    recruit = Recruit.objects.create(company_id=company, **defaults)
    return recruit


class PrivateAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.company = create_company()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass',
        )
        self.client.force_authenticate(self.user)

    def test_apply_recruit(self):
        '''채용 공고 지원 테스트'''
        recruit = create_recruit(company=self.company)

        payload = {
            'recruit': recruit.id,
            'user': self.user.id,
        }
        res = self.client.post(APPLY_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_duplicate_apply_prohibited(self):
        '''채용 공고 중복 지원 불가 테스트'''
        recruit = create_recruit(company=self.company)

        payload = {
            'recruit': recruit.id,
            'user': self.user.id
        }
        res1 = self.client.post(APPLY_URL, payload)
        res2 = self.client.post(APPLY_URL, payload)

        self.assertEqual(res1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res2.status_code, status.HTTP_400_BAD_REQUEST)
