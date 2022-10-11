from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from recruit.serializers import CompanySerializer

from core.models import Company


COMPANY_URL = reverse('recruit:company-list')

def detail_url(company_id):
    return reverse('recruit:company-detail', args=[company_id])

def create_company(**params):
    defaults = {
        'name': 'testname',
        'country': 'Korea',
        'city': 'Seoul',
    }
    
    defaults.update(params)
    return Company.objects.create(**defaults)

class PubliAPITests(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        
    def test_retrieve_company(self):
        '''회사 리스트 get 테스트'''
        create_company()
        create_company(name='testname2')
        
        res = self.client.get(COMPANY_URL)
        companies = Company.objects.all()
        serializer = CompanySerializer(companies, many=True)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
        
    def test_create_without_auth_error(self):
        '''로그인 없이 생성 시 에러 테스트'''
        payload = {
            'name': 'Wanted',
            'country': 'Korea',
            'city': 'Seoul',
        }
        
        res = self.client.post(COMPANY_URL, payload)
        
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        
class PrivateAPITests(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass',
        )
        self.client.force_authenticate(self.user)
        
    def test_create_company(self):
        '''회사 생성 테스트'''
        payload = {
            'name': 'Wanted',
            'country': 'Korea',
            'city': 'Seoul',
        }
        
        res = self.client.post(COMPANY_URL, payload)
        
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        
        for k, v in payload.items():
            self.assertEqual(res.data[k], v)
            
    def test_partial_update_company(self):
        '''회사 부분 업데이트 테스트'''
        company = create_company()
        
        payload = {
            'name': 'Wantedlab',
        }
        
        url = detail_url(company.id)
        res = self.client.patch(url, payload)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
        company.refresh_from_db()
        
        self.assertEqual(company.name, payload['name'])
        
    def test_full_update_company(self):
        '''회사 업데이트 테스트'''
        company = create_company()
        
        payload = {
            'name': 'WantedLab',
            'country': 'South Korea',
            'city': 'Busan'
        }
        
        url = detail_url(company.id)
        res = self.client.put(url, payload)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
        company.refresh_from_db()
        
        for k,v in payload.items():
            self.assertEqual(getattr(company,k), v)
            
    def test_delete_company(self):
        '''회사 삭제 테스트'''
        company = create_company()
        
        url = detail_url(company.id)
        res = self.client.delete(url)
        
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)