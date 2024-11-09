from django.test import TestCase
from ..service.subject_service import SubjectService
from ..models import Subject

class TestSubjectService(TestCase):
    def setUp(self):
        self.service = SubjectService()
        
        # 创建测试数据
        self.parent_subject = Subject.objects.create(
            name="计算机科学与技术",
            level="一级",
            type="工学"
        )
        
        self.sub_subject = Subject.objects.create(
            name="软件工程",
            level="二级",
            type="工学",
            parent_subject=self.parent_subject
        )
    
    def test_get_subject_hierarchy(self):
        # 测试一级学科
        result = self.service.get_subject_hierarchy(
            self.parent_subject.subject_id
        )
        self.assertIsNotNone(result)
        self.assertEqual(result['name'], "计算机科学与技术")
        self.assertEqual(len(result['sub_subjects']), 1)
        
        # 测试二级学科
        result = self.service.get_subject_hierarchy(
            self.sub_subject.subject_id
        )
        self.assertIsNotNone(result)
        self.assertEqual(result['name'], "软件工程")
        self.assertEqual(
            result['parent_subject']['name'],
            "计算机科学与技术"
        ) 