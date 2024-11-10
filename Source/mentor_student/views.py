from django.db import models
from django.http import HttpResponse
from captcha.image import ImageCaptcha
from mentor_student.models import Applicant, Mentor, MentorApplicantPreference, ApplicantScore, MentorSubjectDirection, \
    Subject
import random
import string
from .models import Applicant
from .serializers import ApplicantSerializer, SubjectSerializer
from rest_framework.decorators import action
from rest_framework.decorators import api_view
from .models import MentorApplicantPreference, ApplicantScore
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import AdmissionCatalog
from .serializers import AdmissionCatalogSerializer
from django_filters import rest_framework as filters
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .service.applicant_service import ApplicantService
from .service.mentor_service import MentorService
from .service.subject_service import SubjectService
from .service.score_service import ScoreService
from .service.mentor_subject_service import MentorSubjectService
from .service.volunteer_service import VolunteerService


@csrf_exempt
def login(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "无效的请求方法"})
        
    try:
        data = json.loads(request.body)
        user_id = data.get("userId")
        password = data.get("password")
        captcha_input = data.get("captcha")

        #验证验证码
        if captcha_input != request.session.get('captcha', ''):
            return JsonResponse({"success": False, "error": "验证码错误"})

        #判断是否为导师登录
        is_mentor = str(user_id).startswith('6883')
        
        if is_mentor:
            mentor_service = MentorService()
            if mentor_service.verify_mentor_login(user_id, password):
                return JsonResponse({
                    "success": True,
                    "user_type": "mentor",
                    "user_id": user_id
                })
            return JsonResponse({"success": False, "error": "导师不存在或密码错误"})
        else:
            applicant_service = ApplicantService()
            if applicant_service.verify_login(user_id, password):
                return JsonResponse({
                    "success": True,
                    "user_type": "student",
                    "user_id": user_id
                })
            return JsonResponse({"success": False, "error": "考生不存在或密码错误"})

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})



@csrf_exempt
def generate_captcha(request):
    #生成随机的 5 位验证码
    captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

    #创建验证码图片
    image = ImageCaptcha()
    captcha_image = image.generate(captcha_text)

    #将验证码文本存储到会话中
    request.session['captcha'] = captcha_text

    return HttpResponse(captcha_image, content_type='image/png')


class ApplicantViewSet(viewsets.ModelViewSet):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer
    #permission_classes = [IsAuthenticated]

    #自定义操作：获取考生基本信息
    @action(detail=True, methods=['get'], url_path='basic-info')
    def get_basic_info(self, request, pk=None):
        try:
            applicant = self.get_object()
            serializer = ApplicantSerializer(applicant)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Applicant.DoesNotExist:
            return Response({'error': 'Applicant not found'}, status=status.HTTP_404_NOT_FOUND)  

@csrf_exempt
@require_http_methods(["GET"])
def get_volunteer_status(request, applicant_id):
    """获取考生的志愿选择状态"""
    try:
        volunteer_service = VolunteerService()
        result = volunteer_service.get_volunteer_status(applicant_id)
        
        return JsonResponse({
            'status': 'success',
            'data': result
        })
        
    except ValueError as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=404)
        
    except Exception as e:
        logger.error(f"获取志愿状态时发生错误: {str(e)}", exc_info=True)
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def submit_volunteer(request):
    """提交志愿选择"""
    try:
        data = json.loads(request.body)
        applicant_id = data.get('applicant_id')
        volunteers = data.get('volunteers', [])
        
        volunteer_service = VolunteerService()
        result = volunteer_service.submit_volunteers(applicant_id, volunteers)
        
        return JsonResponse({
            'status': 'success',
            'message': '志愿提交成功',
            'data': result
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': '无效的请求数据'
        }, status=400)
        
    except ValueError as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)
        
    except Exception as e:
        logger.error(f"提交志愿时发生错误: {str(e)}", exc_info=True)
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)
    


import logging
from datetime import datetime

logger = logging.getLogger(__name__)
@csrf_exempt
@require_http_methods(["GET"])
def get_subject_mentors(request, applicant_id):
    """获取考生报考学科的导师信息"""
    try:
        mentor_subject_service = MentorSubjectService()
        result = mentor_subject_service.get_subject_mentors(applicant_id)
        
        return JsonResponse({
            'status': 'success',
            'data': result
        })
        
    except ValueError as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=404)
        
    except Exception as e:
        logger.error(f"获取导师信息时发生错误: {str(e)}", exc_info=True)
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def get_mentors(request):
        """获取所有导师列表"""
        try:
            mentors = Mentor.objects.all()
            #将查询结果转换为列表
            mentor_list = []
            for mentor in mentors:
                mentor_list.append({
                    'mentor_id': mentor.mentor_id,
                    'name': mentor.name,
                    'title': mentor.title,
                    'bio': mentor.bio,
                    'email': mentor.email,
                    'phone': mentor.phone,
                    'subject': {
                        'id': mentor.subject.subject_id,
                        'name': mentor.subject.name
                    } if mentor.subject else None
                })

            return JsonResponse({
                'status': 'success',
                'data': mentor_list
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)



@csrf_exempt
@require_http_methods(["GET"])
def get_applicant_volunteers(request, applicant_id):
    """获取考生已提交的志愿信息"""
    try:
        print(f"Fetching volunteers for applicant_id: {applicant_id}")
        
        #获取志愿信息及相关的导师信息
        preferences = MentorApplicantPreference.objects.filter(
            applicant_id=applicant_id
        ).select_related('mentor').order_by('preference_rank')
        
        print(f"Found preferences count: {preferences.count()}")
        
        #获取导师的研究方向信息
        current_year = datetime.now().year
        mentor_directions = {
            md.mentor_id: md.research_direction
            for md in MentorSubjectDirection.objects.filter(
                mentor__in=[pref.mentor for pref in preferences],
                year=current_year,
                is_active=True
            )
        }
        
        volunteer_data = []
        for pref in preferences:
            mentor = pref.mentor
            volunteer_data.append({
                'mentor_id': mentor.mentor_id,
                'name': mentor.name,
                'title': mentor.title,
                'research_direction': mentor_directions.get(mentor.mentor_id, '未设置'),
                'rank': pref.preference_rank
            })
        
        response_data = {
            'status': 'success',
            'data': volunteer_data
        }
        print(f"Returning response: {response_data}")
        return JsonResponse(response_data)
        
    except Exception as e:
        import traceback
        print(f"Error in get_applicant_volunteers: {str(e)}")
        print(traceback.format_exc())
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def get_applicant_scores(request, applicant_id):
    try:
        score_service = ScoreService()
        scores = score_service.get_applicant_scores(applicant_id)
        
        if not scores:
            return JsonResponse({
                'status': 'error',
                'message': '未找到成绩信息'
            }, status=404)
            
        return JsonResponse({
            'status': 'success',
            'data': scores
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)



@api_view(['GET'])
def get_admission_status(request, applicant_id):
    """获取考生录取状态"""
    try:
        volunteer_service = VolunteerService()
        result = volunteer_service.get_admission_status(applicant_id)

        print("Admission status result:", result)
        
        return Response({
            'status': 'success',
            'data': result
        })
        
    except ValueError as e:
        print(f"ValueError in get_admission_status: {str(e)}")
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as e:
        print(f"Error in get_admission_status: {str(e)}")
        logger.error(f"获取录取状态时发生错误: {str(e)}", exc_info=True)
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class AdmissionCatalogFilter(filters.FilterSet):
    year = filters.NumberFilter()
    subject = filters.CharFilter(field_name='subject__subject_id')

    class Meta:
        model = AdmissionCatalog
        fields = ['year', 'subject']





#设置日志记录器
logger = logging.getLogger(__name__)
class AdmissionCatalogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AdmissionCatalog.objects.select_related('subject').all()
    serializer_class = AdmissionCatalogSerializer

    @action(detail=False, methods=['get'], url_path='subjects', url_name='get_subjects')
    def get_subjects(self, request):
        """获取所有一学科及其二级学科"""
        try:
            first_level_subjects = Subject.objects.filter(level='一级')
            result = []

            for subject in first_level_subjects:
                #获取二级学科
                second_level_subjects = Subject.objects.filter(
                    parent_subject_id=subject.subject_id,
                    level='二级'
                )

                if second_level_subjects.exists():
                    #有二级学科的情况
                    second_level_data = [{
                        'subject_id': sub.subject_id,
                        'name': sub.name,
                        'level': sub.level
                    } for sub in second_level_subjects]
                else:
                    #没有二级学科时，使用一级学科信息
                    second_level_data = [{
                        'subject_id': subject.subject_id,
                        'name': subject.name,
                        'level': subject.level
                    }]

                result.append({
                    'subject_id': subject.subject_id,
                    'name': subject.name,
                    'level': subject.level,
                    'children': second_level_data
                })

            return Response({
                'status': 'success',
                'data': result
            })
        except Exception as e:
            logger.error(f"获取学科错误: {str(e)}")
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def get_sub_subjects(self, request):
        """根据一级学科获取二级学科"""
        try:
            parent_id = request.query_params.get('parent_id')
            logger.info(f"查询二级学科，父学科ID: {parent_id}")

            if not parent_id:
                return Response({
                    'status': 'error',
                    'message': '请提供一级学科ID'
                }, status=status.HTTP_400_BAD_REQUEST)


            sub_subjects = Subject.objects.filter(
                parent_subject_id=parent_id,
                level='二级'
            )

            logger.info(f"查到的二级学科数量: {sub_subjects.count()}")
            for subject in sub_subjects:
                logger.info(f"二级学科: ID={subject.subject_id}, 名称={subject.name}, "
                            f"父学科ID={subject.parent_subject_id}")

            serializer = SubjectSerializer(sub_subjects, many=True)
            return Response({
                'status': 'success',
                'data': serializer.data
            })
        except Exception as e:
            logger.error(f"获取二级学科错误: {str(e)}")
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request, *args, **kwargs):
        try:
            subject_id = request.query_params.get('subject_id')
            year = request.query_params.get('year')

            logger.info(f"查询参数: subject_id={subject_id}, year={year}")

            queryset = self.get_queryset()

            if subject_id:
                try:
                    subject = Subject.objects.get(subject_id=subject_id)
                    if subject.level == '一级':
                        #如果是一级科，查找所有相关的二级学科
                        sub_subjects = Subject.objects.filter(
                            models.Q(subject_id=subject_id) |
                            models.Q(parent_subject_id=subject_id)
                        ).values_list('subject_id', flat=True)
                        queryset = queryset.filter(subject__subject_id__in=sub_subjects)
                    else:
                        queryset = queryset.filter(subject__subject_id=subject_id)
                except Subject.DoesNotExist:
                    return Response([])  #如果学科不存在，返回空列表

            if year:
                queryset = queryset.filter(year=year)

            #添加关联查询以优化性能
            queryset = queryset.select_related('subject')
            
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

        except Exception as e:
            logger.error(f"Error in list view: {str(e)}")
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@require_http_methods(["GET"])
def get_applicant_basic_info(request, applicant_id):
    try:
        applicant_service = ApplicantService()
        basic_info = applicant_service.get_basic_info(applicant_id)
        
        if not basic_info:
            return JsonResponse({
                'status': 'error',
                'message': '考生不存在'
            }, status=404)
            
        return JsonResponse({
            'status': 'success',
            'data': basic_info
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def get_mentor_info(request, mentor_id):
    try:
        mentor_service = MentorService()
        mentor_info = mentor_service.get_mentor_with_directions(mentor_id)
        
        if not mentor_info:
            return JsonResponse({
                'status': 'error',
                'message': '导师不存在'
            }, status=404)
            
        return JsonResponse({
            'status': 'success',
            'data': mentor_info
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def get_subject_info(request, subject_id):
    try:
        subject_service = SubjectService()
        subject_info = subject_service.get_subject_hierarchy(subject_id)
        
        if not subject_info:
            return JsonResponse({
                'status': 'error',
                'message': '学科不存在'
            }, status=404)
            
        return JsonResponse({
            'status': 'success',
            'data': subject_info
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def get_mentor_students(request, mentor_id):
    try:
        service = MentorService()
        #获取导师的配额信息和学生列表
        quota_info = service.get_mentor_admission_quota(mentor_id)
        students = service.get_mentor_students(mentor_id)
        
        #对每个学生处理高优先级志愿信息
        for student in students:
            #获取该学生的所有更高优先级志愿
            higher_preferences = MentorApplicantPreference.objects.filter(
                applicant_id=student['applicant_id'],
                preference_rank__lt=student['preference_rank']
            ).order_by('preference_rank')
            
            #检查是否有更高优先级志愿被接受
            higher_accepted = higher_preferences.filter(status='Accepted').exists()
            
            #添加高优先级状态信息
            student['higher_preference_status'] = 'Accepted' if higher_accepted else None
        
        #构造返回结构
        result = {
            'status': 'success',
            'quota_info': quota_info,
            'students': students
        }
        
        return JsonResponse(result)
        
    except Exception as e:
        logger.error(f"Error in get_mentor_students: {str(e)}", exc_info=True)
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def process_student_application(request, mentor_id):
    """处理学生申请"""
    try:
        data = json.loads(request.body)
        applicant_id = data.get('applicant_id')
        action = data.get('action')  #'Accepted' 或 'Rejected'
        remarks = data.get('remarks', '')
        
        if not all([applicant_id, action]) or action not in ['Accepted', 'Rejected']:
            return JsonResponse({
                'status': 'error',
                'message': '无效的请求参数'
            }, status=400)
        
        mentor_service = MentorService()
        result = mentor_service.process_student_application(
            mentor_id,
            applicant_id,
            action,
            remarks
        )
        
        #如果接受了申请，自动处理其他志愿
        if action == 'Accepted':
            try:
                #获取当前志愿的优先级
                current_preference = MentorApplicantPreference.objects.get(
                    mentor_id=mentor_id,
                    applicant_id=applicant_id
                )
                
                #自动拒绝所有低优先级的志愿，并在remarks中标记原因
                MentorApplicantPreference.objects.filter(
                    applicant_id=applicant_id,
                    preference_rank__gt=current_preference.preference_rank
                ).update(
                    status='Rejected',
                    remarks='由于高志愿被录取自动拒绝'  # 使用remarks存储拒绝原因
                )
                
            except Exception as e:
                logger.error(f"Error processing other preferences: {str(e)}")
                
        return JsonResponse(result)
        
    except ValueError as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def get_mentor_accepted_students(request, mentor_id):
    """取导师已录取的学生列表"""
    try:
        mentor_service = MentorService()
        students = mentor_service.get_mentor_accepted_students(mentor_id)
        
        return JsonResponse({
            'status': 'success',
            'students': students
        })
        
    except Exception as e:
        logger.error(f"Error getting accepted students: {str(e)}", exc_info=True)
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def get_all_student_applications(request):
    """获取全院学生申请信息"""
    try:
        mentor_service = MentorService()
        applications = mentor_service.get_all_student_applications()
        
        return JsonResponse({
            'status': 'success',
            'applications': applications
        })
        
    except Exception as e:
        logger.error(f"Error getting all student applications: {str(e)}", exc_info=True)
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)