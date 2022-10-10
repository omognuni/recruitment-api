from django.test import TestCase
from django.contrib.auth import get_user_model

from core.models import Company


class ModelTest(TestCase):
    '''Model CRUD test'''

    def test_create_user(self):
        '''username으로 유저 생성 테스트'''
        username = 'wanted'
        password = 'testpass'
        user = get_user_model().objects.create_user(username=username, password=password)

        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))

    def test_create_superuser(self):
        '''superuser 생성 테스트'''
        username = 'wantedsuper'
        password = 'testpass'
        user = get_user_model().objects.create_superuser(username=username, password=password)

        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_superuser)

    def test_create_company_model(self):
        '''회사 생성 테스트'''
        kwargs = {
            'name' : 'Wanted',
            'country' : 'Korea',
            'city' : 'Seoul',
        }


        company = Company.objects.create(**kwargs)

        self.assertEqual(str(company), kwargs['name'])