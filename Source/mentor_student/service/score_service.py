from typing import Optional, Dict, List
from django.db.models import Avg, F
from ..dao.score_dao import ScoreDAO
from ..dao.subject_dao import SubjectDAO
from ..dao.applicant_dao import ApplicantDAO
from ..models import ApplicantScore

class ScoreService:
    """成绩服务类"""
    
    def __init__(self):
        self.score_dao = ScoreDAO()
        self.subject_dao = SubjectDAO()
        self.applicant_dao = ApplicantDAO()
    
    def get_applicant_scores(self, applicant_id: int) -> Optional[Dict]:
        """获取考生成绩详情"""
        try:
            scores = self.score_dao.find_by_applicant_id(applicant_id)
            if not scores:
                return None
                
            # 获取考生信息
            applicant = self.applicant_dao.find_by_applicant_id(applicant_id)
            if not applicant:
                return None
                
            # 获取学科信息
            subject = scores.subject if scores.subject else None
                
            return {
                'applicant_name': applicant.name,
                'undergraduate_info': {
                    'school': applicant.undergraduate_school,
                    'major': applicant.undergraduate_major
                },
                'subject_info': {
                    'name': subject.name if subject else '',
                    'subject_id': subject.subject_id if subject else '',
                    'type': subject.type if subject else ''
                },
                'preliminary_score': float(scores.preliminary_score) if scores.preliminary_score else 0.0,
                'final_score': float(scores.final_score) if scores.final_score else 0.0
            }
        except Exception as e:
            print(f"Error in get_applicant_scores: {str(e)}")
            return None
    
    def get_subject_ranking(self, subject_id: int, limit: int = 10) -> Dict:
        """获取学科排名情况"""
        try:
            top_scores = self.score_dao.find_top_scores(subject_id, limit)
            stats = self.score_dao.get_subject_statistics(subject_id)
            
            return {
                'rankings': [self._format_ranking(score) for score in top_scores],
                'statistics': stats
            }
        except Exception as e:
            print(f"Error in get_subject_ranking: {str(e)}")
            return {'rankings': [], 'statistics': {}}
    
    def calculate_total_score(self, score_id: int) -> float:
        """计算总分"""
        try:
            return self.score_dao.get_total_score(score_id)
        except Exception as e:
            print(f"Error in calculate_total_score: {str(e)}")
            return 0.0
    
    def _format_ranking(self, score: ApplicantScore) -> Dict:
        """格式化排名信息"""
        try:
            return {
                'applicant_name': score.applicant.name,
                'total_score': float(score.preliminary_score + score.final_score),
                'preliminary_score': float(score.preliminary_score),
                'final_score': float(score.final_score)
            }
        except Exception as e:
            print(f"Error in _format_ranking: {str(e)}")
            return {
                'applicant_name': '',
                'total_score': 0.0,
                'preliminary_score': 0.0,
                'final_score': 0.0
            } 