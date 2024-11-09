from typing import Dict, List, Optional
from django.db import transaction
from ..models import Applicant, Mentor, MentorApplicantPreference, ApplicantScore
from ..dao.applicant_dao import ApplicantDAO
from ..dao.mentor_dao import MentorDAO

class VolunteerService:
    """志愿服务类"""
    
    def __init__(self):
        self.applicant_dao = ApplicantDAO()
        self.mentor_dao = MentorDAO()
    
    def get_admission_status(self, applicant_id: int) -> Optional[Dict]:
        """获取考生录取状态"""
        try:
            # 获取考生信息
            applicant = self.applicant_dao.find_by_applicant_id(applicant_id)
            if not applicant:
                raise ValueError("考生不存在")
            
            # 获取考生的所有志愿信息
            preferences = MentorApplicantPreference.objects.filter(
                applicant_id=applicant_id
            ).select_related('mentor', 'applicant')
            
            # 打印调试信息
            print(f"Found preferences for applicant {applicant_id}:", preferences.count())
            
            # 获取考生成绩
            try:
                scores = ApplicantScore.objects.get(applicant_id=applicant_id)
                score_info = {
                    'preliminary_score': float(scores.preliminary_score) if scores.preliminary_score else 0.0,
                    'final_score': float(scores.final_score) if scores.final_score else 0.0,
                    'total_score': float(scores.preliminary_score + scores.final_score) if scores.preliminary_score and scores.final_score else 0.0
                }
            except ApplicantScore.DoesNotExist:
                score_info = None
            
            # 整理志愿状态信息
            preference_status = []
            for pref in preferences:
                preference_status.append({
                    'rank': pref.preference_rank,
                    'mentor_name': pref.mentor.name,
                    'mentor_title': pref.mentor.title,
                    'status': pref.status,
                    'remarks': pref.remarks or ''
                })
            
            # 按志愿优先级排序
            preference_status.sort(key=lambda x: x['rank'])
            
            # 确定整体录取状态
            overall_status = self._determine_overall_status(preferences)
            
            result = {
                'basic_info': {
                    'name': applicant.name,
                    'undergraduate_school': applicant.undergraduate_school,
                    'undergraduate_major': applicant.undergraduate_major
                },
                'preferences': preference_status,
                'scores': score_info,
                'overall_status': overall_status
            }
            
            # 打印最终结果
            print("Final admission status result:", result)
            
            return result
            
        except Exception as e:
            print(f"Error in get_admission_status: {str(e)}")
            raise
    
    def get_volunteer_status(self, applicant_id: int) -> Optional[Dict]:
        """获取考生志愿状态"""
        try:
            # 获取考生信息
            applicant = self.applicant_dao.find_by_applicant_id(applicant_id)
            if not applicant:
                raise ValueError("考生不存在")
            
            # 获取考生的所有志愿信息
            preferences = MentorApplicantPreference.objects.filter(
                applicant_id=applicant_id
            ).select_related('mentor')
            
            # 获取考生成绩
            try:
                scores = ApplicantScore.objects.get(applicant_id=applicant_id)
                score_info = {
                    'preliminary_score': float(scores.preliminary_score),
                    'final_score': float(scores.final_score),
                    'total_score': float(scores.preliminary_score + scores.final_score)
                }
            except ApplicantScore.DoesNotExist:
                score_info = None
            
            # 整理志愿信息
            volunteers = []
            for pref in preferences:
                volunteers.append({
                    'rank': pref.preference_rank,
                    'mentor_name': pref.mentor.name,
                    'mentor_title': pref.mentor.title,
                    'status': pref.status
                })
            
            # 按志愿优先级排序
            volunteers.sort(key=lambda x: x['rank'])
            
            return {
                'volunteers': volunteers,
                'scores': score_info,
                'overall_status': self._determine_overall_status(preferences)
            }
            
        except Exception as e:
            print(f"Error in get_volunteer_status: {str(e)}")
            raise
    
    @transaction.atomic
    def submit_volunteers(self, applicant_id: int, volunteers: List[Dict]) -> Dict:
        """提交志愿选择"""
        try:
            # 验证考生是否存在
            applicant = self.applicant_dao.find_by_applicant_id(applicant_id)
            if not applicant:
                raise ValueError("考生不存在")
            
            # 检查是否已提交过志愿
            if MentorApplicantPreference.objects.filter(applicant=applicant).exists():
                raise ValueError("已提交过志愿，不可修改")
            
            # 验证并创建志愿
            created_volunteers = []
            for volunteer in volunteers:
                mentor_id = volunteer.get('mentor_id')
                rank = volunteer.get('rank')
                
                # 验证导师是否存在
                mentor = self.mentor_dao.find_by_mentor_id(mentor_id)
                if not mentor:
                    raise ValueError(f"导师 {mentor_id} 不存在")
                
                # 创建志愿记录
                preference = MentorApplicantPreference.objects.create(
                    applicant=applicant,
                    mentor=mentor,
                    preference_rank=rank,
                    status='Pending'
                )
                
                created_volunteers.append({
                    'mentor_id': mentor_id,
                    'mentor_name': mentor.name,
                    'rank': rank
                })
            
            return {
                'applicant_id': applicant_id,
                'volunteers': created_volunteers
            }
            
        except Exception as e:
            print(f"Error in submit_volunteers: {str(e)}")
            raise
    
    def _determine_overall_status(self, preferences) -> str:
        """确定整体录取状态"""
        if not preferences.exists():
            return '待定'
        
        if preferences.filter(status='Accepted').exists():
            return '已录取'
        elif preferences.filter(status='Pending').exists():
            return '待定'
        elif preferences.filter(status='Rejected').count() == preferences.count():
            return '未录取'
        return '待定'