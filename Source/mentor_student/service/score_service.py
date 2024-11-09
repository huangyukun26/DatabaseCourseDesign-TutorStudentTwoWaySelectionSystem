from typing import Optional, Dict, List
from ..dao.score_dao import ScoreDAO
from ..dao.subject_dao import SubjectDAO
from ..models import ApplicantScore

class ScoreService:
    """成绩服务类"""
    
    def __init__(self):
        self.score_dao = ScoreDAO()
        self.subject_dao = SubjectDAO()
    
    def get_applicant_scores(self, applicant_id: int) -> Optional[Dict]:
        """获取考生成绩详情"""
        scores = self.score_dao.find_by_applicant_id(applicant_id)
        if not scores:
            return None
            
        return self._format_score_detail(scores)
    
    def get_subject_ranking(self, subject_id: int, limit: int = 10) -> Dict:
        """获取学科排名情况"""
        top_scores = self.score_dao.find_top_scores(subject_id, limit)
        stats = self.score_dao.get_subject_statistics(subject_id)
        
        return {
            'rankings': [self._format_ranking(score) for score in top_scores],
            'statistics': stats
        }
    
    def calculate_total_score(self, score_id: int) -> float:
        """计算总分"""
        return self.score_dao.get_total_score(score_id)
    
    def _format_score_detail(self, score: ApplicantScore) -> Dict:
        """格式化成绩详情"""
        return {
            'applicant_name': score.applicant.name,
            'subject_name': score.subject.name if score.subject else None,
            'preliminary_score': score.preliminary_score,
            'final_score': score.final_score,
            'total_score': score.preliminary_score + score.final_score
        }
    
    def _format_ranking(self, score: ApplicantScore) -> Dict:
        """格式化排名信息"""
        return {
            'applicant_name': score.applicant.name,
            'total_score': score.preliminary_score + score.final_score,
            'preliminary_score': score.preliminary_score,
            'final_score': score.final_score
        } 