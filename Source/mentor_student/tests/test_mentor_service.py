from django.test import TestCase
from django.utils import timezone
from ..models import (
    Mentor, 
    Applicant, 
    MentorApplicantPreference, 
    ApplicantScore, 
    MentorCatalogAssignment, 
    AdmissionCatalog,
    Subject
)
from ..service.mentor_service import MentorService

class MentorServiceTests(TestCase):
    def setUp(self):
        # 创建测试学科
        self.subject = Subject.objects.create(
            name="计算机科学与技术",
            level="一级",
            type="工学",
            description="计算机科学与技术学科"
        )
        
        # 创建测试导师
        self.mentor = Mentor.objects.create(
            name="测试导师",
            title="教授",
            email="test@test.com",
            phone="12345678901"
        )
        
        # 创建测试考生
        self.applicant = Applicant.objects.create(
            name="测试学生",
            birth_date=timezone.now().date(),
            id_card_number="123456789012345678",
            origin="测试地区",
            undergraduate_major="计算机",
            email="student@test.com",
            phone="12345678902",
            undergraduate_school="测试大学",
            school_type="985"
        )
        
        # 创建招生计划
        self.catalog = AdmissionCatalog.objects.create(
            subject=self.subject,  # 使用创建的学科对象
            direction_id=1,
            total_quota=2,
            year=timezone.now().year
        )
        
        # 分配招生名额
        self.assignment = MentorCatalogAssignment.objects.create(
            catalog=self.catalog,
            mentor=self.mentor,
            year=timezone.now().year,
            has_admission_eligibility=True
        )
        
        # 创建申请记录
        self.preference = MentorApplicantPreference.objects.create(
            applicant=self.applicant,
            mentor=self.mentor,
            preference_rank=1,
            status='Pending'
        )
        
        # 创建成绩记录
        self.score = ApplicantScore.objects.create(
            applicant=self.applicant,
            subject=self.subject,  # 添加学科关联
            preliminary_score=80.0,
            final_score=85.0
        )
        
        self.mentor_service = MentorService()

    def test_get_mentor_admission_quota(self):
        """测试获取导师招生名额"""
        quota_info = self.mentor_service.get_mentor_admission_quota(self.mentor.mentor_id)
        
        # 检查返回的数据结构
        self.assertEqual(quota_info['status'], 'success')
        self.assertIn('quota_info', quota_info)
        self.assertIn('overall', quota_info['quota_info'])
        self.assertEqual(quota_info['quota_info']['overall']['total_quota'], 2)
        self.assertEqual(quota_info['quota_info']['overall']['used_quota'], 0)
        self.assertEqual(quota_info['quota_info']['overall']['remaining_quota'], 2)

    def test_process_student_application_accept(self):
        """测试接受学生申请"""
        result = self.mentor_service.process_student_application(
            self.mentor.mentor_id,
            self.applicant.applicant_id,
            'Accepted',
            '接受申请'
        )
        
        self.assertEqual(result['status'], 'success')
        self.assertIn('updated_quota', result)
        self.assertEqual(result['updated_quota']['overall']['used_quota'], 1)
        self.assertEqual(result['updated_quota']['overall']['remaining_quota'], 1)
        
        # 验证申请状态已更新
        updated_preference = MentorApplicantPreference.objects.get(
            mentor=self.mentor,
            applicant=self.applicant
        )
        self.assertEqual(updated_preference.status, 'Accepted')

    def test_process_student_application_reject(self):
        """测试拒绝学生申请"""
        result = self.mentor_service.process_student_application(
            self.mentor.mentor_id,
            self.applicant.applicant_id,
            'Rejected',
            '拒绝申请'
        )
        
        self.assertEqual(result['status'], 'success')
        self.assertIn('updated_quota', result)
        self.assertEqual(result['updated_quota']['overall']['used_quota'], 0)
        
        # 验证申请状态已更新
        updated_preference = MentorApplicantPreference.objects.get(
            mentor=self.mentor,
            applicant=self.applicant
        )
        self.assertEqual(updated_preference.status, 'Rejected')

    def test_quota_limit(self):
        """测试招生名额限制"""
        # 创建第二个学生
        applicant2 = Applicant.objects.create(
            name="测试学生2",
            birth_date=timezone.now().date(),
            id_card_number="123456789012345679",
            origin="测试地区",
            undergraduate_major="计算机",
            email="student2@test.com",
            phone="12345678903",
            undergraduate_school="测试大学",
            school_type="985"
        )
        
        # 创建第二个学生的申请记录
        preference2 = MentorApplicantPreference.objects.create(
            applicant=applicant2,
            mentor=self.mentor,
            preference_rank=2,
            status='Pending'
        )
        
        # 创建第二个学生的成绩记录
        score2 = ApplicantScore.objects.create(
            applicant=applicant2,
            subject=self.subject,  # 使用相同的学科
            preliminary_score=75.0,
            final_score=80.0
        )
        
        # 创建第三个学生
        applicant3 = Applicant.objects.create(
            name="测试学生3",
            birth_date=timezone.now().date(),
            id_card_number="123456789012345680",
            origin="测试地区",
            undergraduate_major="计算机",
            email="student3@test.com",
            phone="12345678904",
            undergraduate_school="测试大学",
            school_type="985"
        )
        
        # 创建第三个学生的申请记录
        preference3 = MentorApplicantPreference.objects.create(
            applicant=applicant3,
            mentor=self.mentor,
            preference_rank=3,
            status='Pending'
        )
        
        # 创建第三个学生的成绩记录
        score3 = ApplicantScore.objects.create(
            applicant=applicant3,
            subject=self.subject,  # 使用相同的学科
            preliminary_score=70.0,
            final_score=85.0
        )
        
        # 接受第一个学生
        result1 = self.mentor_service.process_student_application(
            self.mentor.mentor_id,
            self.applicant.applicant_id,
            'Accepted',
            '接受第一个申请'
        )
        
        self.assertEqual(result1['status'], 'success')
        self.assertEqual(result1['updated_quota']['overall']['used_quota'], 1)
        self.assertEqual(result1['updated_quota']['overall']['remaining_quota'], 1)
        
        # 接受第二个学生
        result2 = self.mentor_service.process_student_application(
            self.mentor.mentor_id,
            applicant2.applicant_id,
            'Accepted',
            '接受第二个申请'
        )
        
        self.assertEqual(result2['status'], 'success')
        self.assertEqual(result2['updated_quota']['overall']['used_quota'], 2)
        self.assertEqual(result2['updated_quota']['overall']['remaining_quota'], 0)
        
        # 尝试接受第三个学生，应该抛出异常
        with self.assertRaises(ValueError) as context:
            self.mentor_service.process_student_application(
                self.mentor.mentor_id,
                applicant3.applicant_id,
                'Accepted',
                '尝试接受第三个申请'
            )
        
        self.assertEqual(str(context.exception), "导师在计算机科学与技术学科下的招生名额已用完")

    def test_process_student_application_invalid_mentor(self):
        """测试处理不存在导师的申请"""
        with self.assertRaises(ValueError) as context:
            self.mentor_service.process_student_application(
                999999,  # 不存在的导师ID
                self.applicant.applicant_id,
                'Accepted'
            )
        self.assertEqual(str(context.exception), "导师不存在")

    def test_process_student_application_invalid_applicant(self):
        """测试处理不存在学生的申请"""
        with self.assertRaises(ValueError) as context:
            self.mentor_service.process_student_application(
                self.mentor.mentor_id,
                999999,  # 不存在的学生ID
                'Accepted'
            )
        self.assertEqual(str(context.exception), "未找到该学生的申请记录")

    def test_process_student_application_already_accepted(self):
        """测试处理已接受的申请"""
        # 先接受申请
        self.mentor_service.process_student_application(
            self.mentor.mentor_id,
            self.applicant.applicant_id,
            'Accepted'
        )
        
        # 再次尝试接受
        with self.assertRaises(ValueError) as context:
            self.mentor_service.process_student_application(
                self.mentor.mentor_id,
                self.applicant.applicant_id,
                'Accepted'
            )
        self.assertEqual(str(context.exception), "该申请已经被处理")