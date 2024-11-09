from django.test import TestCase
from ..service.score_service import ScoreService
from ..models import Applicant, Subject, ApplicantScore

class TestScoreService(TestCase):
    def setUp(self):
        self.service = ScoreService()
        
        # 创建测试数据
        self.test_subject = Subject.objects.create(
            name="计算机科学",
            level="一级",
            type="工学"
        )
        
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
        
        self.test_score = ApplicantScore.objects.create(
            applicant=self.test_applicant,
            subject=self.test_subject,
            preliminary_score=85.0,
            final_score=88.0
        )
    
    def test_get_applicant_scores(self):
        result = self.service.get_applicant_scores(
            self.test_applicant.applicant_id
        )
        
        self.assertIsNotNone(result)
        self.assertEqual(result['applicant_name'], "测试考生")
        self.assertEqual(result['preliminary_score'], 85.0)
        self.assertEqual(result['final_score'], 88.0)
        self.assertEqual(result['total_score'], 173.0) 