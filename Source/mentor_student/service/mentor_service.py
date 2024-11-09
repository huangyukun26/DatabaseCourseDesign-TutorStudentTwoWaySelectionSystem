from typing import Optional, Dict, List
from ..dao.mentor_dao import MentorDAO
from ..models import Mentor, MentorSubjectDirection

class MentorService:
    """导师服务类"""
    
    def __init__(self):
        self.mentor_dao = MentorDAO()
    
    def get_mentor_with_directions(self, mentor_id: int) -> Optional[Dict]:
        """获取导师信息及其研究方向"""
        mentor = self.mentor_dao.find_by_mentor_id(mentor_id)
        if not mentor:
            return None
            
        directions = self.mentor_dao.get_research_directions(mentor_id)
        
        return {
            'basic_info': self._format_basic_info(mentor),
            'research_directions': [self._format_direction(d) for d in directions]
        }
    
    def verify_mentor_login(self, mentor_id: int, password: str) -> bool:
        """验证导师登录"""
        mentor = self.mentor_dao.find_by_mentor_id(mentor_id)
        if not mentor:
            return False
        return mentor.id_card_number[-8:] == password
    
    def find_mentors_by_direction(self, subject_id: int, direction: str) -> List[Dict]:
        """根据研究方向查找导师"""
        mentors = self.mentor_dao.find_by_research_direction(subject_id, direction)
        return [self._format_basic_info(m) for m in mentors]
    
    def _format_basic_info(self, mentor: Mentor) -> Dict:
        """格式化导师基本信息"""
        return {
            'mentor_id': mentor.mentor_id,
            'name': mentor.name,
            'title': mentor.title,
            'email': mentor.email,
            'phone': mentor.phone,
            'bio': mentor.bio
        }
    
    def _format_direction(self, direction: MentorSubjectDirection) -> Dict:
        """格式化研究方向信息"""
        return {
            'subject_name': direction.subject.name,
            'research_direction': direction.research_direction,
            'year': direction.year
        } 