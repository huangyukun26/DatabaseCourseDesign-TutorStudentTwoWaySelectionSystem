from django.test import TestCase
from ..dao.applicant_dao import ApplicantDAO
from ..models import Applicant

class TestApplicantDAO(TestCase):
    def setUp(self):
        self.dao = ApplicantDAO()
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
    
    def test_find_by_applicant_id(self):
        # 测试根据考生ID查找
        found = self.dao.find_by_applicant_id(self.test_applicant.applicant_id)
        self.assertIsNotNone(found)
        self.assertEqual(found.name, "测试考生")
    
    def test_find_by_id_card(self):
        # 测试根据身份证号查找
        found = self.dao.find_by_id_card("123456200001010000")
        self.assertIsNotNone(found)
        self.assertEqual(found.name, "测试考生")
    
    def test_find_by_undergraduate_school(self):
        # 测试根据学校查找
        found = self.dao.find_by_undergraduate_school("测试大学")
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].name, "测试考生")
    
    def test_find_by_major(self):
        # 测试根据专业查找
        found = self.dao.find_by_major("计算机科学")
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].name, "测试考生")
    
    def test_not_found(self):
        # 测试查找不存在的记录
        not_found = self.dao.find_by_applicant_id(99999)
        self.assertIsNone(not_found)
        
        not_found = self.dao.find_by_id_card("999999999999999999")
        self.assertIsNone(not_found) 