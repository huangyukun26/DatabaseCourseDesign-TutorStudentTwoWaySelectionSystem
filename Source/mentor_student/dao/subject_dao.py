from typing import Optional, List
from .base_dao import BaseDAO
from ..models import Subject

class SubjectDAO(BaseDAO[Subject]):
    """学科DAO实现类"""
    
    def __init__(self):
        super().__init__(Subject)
    
    def find_by_subject_id(self, subject_id: int) -> Optional[Subject]:
        """根据学科ID查找学科"""
        try:
            return self.model_class.objects.get(subject_id=subject_id)
        except self.model_class.DoesNotExist:
            return None
    
    def find_by_name(self, name: str) -> Optional[Subject]:
        """根据学科名称查找学科"""
        try:
            return self.model_class.objects.get(name=name)
        except self.model_class.DoesNotExist:
            return None
    
    def find_by_level(self, level: str) -> List[Subject]:
        """根据学科等级查找学科（一级/二级）"""
        return list(self.model_class.objects.filter(level=level))
    
    def find_by_type(self, type: str) -> List[Subject]:
        """根据学科类型查找学科"""
        return list(self.model_class.objects.filter(type=type))
    
    def find_sub_subjects(self, parent_id: int) -> List[Subject]:
        """获取指定学科的所有二级学科"""
        return list(self.model_class.objects.filter(
            parent_subject_id=parent_id,
            level='二级'
        ))
    
    def find_parent_subject(self, subject_id: int) -> Optional[Subject]:
        """获取指定学科的父级学科"""
        try:
            subject = self.find_by_subject_id(subject_id)
            if subject and subject.parent_subject:
                return subject.parent_subject
            return None
        except Subject.DoesNotExist:
            return None 