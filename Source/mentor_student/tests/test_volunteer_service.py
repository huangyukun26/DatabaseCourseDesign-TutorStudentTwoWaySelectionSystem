from django.test import TestCase
from ..service.volunteer_service import VolunteerService
from ..models import Applicant, Mentor, MentorApplicantPreference, ApplicantScore

class TestVolunteerService(TestCase):
    def setUp(self):
        self.service = VolunteerService()
        
        # 创建测试数据
        self.applicant = Applicant.objects.create(
            name="测试考生",
            birth_date="2000-01-01",
            id_card_number="123456200001010000",
            undergraduate_school="测试大学",
            undergraduate_major="计算机"
        )
        
        self.mentor1 = Mentor.objects.create(
            name="测试导师1",
            title="教授"
        )
        
        self.mentor2 = Mentor.objects.create(
            name="测试导师2",
            title="副教授"
        )
        
        self.score = ApplicantScore.objects.create(
            applicant=self.applicant,
            preliminary_score=85.0,
            final_score=88.0
        )
    
    def test_submit_volunteers(self):
        volunteers = [
            {'mentor_id': self.mentor1.mentor_id, 'rank': 1},
            {'mentor_id': self.mentor2.mentor_id, 'rank': 2}
        ]
        
        result = self.service.submit_volunteers(
            self.applicant.applicant_id,
            volunteers
        )
        
        self.assertEqual(len(result['volunteers']), 2)
        self.assertEqual(
            result['volunteers'][0]['mentor_name'],
            "测试导师1"
        )
    
    def test_get_volunteer_status(self):
        # 创建测试志愿
        MentorApplicantPreference.objects.create(
            applicant=self.applicant,
            mentor=self.mentor1,
            preference_rank=1,
            status='Pending'
        )
        
        result = self.service.get_volunteer_status(
            self.applicant.applicant_id
        )
        
        self.assertIsNotNone(result)
        self.assertEqual(len(result['volunteers']), 1)
        self.assertEqual(result['overall_status'], '待定')
        self.assertEqual(result['scores']['total_score'], 173.0) 