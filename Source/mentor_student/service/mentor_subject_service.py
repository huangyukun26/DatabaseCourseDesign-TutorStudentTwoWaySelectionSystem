from typing import Dict, List, Optional
from datetime import datetime
from django.db.models import QuerySet
from ..models import Applicant, ApplicantScore, MentorSubjectDirection
from ..dao.applicant_dao import ApplicantDAO
from ..dao.score_dao import ScoreDAO

class MentorSubjectService:
    """导师学科服务类"""
    
    def __init__(self):
        self.applicant_dao = ApplicantDAO()
        self.score_dao = ScoreDAO()
    
    def get_subject_mentors(self, applicant_id: int) -> Optional[Dict]:
        """获取考生报考学科的导师信息"""
        try:
            #获取考生和成绩信息
            applicant = self.applicant_dao.find_by_applicant_id(applicant_id)
            if not applicant:
                raise ValueError("考生不存在")
                
            scores = self.score_dao.find_by_applicant_id(applicant_id)
            if not scores or not scores.subject:
                raise ValueError("未找到考生成绩或学科信息")
            
            main_subject = scores.subject
            
            #构建学科信息
            subject_data = {
                'id': main_subject.subject_id,
                'name': main_subject.name,
                'level': main_subject.level,
                'type': main_subject.type
            }
            
            #获取导师研究方向
            current_year = datetime.now().year
            mentor_directions = self._get_mentor_directions(
                main_subject.subject_id,
                current_year
            )
            
            #按研究方向分组
            direction_groups = self._group_by_direction(mentor_directions)
            
            return {
                'main_subject': subject_data,
                'has_sub_subjects': bool(direction_groups),
                'sub_subjects': list(direction_groups.values())
            }
            
        except Exception as e:
            print(f"Error in get_subject_mentors: {str(e)}")
            raise
    
    def _get_mentor_directions(self, subject_id: int, year: int) -> QuerySet:
        """获取指定学科和年份的导师方向"""
        return MentorSubjectDirection.objects.filter(
            subject_id=subject_id,
            is_active=True,
            year=year
        ).select_related('mentor')
    
    def _group_by_direction(self, mentor_directions: QuerySet) -> Dict:
        """将导师按研究方向分���"""
        direction_groups = {}
        for md in mentor_directions:
            if md.research_direction not in direction_groups:
                direction_groups[md.research_direction] = {
                    'id': len(direction_groups) + 1,
                    'name': md.research_direction,
                    'mentors': []
                }
            
            direction_groups[md.research_direction]['mentors'].append({
                'mentor_id': md.mentor.mentor_id,
                'name': md.mentor.name,
                'title': md.mentor.title,
                'research_direction': md.research_direction
            })
            
        return direction_groups 