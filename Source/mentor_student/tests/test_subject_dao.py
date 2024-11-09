from django.test import TestCase
from ..dao.subject_dao import SubjectDAO
from ..models import Subject

class TestSubjectDAO(TestCase):
    def setUp(self):
        self.dao = SubjectDAO()
        
        # 创建一级学科
        self.parent_subject = Subject.objects.create(
            name="计算机科学与技术",
            level="一级",
            type="工学",
            description="计算机科学与技术一级学科"
        )
        
        # 创建二级学科
        self.sub_subject1 = Subject.objects.create(
            name="软件工程",
            level="二级",
            type="工学",
            description="软件工程方向",
            parent_subject=self.parent_subject
        )
        
        self.sub_subject2 = Subject.objects.create(
            name="人工智能",
            level="二级",
            type="工学",
            description="人工智能方向",
            parent_subject=self.parent_subject
        )
    
    def test_find_by_subject_id(self):
        found = self.dao.find_by_subject_id(self.parent_subject.subject_id)
        self.assertIsNotNone(found)
        self.assertEqual(found.name, "计算机科学与技术")
    
    def test_find_by_name(self):
        found = self.dao.find_by_name("软件工程")
        self.assertIsNotNone(found)
        self.assertEqual(found.level, "二级")
    
    def test_find_by_level(self):
        first_level = self.dao.find_by_level("一级")
        self.assertEqual(len(first_level), 1)
        self.assertEqual(first_level[0].name, "计算机科学与技术")
        
        second_level = self.dao.find_by_level("二级")
        self.assertEqual(len(second_level), 2)
    
    def test_find_by_type(self):
        found = self.dao.find_by_type("工学")
        self.assertEqual(len(found), 3)  # 1个一级 + 2个二级
    
    def test_find_sub_subjects(self):
        subs = self.dao.find_sub_subjects(self.parent_subject.subject_id)
        self.assertEqual(len(subs), 2)
        self.assertIn("软件工程", [sub.name for sub in subs])
        self.assertIn("人工智能", [sub.name for sub in subs])
    
    def test_find_parent_subject(self):
        parent = self.dao.find_parent_subject(self.sub_subject1.subject_id)
        self.assertIsNotNone(parent)
        self.assertEqual(parent.name, "计算机科学与技术")
        
        # 测试一级学科的父级
        no_parent = self.dao.find_parent_subject(self.parent_subject.subject_id)
        self.assertIsNone(no_parent)
    
    def test_not_found(self):
        not_found = self.dao.find_by_subject_id(99999)
        self.assertIsNone(not_found)
        
        not_found = self.dao.find_by_name("不存在的学科")
        self.assertIsNone(not_found) 