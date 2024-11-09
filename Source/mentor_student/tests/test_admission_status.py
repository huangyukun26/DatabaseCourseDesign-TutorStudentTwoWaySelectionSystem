from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from ..models import Applicant, Mentor, MentorApplicantPreference, ApplicantScore, Subject
from ..service.volunteer_service import VolunteerService

class TestAdmissionStatus(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.service = VolunteerService()
        
        # 创建测试学科
        self.subject = Subject.objects.create(
            name="计算机科学",
            level="一级",
            type="工学"
        )
        
        # 创建测试考生
        self.applicant = Applicant.objects.create(
            name="测试考生",
            birth_date="2000-01-01",
            id_card_number="123456200001010000",
            undergraduate_school="测试大学",
            undergraduate_major="计算机科学",
            email="test@test.com",
            phone="12345678901"
        )
        
        # 创建测试导师
        self.mentor1 = Mentor.objects.create(
            name="测试导师1",
            title="教授",
            email="mentor1@test.com",
            phone="12345678902"
        )
        
        self.mentor2 = Mentor.objects.create(
            name="测试导师2",
            title="副教授",
            email="mentor2@test.com",
            phone="12345678903"
        )
        
        # 创建测试成绩
        self.score = ApplicantScore.objects.create(
            applicant=self.applicant,
            subject=self.subject,
            preliminary_score=85.0,
            final_score=88.0
        )
        
        # 创建测试志愿
        self.preference1 = MentorApplicantPreference.objects.create(
            applicant=self.applicant,
            mentor=self.mentor1,
            preference_rank=1,
            status='Pending'
        )
        
        self.preference2 = MentorApplicantPreference.objects.create(
            applicant=self.applicant,
            mentor=self.mentor2,
            preference_rank=2,
            status='Pending'
        )

    def test_get_admission_status_service(self):
        """测试服务层获取录取状态"""
        result = self.service.get_admission_status(self.applicant.applicant_id)
        
        # 验证基本信息
        self.assertEqual(result['basic_info']['name'], "测试考生")
        self.assertEqual(result['basic_info']['undergraduate_school'], "测试大学")
        
        # 验证成绩信息
        self.assertEqual(result['scores']['preliminary_score'], 85.0)
        self.assertEqual(result['scores']['final_score'], 88.0)
        self.assertEqual(result['scores']['total_score'], 173.0)
        
        # 验证志愿信息
        self.assertEqual(len(result['preferences']), 2)
        self.assertEqual(result['preferences'][0]['mentor_name'], "测试导师1")
        self.assertEqual(result['preferences'][0]['rank'], 1)
        
        # 验证整体状态
        self.assertEqual(result['overall_status'], '待定')

    def test_get_admission_status_api(self):
        """测试API接口获取录取状态"""
        url = reverse('admission_status', args=[self.applicant.applicant_id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()['data']
        
        # 验证API返回的数据结构
        self.assertIn('basic_info', data)
        self.assertIn('preferences', data)
        self.assertIn('scores', data)
        self.assertIn('overall_status', data)

    def test_admission_status_changes(self):
        """测试不同录取状态的变化"""
        # 测试已录取状态
        self.preference1.status = 'Accepted'
        self.preference1.save()
        
        result = self.service.get_admission_status(self.applicant.applicant_id)
        self.assertEqual(result['overall_status'], '已录取')
        
        # 测试未录取状态
        self.preference1.status = 'Rejected'
        self.preference1.save()
        self.preference2.status = 'Rejected'
        self.preference2.save()
        
        result = self.service.get_admission_status(self.applicant.applicant_id)
        self.assertEqual(result['overall_status'], '未录取')

    def test_not_found(self):
        """测试不存在的考生"""
        url = reverse('admission_status', args=[99999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_no_scores(self):
        """测试没有成绩的情况"""
        # 删除成绩记录
        self.score.delete()
        
        result = self.service.get_admission_status(self.applicant.applicant_id)
        self.assertIsNone(result['scores'])

    def test_no_preferences(self):
        """测试没有志愿的情况"""
        # 删除所有志愿
        MentorApplicantPreference.objects.all().delete()
        
        result = self.service.get_admission_status(self.applicant.applicant_id)
        self.assertEqual(len(result['preferences']), 0)
        self.assertEqual(result['overall_status'], '待定')