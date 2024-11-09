from django.test import TestCase
from datetime import datetime
from ..service.mentor_subject_service import MentorSubjectService
from ..models import Applicant, Subject, ApplicantScore, Mentor, MentorSubjectDirection

class TestMentorSubjectService(TestCase):
    def setUp(self):
        self.service = MentorSubjectService()
        
        # 创建测试数据
        self.subject = Subject.objects.create(
            name="计算机科学",
            level="一级",
            type="工学"
        )
        
        self.applicant = Applicant.objects.create(
            name="测试考生",
            birth_date="2000-01-01",
            id_card_number="123456200001010000",
            undergraduate_school="测试大学",
            undergraduate_major="计算机"
        )
        
        self.score = ApplicantScore.objects.create(
            applicant=self.applicant,
            subject=self.subject,
            preliminary_score=85.0,
            final_score=88.0
        )
        
        self.mentor = Mentor.objects.create(
            name="测试导师",
            title="教授"
        )
        
        self.direction = MentorSubjectDirection.objects.create(
            mentor=self.mentor,
            subject=self.subject,
            research_direction="人工智能",
            year=datetime.now().year,
            is_active=True
        )
    
    def test_get_subject_mentors(self):
        result = self.service.get_subject_mentors(self.applicant.applicant_id)
        
        self.assertIsNotNone(result)
        self.assertEqual(result['main_subject']['name'], "计算机科学")
        self.assertTrue(result['has_sub_subjects'])
        self.assertEqual(len(result['sub_subjects']), 1)
        self.assertEqual(
            result['sub_subjects'][0]['mentors'][0]['name'],
            "测试导师"
        ) 