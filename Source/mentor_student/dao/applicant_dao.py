from typing import Optional, List
from .base_dao import BaseDAO
from ..models import Applicant, ApplicantScore

class ApplicantDAO(BaseDAO[Applicant]):
    def __init__(self):
        super().__init__(Applicant)
    
    def find_by_applicant_id(self, applicant_id: int) -> Optional[Applicant]:
        """根据考生ID查找考生"""
        try:
            return self.model_class.objects.get(applicant_id=applicant_id)
        except self.model_class.DoesNotExist:
            return None
    
    def find_by_id_card(self, id_card: str) -> Optional[Applicant]:
        """根据身份证号查找考生"""
        try:
            return self.model_class.objects.get(id_card_number=id_card)
        except self.model_class.DoesNotExist:
            return None
            
    def find_by_undergraduate_school(self, school: str) -> List[Applicant]:
        """根据本科学校查找考生"""
        return list(self.model_class.objects.filter(undergraduate_school=school))
    
    def find_by_major(self, major: str) -> List[Applicant]:
        """根据专业查找考生"""
        return list(self.model_class.objects.filter(undergraduate_major=major))
