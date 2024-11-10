from typing import Optional, Dict, List
from ..dao.applicant_dao import ApplicantDAO
from ..dao.score_dao import ScoreDAO
from ..models import Applicant

class ApplicantService:
    """考生服务类"""
    
    def __init__(self):
        self.applicant_dao = ApplicantDAO()
        self.score_dao = ScoreDAO()
    
    def get_applicant_with_scores(self, applicant_id: int) -> Optional[Dict]:
        """获取考生信息及其成绩"""
        applicant = self.applicant_dao.find_by_applicant_id(applicant_id)
        if not applicant:
            return None
            
        scores = self.score_dao.find_by_applicant_id(applicant_id)
        
        return {
            'basic_info': self._format_basic_info(applicant),
            'scores': self._format_scores(scores) if scores else None
        }
    
    def verify_login(self, applicant_id: int, password: str) -> bool:
        """验证考生登录"""
        applicant = self.applicant_dao.find_by_applicant_id(applicant_id)
        if not applicant:
            return False
        #密码是身份证后8位
        return applicant.id_card_number[-8:] == password
    
    def get_basic_info(self, applicant_id: int) -> Optional[Dict]:
        """获取考生基本信息"""
        applicant = self.applicant_dao.find_by_applicant_id(applicant_id)
        if not applicant:
            return None
        return self._format_basic_info(applicant)
    
    def _format_basic_info(self, applicant: Applicant) -> Dict:
        """格式化考生基本信息"""
        return {
            'name': applicant.name,
            'birth_date': applicant.birth_date,
            'id_card_number': applicant.id_card_number,
            'origin': applicant.origin,
            'undergraduate_school': applicant.undergraduate_school,
            'undergraduate_major': applicant.undergraduate_major,
            'school_type': applicant.school_type,
            'email': applicant.email,
            'phone': applicant.phone,
            'resume': applicant.resume if hasattr(applicant, 'resume') else ''
        }
    
    def _format_scores(self, scores) -> Dict:
        """格式化考生成绩信息"""
        return {
            'preliminary_score': scores.preliminary_score,
            'final_score': scores.final_score,
            'total_score': scores.preliminary_score + scores.final_score,
            'subject': scores.subject.name if scores.subject else None
        } 