from django.test import TestCase, Client
from django.urls import reverse
from ..models import Applicant, Mentor, Subject

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        
        # 创建测试数据
        self.test_applicant = Applicant.objects.create(
            name="测试考生",
            birth_date="2000-01-01",
            id_card_number="123456200001010000",
            origin="北京",
            undergraduate_major="计算机科学",
            email="test@test.com",
            phone="12345678901",
            undergraduate_school="测试大学",
            school_type="本科"
        )
    
    def test_login(self):
        response = self.client.post('/api/login/', {
            'userId': self.test_applicant.applicant_id,
            'password': self.test_applicant.id_card_number[-8:],
            'captcha': '1234'
        }, content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        
    def test_get_applicant_basic_info(self):
        response = self.client.get(
            f'/api/applicant/basic-info/{self.test_applicant.applicant_id}/'
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['data']['name'], "测试考生") 