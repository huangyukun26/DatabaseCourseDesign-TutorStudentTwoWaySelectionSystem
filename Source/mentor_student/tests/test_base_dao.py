from django.test import TestCase
from ..models import Applicant
from ..dao.base_dao import BaseDAO

class TestBaseDAO(TestCase):
    def setUp(self):
        self.dao = BaseDAO(Applicant)
    
    def test_basic_operations(self):
        # 测试插入
        applicant = self.dao.insert(
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
        self.assertIsNotNone(applicant)
        self.assertEqual(applicant.name, "测试考生")
        
        # 测试查找
        found = self.dao.find_by_id(applicant.applicant_id)
        self.assertIsNotNone(found)
        self.assertEqual(found.name, "测试考生")
        
        # 测试更新
        updated = self.dao.update(applicant, name="新名字")
        self.assertEqual(updated.name, "新名字")
        
        # 测试删除
        self.assertTrue(self.dao.delete(applicant))
        self.assertIsNone(self.dao.find_by_id(applicant.applicant_id)) 