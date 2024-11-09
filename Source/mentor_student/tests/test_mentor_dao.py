from django.test import TestCase
from ..dao.mentor_dao import MentorDAO
from ..models import Mentor, Subject, MentorSubjectDirection

class TestMentorDAO(TestCase):
    def setUp(self):
        self.dao = MentorDAO()
        
        # 创建测试导师
        self.test_mentor = Mentor.objects.create(
            name="测试导师",
            title="教授",
            id_card_number="123456195001010000",
            bio="测试简介",
            email="mentor@test.com",
            phone="12345678901"
        )
        
        # 创建测试学科
        self.test_subject = Subject.objects.create(
            name="计算机科学",
            level="一级",
            type="工学",
            description="计算机科学与技术"
        )
        
        # 创建研究方向
        self.test_direction = MentorSubjectDirection.objects.create(
            mentor=self.test_mentor,
            subject=self.test_subject,
            research_direction="人工智能",
            year=2024,
            is_active=True
        )
    
    def test_find_by_mentor_id(self):
        found = self.dao.find_by_mentor_id(self.test_mentor.mentor_id)
        self.assertIsNotNone(found)
        self.assertEqual(found.name, "测试导师")
    
    def test_find_by_id_card(self):
        found = self.dao.find_by_id_card("123456195001010000")
        self.assertIsNotNone(found)
        self.assertEqual(found.name, "测试导师")
    
    def test_find_by_title(self):
        found = self.dao.find_by_title("教授")
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].name, "测试导师")
    
    def test_find_by_research_direction(self):
        found = self.dao.find_by_research_direction(
            self.test_subject.subject_id,
            "人工智能"
        )
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].name, "测试导师")
    
    def test_get_research_directions(self):
        directions = self.dao.get_research_directions(self.test_mentor.mentor_id)
        self.assertEqual(len(directions), 1)
        self.assertEqual(directions[0].research_direction, "人工智能")
        self.assertEqual(directions[0].subject.name, "计算机科学")
    
    def test_not_found(self):
        not_found = self.dao.find_by_mentor_id(99999)
        self.assertIsNone(not_found)
        
        not_found = self.dao.find_by_id_card("999999999999999999")
        self.assertIsNone(not_found) 