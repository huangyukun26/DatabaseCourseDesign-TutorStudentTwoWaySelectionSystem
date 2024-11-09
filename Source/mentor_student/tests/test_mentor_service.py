from django.test import TestCase
from ..service.mentor_service import MentorService
from ..models import Mentor, Subject, MentorSubjectDirection

class TestMentorService(TestCase):
    def setUp(self):
        self.service = MentorService()
        
        # 创建测试数据
        self.test_mentor = Mentor.objects.create(
            name="测试导师",
            title="教授",
            id_card_number="123456195001010000",
            bio="测试简介",
            email="mentor@test.com",
            phone="12345678901"
        )
        
        self.test_subject = Subject.objects.create(
            name="计算机科学",
            level="一级",
            type="工学"
        )
        
        self.test_direction = MentorSubjectDirection.objects.create(
            mentor=self.test_mentor,
            subject=self.test_subject,
            research_direction="人工智能",
            year=2024,
            is_active=True
        )
    
    def test_get_mentor_with_directions(self):
        result = self.service.get_mentor_with_directions(
            self.test_mentor.mentor_id
        )
        
        self.assertIsNotNone(result)
        self.assertEqual(result['basic_info']['name'], "测试导师")
        self.assertEqual(len(result['research_directions']), 1)
        self.assertEqual(
            result['research_directions'][0]['research_direction'],
            "人工智能"
        ) 