from venv import create
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from recruit.serializers import RecruitSerializer
from core.models import Company, Recruit


RECRUIT_URL = reverse('recruit:recruit-list')

def detail_url(recruit_id):
    return reverse('recruit:recruit-detail', args=[recruit_id])

def create_recruit(company, **params):
    defaults = {
        'title': 'sample title',
        'position': 'Front',
        'reward': 10000,
        'description': '원티드랩에서 프론트엔드 주니어 개발자를 채용합니다. 자격요건은..',
        'stack': 'Python'
    }
    recruit = Recruit.objects.create(company=company, **defaults)
    return recruit

class PublicAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.company = Company.objects.create(name='Wanted', country='Korea', city='Seoul')

    def test_retrieve_recruit(self):
        '''채용 공고 목록 get 테스트'''
        create_recruit(company=self.company)
        create_recruit(company=self.company)

        res = self.client.get(RECRUIT_URL)

        recruits = Recruit.objects.all()
        serializer = RecruitSerializer(recruits, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_recruit(self):
        '''채용 공고 생성 테스트'''
        payload = {
            'title': 'sample title',
            'position': 'Backend',
            'reward': 100000,
            'company': self.company.id,
            'stack': 'Python'
        }
        res = self.client.post(RECRUIT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        
        recruit = Recruit.objects.get(id=res.data['id'])

        self.assertEqual(str(recruit), payload['title'])

    def test_update_recruit(self):
        '''채용 공고 업데이트 테스트'''
        recruit = create_recruit(company=self.company)
        payload ={
            'reward': 50000,
            'description': '원티드랩에서 백엔드 주니어 개발자를 채용합니다. 자격요건은..',
            'stack': 'Django'
        }

        url = detail_url(recruit.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
        recruit.refresh_from_db()

        self.assertEqual(recruit.description, payload['description'])
        # for k,v in payload.items():
        #     self.assertEqual(getattr(recruit, k), v)

    def test_full_update_recruit(self):
        '''채용 공고 전체 업데이트 테스트'''
        recruit = create_recruit(company=self.company)
        company = Company.objects.create(name='kakao', country='Korea', city='Seoul')

        payload = {
            'title': 'sample title2',
            'position': 'Back',
            'reward': 50000,
            'description': '원티드랩에서 백엔드 주니어 개발자를 채용합니다. 자격요건은..',
            'company': company.id,
            'stack': 'Python'
        }

        url = detail_url(recruit.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recruit.refresh_from_db()
        
        for k,v in payload.items():
            if k == 'company':
                self.assertEqual(recruit.company.id, v)
            else:
                self.assertEqual(getattr(recruit, k), v)

    def test_delete_recruit(self):
        '''채용 공고 삭제 테스트'''
        recruit = create_recruit(company=self.company)
        
        url = detail_url(recruit.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Recruit.objects.filter(id=recruit.id).exists())

    def test_detail_recruit(self):
        '''채용 공고 상세 페이지 테스트'''
        recruit = create_recruit(company=self.company)
        
        for i in range(3):
            create_recruit(company=self.company)

        url = detail_url(recruit.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(3, len(res.data['related_ad']))