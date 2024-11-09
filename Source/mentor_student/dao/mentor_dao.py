from typing import Optional, List
from .base_dao import BaseDAO
from ..models import Mentor, MentorSubjectDirection

class MentorDAO(BaseDAO[Mentor]):
    """导师DAO实现类"""
    
    def __init__(self):
        super().__init__(Mentor)
    
    def find_by_mentor_id(self, mentor_id: int) -> Optional[Mentor]:
        """根据导师ID查找导师"""
        try:
            return self.model_class.objects.get(mentor_id=mentor_id)
        except self.model_class.DoesNotExist:
            return None
    
    def find_by_id_card(self, id_card: str) -> Optional[Mentor]:
        """根据身份证号查找导师"""
        try:
            return self.model_class.objects.get(id_card_number=id_card)
        except self.model_class.DoesNotExist:
            return None
            
    def find_by_title(self, title: str) -> List[Mentor]:
        """根据职称查找导师"""
        return list(self.model_class.objects.filter(title=title))
    
    def find_by_research_direction(self, subject_id: int, direction: str) -> List[Mentor]:
        """根据研究方向查找导师"""
        return list(self.model_class.objects.filter(
            mentorsubjectdirection__subject_id=subject_id,
            mentorsubjectdirection__research_direction=direction,
            mentorsubjectdirection__is_active=True
        ))
    
    def get_research_directions(self, mentor_id: int) -> List[MentorSubjectDirection]:
        """获取导师的所有研究方向"""
        try:
            mentor = self.find_by_mentor_id(mentor_id)
            if not mentor:
                return []
            return list(MentorSubjectDirection.objects.filter(
                mentor=mentor,
                is_active=True
            ).select_related('subject'))
        except Exception:
            return []