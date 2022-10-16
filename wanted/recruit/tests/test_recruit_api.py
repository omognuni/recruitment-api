from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from recruit.serializers import RecruitSerializer

from core.models import Company, Recruit


RECRUIT_URL = reverse('recruit:recruit-list')


def detail_url(recruit_id):
    return reverse('recruit:recruit-detail', args=[recruit_id])


def recruit_apply_url(recruit_id):
    return reverse('recruit:recruit-apply', args=[recruit_id])

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


class PublicAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.company = Company.objects.create(
            name='Wanted', country='Korea', city='Seoul')
        self.user = get_user_model().objects.create_user(username='testuser',
                                                         password='testpass'
                                                         )

    def test_retrieve_recruit(self):
        '''채용 공고 목록 get 테스트'''
        create_recruit(company=self.company)
        create_recruit(company=self.company)

        res = self.client.get(RECRUIT_URL)

        recruits = Recruit.objects.all()
        serializer = RecruitSerializer(recruits, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_detail_recruit(self):
        '''채용 공고 상세 페이지 테스트'''

        recruit = create_recruit(company=self.company)

        for _ in range(3):
            create_recruit(company=self.company)

        url = detail_url(recruit.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(3, len(res.data['related_ad']))
        self.assertFalse(recruit.id in res.data['related_ad'])

    def test_create_without_auth_error(self):
        '''로그인 없이 생성 시 에러 테스트'''
        payload = {
            'title': 'sample title',
            'position': 'Backend',
            'reward': 100000,
            'company_id': self.company.id,
            'stack': 'Python'
        }
        res = self.client.post(RECRUIT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.company = Company.objects.create(
            name='Wanted', country='Korea', city='Seoul')

        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass',
        )

        self.client.force_authenticate(self.user)

    def test_create_recruit(self):
        '''채용 공고 생성 테스트'''
        payload = {
            'title': 'sample title',
            'position': 'Backend',
            'reward': 100000,
            'company_id': self.company.id,
            'stack': 'Python'
        }
        res = self.client.post(RECRUIT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recruit = Recruit.objects.get(id=res.data['id'])

        self.assertEqual(str(recruit), payload['title'])
        for k, v in payload.items():
            if k == 'company_id':
                self.assertEqual(getattr(recruit,k), self.company)
            else:
                self.assertEqual(getattr(recruit, k), v)

    def test_update_recruit(self):
        '''채용 공고 업데이트 테스트'''
        recruit = create_recruit(company=self.company)
        payload = {
            'reward': 50000,
            'description': '원티드랩에서 백엔드 주니어 개발자를 채용합니다. 자격요건은..',
            'stack': 'Django'
        }

        url = detail_url(recruit.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        recruit.refresh_from_db()

        self.assertEqual(recruit.description, payload['description'])
        for k, v in payload.items():
            self.assertEqual(getattr(recruit, k), v)

    def test_full_update_recruit(self):
        '''채용 공고 전체 업데이트 테스트'''
        recruit = create_recruit(company=self.company)
        company = Company.objects.create(
            name='kakao', country='Korea', city='Seoul')

        payload = {
            'title': 'sample title2',
            'position': 'Back',
            'reward': 50000,
            'description': '원티드랩에서 백엔드 주니어 개발자를 채용합니다. 자격요건은..',
            'company_id': company.id,
            'stack': 'Python'
        }

        url = detail_url(recruit.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recruit.refresh_from_db()

        for k, v in payload.items():
            if k == 'company_id':
                self.assertEqual(getattr(recruit,k), company)
            else:
                self.assertEqual(getattr(recruit, k), v)
            
    def test_update_recruit_with_invalid_company_error(self):
        '''유효하지 않은 회사로 채용 공고 업데이트 시 에러'''
        recruit = create_recruit(company=self.company)
        payload = {
            'company_id': 999,
            'description': '원티드랩에서 백엔드 주니어 개발자를 채용합니다. 자격요건은..',
            'stack': 'Django'
        }

        url = detail_url(recruit.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_delete_recruit(self):
        '''채용 공고 삭제 테스트'''
        recruit = create_recruit(company=self.company)

        url = detail_url(recruit.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Recruit.objects.filter(id=recruit.id).exists())

    def test_search_recruit_by_stack(self):
        '''채용 공고 사용기술 검색 구현'''
        create_recruit(company=self.company, stack='Django')
        create_recruit(company=self.company, stack='JS')
        create_recruit(company=self.company, stack='Python')
        params = {'search': 'Django'}
        
        res = self.client.get(RECRUIT_URL, params)
        recruit = Recruit.objects.get(stack='Django')
        serializer = RecruitSerializer(recruit)
        
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['stack'], 'Django')
        self.assertEqual(res.data[0], serializer.data)

    def test_search_recruit_by_company(self):
        '''채용 공고 회사 검색 구현'''
        create_recruit(company=self.company, stack='Django')
        kakao = create_company(name='Kakao')
        create_recruit(company=kakao, stack='JS')
        naver = create_company(name='Naver')
        create_recruit(company=naver, stack='Python')
        params = {'search': 'Wanted'}
        
        res = self.client.get(RECRUIT_URL, params)
        recruit = Recruit.objects.get(company_id=self.company)
        serializer = RecruitSerializer(recruit)
        
        # self.assertEqual(len(res.data), 1)
        # self.assertEqual(res.data[0]['company'], 'Wanted')
        self.assertEqual(res.data[0], serializer.data)
        
    
        
        