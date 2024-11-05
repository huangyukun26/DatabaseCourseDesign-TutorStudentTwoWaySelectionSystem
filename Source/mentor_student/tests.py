import json

from django.test import TestCase
from rest_framework.test import APIClient
from .models import Applicant
from datetime import date

class ApplicantAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.applicant = Applicant.objects.create(
            name="Test Applicant",
            email="test@example.com",
            birth_date=date(1995, 1, 1),
            id_card_number="123456789012345678",
            origin="Test Origin",
            undergraduate_major="Computer Science",
            phone="1234567890",
            undergraduate_school="Test University",
            school_type="Public",
            resume="Test Resume",
        )

    def test_get_applicant_list(self):
        response = self.client.get('/api/applicants/')
        self.assertEqual(response.status_code, 200)

    def test_create_applicant(self):
        data = {
            "name": "New Applicant",
            "email": "new@example.com",
            "birth_date": "2000-01-01",
            "id_card_number": "987654321098765432",
            "origin": "New Origin",
            "undergraduate_major": "Physics",
            "phone": "0987654321",
            "undergraduate_school": "New University",
            "school_type": "Private",
            "resume": "New Resume",
        }
        response = self.client.post('/api/applicants/', data)
        self.assertEqual(response.status_code, 201)

    def test_update_applicant(self):
        data = {
            "name": "Updated Applicant",
            "email": "updated@example.com",
            "birth_date": "1995-01-01",
            "id_card_number": "123456789012345678",
            "origin": "Updated Origin",
            "undergraduate_major": "Mathematics",
            "phone": "1112223333",
            "undergraduate_school": "Updated University",
            "school_type": "Private",
            "resume": "Updated Resume",
        }
        response = self.client.put(
            f'/api/applicants/{self.applicant.applicant_id}/',
            data=json.dumps(data),  #将数据转换为 JSON 格式
            content_type="application/json"
        )
        print(response.json())  #打印返回的响应内容，查看具体的错误信息
        self.assertEqual(response.status_code, 200)

    def test_delete_applicant(self):
        response = self.client.delete(f'/api/applicants/{self.applicant.applicant_id}/')
        self.assertEqual(response.status_code, 204)



