from django.test import TestCase
from ..service.applicant_service import ApplicantService
from ..models import Applicant, Subject, ApplicantScore

class TestApplicantService(TestCase):
    def setUp(self):
        self.service = ApplicantService()
        
        # 创建测试考生
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
        
        # 创建测试学科
        self.test_subject = Subject.objects.create(
            name="计算机科学",
            level="一级",
            type="工学",
            description="计算机科学与技术"
        )
        
        # 创建测试成绩
        self.test_score = ApplicantScore.objects.create(
            applicant=self.test_applicant,
            subject=self.test_subject,
            preliminary_score=85.0,
            final_score=88.0
        )
    
    def test_get_applicant_with_scores(self):
        result = self.service.get_applicant_with_scores(
            self.test_applicant.applicant_id
        )
        
        self.assertIsNotNone(result)
        self.assertEqual(result['basic_info']['name'], "测试考生")
        self.assertEqual(result['scores']['preliminary_score'], 85.0)
        self.assertEqual(result['scores']['final_score'], 88.0)
        self.assertEqual(result['scores']['total_score'], 173.0)
    
    def test_verify_login(self):
        # 测试正确密码
        self.assertTrue(
            self.service.verify_login(
                self.test_applicant.applicant_id,
                self.test_applicant.id_card_number[-8:]
            )
        )
        
        # 测试错误密码
        self.assertFalse(
            self.service.verify_login(
                self.test_applicant.applicant_id,
                "wrong_password"
            )
        )
    
    def test_get_basic_info(self):
        result = self.service.get_basic_info(self.test_applicant.applicant_id)
        
        self.assertIsNotNone(result)
        self.assertEqual(result['name'], "测试考生")
        self.assertEqual(result['undergraduate_school'], "测试大学")
        self.assertEqual(result['undergraduate_major'], "计算机科学")
    
    def test_not_found(self):
        result = self.service.get_applicant_with_scores(99999)
        self.assertIsNone(result)
        
        result = self.service.get_basic_info(99999)
        self.assertIsNone(result) 