from typing import Optional, List, Dict
from django.db.models import Avg, F
from .base_dao import BaseDAO
from ..models import ApplicantScore, Applicant

class ScoreDAO(BaseDAO[ApplicantScore]):
    """成绩DAO实现类"""
    
    def __init__(self):
        super().__init__(ApplicantScore)
    
    def find_by_score_id(self, score_id: int) -> Optional[ApplicantScore]:
        """根据成绩ID查找成绩"""
        try:
            return self.model_class.objects.get(score_id=score_id)
        except self.model_class.DoesNotExist:
            return None
    
    def find_by_applicant_id(self, applicant_id: int) -> Optional[ApplicantScore]:
        """根据考生ID查找成绩"""
        try:
            return self.model_class.objects.get(applicant__applicant_id=applicant_id)
        except self.model_class.DoesNotExist:
            return None
    
    def find_by_subject_id(self, subject_id: int) -> List[ApplicantScore]:
        """根据学科ID查找所有成绩"""
        return list(self.model_class.objects.filter(
            subject_id=subject_id
        ).select_related('applicant'))
    
    def get_total_score(self, score_id: int) -> float:
        """计算总分"""
        try:
            score = self.find_by_score_id(score_id)
            if score:
                return score.preliminary_score + score.final_score
            return 0.0
        except Exception:
            return 0.0
    
    def get_subject_statistics(self, subject_id: int) -> Dict:
        """获取学科成绩统计信息"""
        try:
            stats = self.model_class.objects.filter(
                subject_id=subject_id
            ).aggregate(
                avg_preliminary=Avg('preliminary_score'),
                avg_final=Avg('final_score'),
                avg_total=Avg(F('preliminary_score') + F('final_score'))
            )
            return {
                'average_preliminary': float(stats['avg_preliminary'] or 0),
                'average_final': float(stats['avg_final'] or 0),
                'average_total': float(stats['avg_total'] or 0)
            }
        except Exception:
            return {
                'average_preliminary': 0.0,
                'average_final': 0.0,
                'average_total': 0.0
            }
    
    def find_top_scores(self, subject_id: int, limit: int = 10) -> List[ApplicantScore]:
        """获取学科前N名成绩"""
        return list(self.model_class.objects.filter(
            subject_id=subject_id
        ).annotate(
            total_score=F('preliminary_score') + F('final_score')
        ).order_by('-total_score')[:limit]) 