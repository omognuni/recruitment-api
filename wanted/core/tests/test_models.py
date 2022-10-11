from django.test import TestCase
from django.contrib.auth import get_user_model

from core.models import Company, Recruit


def create_company():
    return Company.objects.create(name='testname', country='Korea', city='Seoul')


class ModelTest(TestCase):
    '''Model CRUD test'''

    def test_create_user(self):
        '''username으로 유저 생성 테스트'''
        username = 'wanted'
        password = 'testpass'
        user = get_user_model().objects.create_user(
            username=username, password=password)

        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))

    def test_create_superuser(self):
        '''superuser 생성 테스트'''
        username = 'wantedsuper'
        password = 'testpass'
        user = get_user_model().objects.create_superuser(
            username=username, password=password)

        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_superuser)

    def test_create_user_with_company(self):
        '''user에 company id 추가 테스트'''
        username = 'wanted'
        password = 'testpass'
        company = create_company()

        user = get_user_model().objects.create_user(
            username=username, password=password, company=company)

        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))
        self.assertEqual(user.company.id, company.id)

    def test_create_company_model(self):
        '''회사 생성 테스트'''
        kwargs = {
            'name': 'Wanted',
            'country': 'Korea',
            'city': 'Seoul',
        }

        company = Company.objects.create(**kwargs)

        self.assertEqual(str(company), kwargs['name'])

    def test_create_recruit_model(self):
        '''채용 공고 생성 테스트'''
        company = create_company()
        user = get_user_model().objects.create_user(
            username='testuser', password='testpass', company=company)

        kwargs = {
            'title': 'sample title',
            'position': 'FE',
            'reward': 50000,
            'description': '원티드랩에서 백엔드 주니어 개발자를 채용합니다. 자격요건은..',
            'stack': 'Python',
            'user': user
        }

        recruit = Recruit.objects.create(**kwargs, company=company)
        self.assertEqual(str(recruit), recruit.title)
