from typing import Optional, Dict, List
from ..dao.subject_dao import SubjectDAO
from ..models import Subject

class SubjectService:
    """学科服务类"""
    
    def __init__(self):
        self.subject_dao = SubjectDAO()
    
    def get_subject_hierarchy(self, subject_id: int) -> Optional[Dict]:
        """获取学科层级信息"""
        subject = self.subject_dao.find_by_subject_id(subject_id)
        if not subject:
            return None
            
        result = self._format_subject_info(subject)
        if subject.level == '二级':
            parent = self.subject_dao.find_parent_subject(subject_id)
            if parent:
                result['parent_subject'] = self._format_subject_info(parent)
        else:
            sub_subjects = self.subject_dao.find_sub_subjects(subject_id)
            result['sub_subjects'] = [
                self._format_subject_info(sub) for sub in sub_subjects
            ]
        
        return result
    
    def get_all_first_level_subjects(self) -> List[Dict]:
        """获取所有一级学科"""
        subjects = self.subject_dao.find_by_level('一级')
        return [self._format_subject_info(s) for s in subjects]
    
    def get_sub_subjects(self, parent_id: int) -> List[Dict]:
        """获取二级学科列表"""
        subjects = self.subject_dao.find_sub_subjects(parent_id)
        return [self._format_subject_info(s) for s in subjects]
    
    def _format_subject_info(self, subject: Subject) -> Dict:
        """格式化学科信息"""
        return {
            'subject_id': subject.subject_id,
            'name': subject.name,
            'level': subject.level,
            'type': subject.type,
            'description': subject.description
        } 