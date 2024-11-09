from django.test import TestCase
from ..dao.score_dao import ScoreDAO
from ..models import ApplicantScore, Applicant, Subject

class TestScoreDAO(TestCase):
    def setUp(self):
        self.dao = ScoreDAO()
        
        # 创建测试学科
        self.test_subject = Subject.objects.create(
            name="计算机科学",
            level="一级",
            type="工学",
            description="计算机科学与技术"
        )
        
        # 创建测试考生
        self.test_applicant1 = Applicant.objects.create(
            name="测试考生1",
            birth_date="2000-01-01",
            id_card_number="123456200001010001",
            origin="北京",
            undergraduate_major="计算机科学",
            email="test1@test.com",
            phone="12345678901",
            undergraduate_school="测试大学",
            school_type="本科"
        )
        
        self.test_applicant2 = Applicant.objects.create(
            name="测试考生2",
            birth_date="2000-01-02",
            id_card_number="123456200001010002",
            origin="上海",
            undergraduate_major="计算机科学",
            email="test2@test.com",
            phone="12345678902",
            undergraduate_school="测试大学",
            school_type="本科"
        )
        
        # 创建测试成绩
        self.test_score1 = ApplicantScore.objects.create(
            applicant=self.test_applicant1,
            subject=self.test_subject,
            preliminary_score=85.0,
            final_score=88.0
        )
        
        self.test_score2 = ApplicantScore.objects.create(
            applicant=self.test_applicant2,
            subject=self.test_subject,
            preliminary_score=90.0,
            final_score=92.0
        )
    
    def test_find_by_score_id(self):
        found = self.dao.find_by_score_id(self.test_score1.score_id)
        self.assertIsNotNone(found)
        self.assertEqual(found.applicant.name, "测试考生1")
    
    def test_find_by_applicant_id(self):
        found = self.dao.find_by_applicant_id(self.test_applicant1.applicant_id)
        self.assertIsNotNone(found)
        self.assertEqual(found.preliminary_score, 85.0)
    
    def test_find_by_subject_id(self):
        scores = self.dao.find_by_subject_id(self.test_subject.subject_id)
        self.assertEqual(len(scores), 2)
    
    def test_get_total_score(self):
        total = self.dao.get_total_score(self.test_score1.score_id)
        self.assertEqual(total, 173.0)  # 85.0 + 88.0
    
    def test_get_subject_statistics(self):
        stats = self.dao.get_subject_statistics(self.test_subject.subject_id)
        self.assertEqual(stats['average_preliminary'], 87.5)  # (85 + 90) / 2
        self.assertEqual(stats['average_final'], 90.0)  # (88 + 92) / 2
        self.assertEqual(stats['average_total'], 177.5)  # (173 + 182) / 2
    
    def test_find_top_scores(self):
        top_scores = self.dao.find_top_scores(self.test_subject.subject_id, 2)
        self.assertEqual(len(top_scores), 2)
        self.assertEqual(top_scores[0].applicant.name, "测试考生2")  # 分数更高的考生2应该排在前面
    
    def test_not_found(self):
        not_found = self.dao.find_by_score_id(99999)
        self.assertIsNone(not_found)
        
        not_found = self.dao.find_by_applicant_id(99999)
        self.assertIsNone(not_found) 