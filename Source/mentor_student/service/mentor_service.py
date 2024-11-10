from typing import Optional, Dict, List
from ..dao.mentor_dao import MentorDAO
from ..models import Mentor, MentorSubjectDirection, MentorApplicantPreference, MentorCatalogAssignment, ApplicantScore
from datetime import datetime
from django.db import models
import logging

logger = logging.getLogger(__name__)

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
    
    def get_mentor_admission_quota(self, mentor_id: int) -> Dict:
        try:
            mentor = self.mentor_dao.find_by_mentor_id(mentor_id)
            if not mentor:
                raise ValueError("导师不存在")
                
            # 初始化配额结构
            subject_quotas = {}
            total_quota = 0
            
            # 1. 获取并初始化所有配额
            catalog_assignments = MentorCatalogAssignment.objects.filter(
                mentor=mentor,
                has_admission_eligibility=True,
                year=datetime.now().year
            ).select_related(
                'catalog',
                'catalog__subject',
                'catalog__subject__parent_subject'
            )
            
            for assignment in catalog_assignments:
                catalog = assignment.catalog
                subject = catalog.subject
                parent_subject_id = str(
                    subject.parent_subject_id if subject.parent_subject 
                    else subject.subject_id
                )
                
                # 计算个人配额
                total_mentors = MentorCatalogAssignment.objects.filter(
                    catalog=catalog,
                    has_admission_eligibility=True,
                    year=datetime.now().year
                ).count()
                quota = -(-1 * (catalog.total_quota + catalog.additional_quota) // total_mentors)
                
                if parent_subject_id not in subject_quotas:
                    subject_quotas[parent_subject_id] = {
                        'subject_name': subject.parent_subject.name if subject.parent_subject else subject.name,
                        'total_quota': 0,
                        'used_quota': 0,
                        'catalogs': [],
                        'sub_subjects': {}
                    }
                
                # 更新配额
                subject_quotas[parent_subject_id]['total_quota'] += quota
                total_quota += quota
                
                # 添加目录信息
                subject_quotas[parent_subject_id]['catalogs'].append({
                    'catalog_id': catalog.catalog_id,
                    'direction_id': catalog.direction_id,
                    'quota': quota,
                    'subject_id': subject.subject_id,
                    'subject_name': subject.name
                })
                
                # 如果是二级学科，初始化子学科配额
                if subject.parent_subject:
                    sub_subject_id = str(subject.subject_id)
                    if sub_subject_id not in subject_quotas[parent_subject_id]['sub_subjects']:
                        subject_quotas[parent_subject_id]['sub_subjects'][sub_subject_id] = {
                            'subject_name': subject.name,
                            'total_quota': quota,
                            'used_quota': 0,
                            'remaining_quota': quota
                        }
            
            # 2. 获取学生列表和计算使用量
            students = []
            total_used = 0
            
            # 获取该导师的所有目录分配
            catalog_subject_map = {
                str(assignment.catalog.subject.parent_subject_id): str(assignment.catalog.subject_id)
                for assignment in catalog_assignments
                if assignment.catalog.subject.parent_subject_id
            }
            
            preferences = MentorApplicantPreference.objects.filter(
                mentor=mentor
            ).select_related('applicant')
            
            for pref in preferences:
                try:
                    score = ApplicantScore.objects.select_related(
                        'subject',
                        'subject__parent_subject'
                    ).get(applicant=pref.applicant)
                    
                    # 获取实际报考的学科
                    actual_subject = score.subject
                    parent_subject_id = str(
                        actual_subject.parent_subject_id if actual_subject.parent_subject 
                        else actual_subject.subject_id
                    )
                    
                    # 如果是一级学科，尝试找到对应的二级学科
                    if parent_subject_id in catalog_subject_map:
                        sub_subject_id = catalog_subject_map[parent_subject_id]
                        try:
                            sub_subject = actual_subject.sub_subjects.get(subject_id=sub_subject_id)
                            actual_subject = sub_subject
                        except Exception:
                            pass
                    
                    # 如果是Accepted状态，更新使用量
                    if pref.status == 'Accepted':
                        if parent_subject_id in subject_quotas:
                            # 更新一级学科使用量
                            subject_quotas[parent_subject_id]['used_quota'] += 1
                            total_used += 1
                            
                            # 如果是二级学科，更新二级学科使用量
                            if actual_subject.parent_subject:
                                sub_subject_id = str(actual_subject.subject_id)
                                if sub_subject_id in subject_quotas[parent_subject_id]['sub_subjects']:
                                    subject_quotas[parent_subject_id]['sub_subjects'][sub_subject_id]['used_quota'] += 1
                
                    # 添加学生信息
                    students.append({
                        'applicant_id': pref.applicant.applicant_id,
                        'name': pref.applicant.name,
                        'undergraduate_school': pref.applicant.undergraduate_school,
                        'undergraduate_major': pref.applicant.undergraduate_major,
                        'preference_rank': pref.preference_rank,
                        'status': pref.status,
                        'subject_id': actual_subject.subject_id,
                        'subject_name': actual_subject.name,
                        'parent_subject_id': parent_subject_id,
                        'parent_subject_name': actual_subject.parent_subject.name if actual_subject.parent_subject else actual_subject.name,
                        'scores': {
                            'preliminary_score': score.preliminary_score,
                            'final_score': score.final_score,
                            'total_score': score.preliminary_score + score.final_score
                        }
                    })
                    
                except ApplicantScore.DoesNotExist:
                    continue
            
            # 3. 更新所有剩余配额
            for quota in subject_quotas.values():
                quota['remaining_quota'] = quota['total_quota'] - quota['used_quota']
                for sub_quota in quota['sub_subjects'].values():
                    sub_quota['remaining_quota'] = sub_quota['total_quota'] - sub_quota['used_quota']
            
            return {
                'overall': {
                    'total_quota': total_quota,
                    'used_quota': total_used,
                    'remaining_quota': total_quota - total_used
                },
                'by_subject': subject_quotas
            }
                    
        except Exception as e:
            logger.error(f"Error getting mentor admission quota: {str(e)}", exc_info=True)
            raise
    
    def process_student_application(self, mentor_id: int, applicant_id: int, action: str, remarks: str = '') -> Dict:
        """处理学生申请（考虑一级和二级学科限制）"""
        try:
            mentor = self.mentor_dao.find_by_mentor_id(mentor_id)
            if not mentor:
                raise ValueError("导师不存在")
                
            # 获取学生的申请记录和报考学科
            try:
                preference = MentorApplicantPreference.objects.get(
                    mentor=mentor,
                    applicant_id=applicant_id
                )
                score = ApplicantScore.objects.select_related('subject').get(applicant_id=applicant_id)
                if not score.subject:
                    raise ValueError("未找到学生的报考学科信息")
                    
            except MentorApplicantPreference.DoesNotExist:
                raise ValueError("未找到该学生的申请记录")
            except ApplicantScore.DoesNotExist:
                raise ValueError("未找到该学生的成绩和报考学科信息")
                
            # 检查申请是否已经被处理
            if preference.status in ['Accepted', 'Rejected']:
                raise ValueError("该申请已经被处理")
                
            if action == 'Accepted':
                # 获取学生报考的学科信息
                subject = score.subject
                parent_subject_id = subject.parent_subject_id if subject.parent_subject else subject.subject_id
                
                # 检查该科下的招生名额
                quota_info = self.get_mentor_admission_quota(mentor_id)
                parent_quota = quota_info['by_subject'].get(str(parent_subject_id))
                
                if not parent_quota:
                    raise ValueError("导师在该学科下没有招生指标")
                    
                # 检查一级学科名额
                if parent_quota['remaining_quota'] <= 0:
                    raise ValueError(f"导师在{parent_quota['subject_name']}学科下的招生名额已用完")
                
                # 如果是二级学科，还需要检查二级学科名额
                if subject.parent_subject:
                    sub_quota = parent_quota['sub_subjects'].get(str(subject.subject_id))
                    if sub_quota and sub_quota['remaining_quota'] <= 0:
                        raise ValueError(f"导师在{sub_quota['subject_name']}方向下的招生名额已用完")
                        
            # 更新申请状态
            preference.status = action
            preference.remarks = remarks
            preference.save()
            
            # 更新返回结构
            quota_result = self.get_mentor_admission_quota(mentor_id)
            return {
                'status': 'success',
                'message': '处理成功',
                'updated_quota': quota_result['quota_info']
            }
            
        except Exception as e:
            print(f"Error in process_student_application: {str(e)}")
            raise
    
    def get_mentor_students(self, mentor_id):
        """获取导师的学生申请列表"""
        try:
            applications = MentorApplicantPreference.objects.filter(
                mentor_id=mentor_id
            ).select_related(
                'applicant',
                'mentor'
            )

            students = []
            for app in applications:
                scores = ApplicantScore.objects.filter(applicant=app.applicant).first()
                subject = scores.subject if scores else None
                
                # 计算总分
                total_score = None
                if scores and scores.preliminary_score is not None and scores.final_score is not None:
                    total_score = scores.preliminary_score + scores.final_score
                
                # 修改这里的学科ID处理逻辑
                subject_id = subject.subject_id if subject else None
                parent_subject_id = str(subject_id)  # 转换为字符串
                
                student_info = {
                    'applicant_id': app.applicant.applicant_id,
                    'name': app.applicant.name,
                    'undergraduate_school': app.applicant.undergraduate_school,
                    'undergraduate_major': app.applicant.undergraduate_major,
                    'subject_id': subject_id,
                    'subject_name': subject.name if subject else None,
                    'parent_subject_id': parent_subject_id,  # 使用字符串类型
                    'parent_subject_name': subject.name if subject else None,
                    'preference_rank': app.preference_rank,
                    'status': app.status,
                    'scores': {
                        'preliminary_score': scores.preliminary_score if scores else None,
                        'final_score': scores.final_score if scores else None,
                        'total_score': total_score
                    } if scores else None
                }
                students.append(student_info)
                
            return students
            
        except Exception as e:
            logger.error(f"Error getting mentor students: {str(e)}", exc_info=True)
            raise