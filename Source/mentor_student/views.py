from django.db import models
from django.http import HttpResponse
from captcha.image import ImageCaptcha
from django.views.decorators.csrf import csrf_exempt
from mentor_student.models import Applicant, Mentor, MentorApplicantPreference, ApplicantScore, MentorSubjectDirection, \
    Subject
import random
import string
from .models import Applicant
from .serializers import ApplicantSerializer, SubjectSerializer
from rest_framework.decorators import action
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist
import json
from rest_framework.decorators import api_view
from .models import MentorApplicantPreference, ApplicantScore
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import AdmissionCatalog
from .serializers import AdmissionCatalogSerializer
from django_filters import rest_framework as filters


@csrf_exempt
def login(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_id = data.get("userId")
            password = data.get("password")
            captcha_input = data.get("captcha")

            #验证验证码
            if captcha_input != request.session.get('captcha', ''):
                return JsonResponse({"success": False, "error": "验证码错误"})

            #判断是否为导师登录（ID前缀为6883）
            is_mentor = str(user_id).startswith('6883')

            if is_mentor:
                try:
                    mentor = Mentor.objects.get(mentor_id=user_id)
                    if mentor.id_card_number[-8:] == password:
                        return JsonResponse({
                            "success": True,
                            "user_type": "mentor",
                            "user_id": user_id
                        })
                except Mentor.DoesNotExist:
                    return JsonResponse({"success": False, "error": "导师不存在"})
            else:
                try:
                    applicant = Applicant.objects.get(applicant_id=user_id)
                    if applicant.id_card_number[-8:] == password:
                        return JsonResponse({
                            "success": True,
                            "user_type": "student",
                            "user_id": user_id
                        })
                except Applicant.DoesNotExist:
                    return JsonResponse({"success": False, "error": "考生不存在"})

            return JsonResponse({"success": False, "error": "密码错误"})

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "无效的请求方法"})



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
@require_http_methods(["POST"])
def submit_volunteer(request):
    """
    提交志愿选择
    请求体格式：
    {
        "applicant_id": "考生ID",
        "volunteers": [
            {"mentor_id": 1, "rank": 1},
            {"mentor_id": 2, "rank": 2},
            {"mentor_id": 3, "rank": 3}
        ]
    }
    """
    try:
        data = json.loads(request.body)
        applicant_id = data.get('applicant_id')
        volunteers = data.get('volunteers', [])

        #验证考生是否存在
        try:
            applicant = Applicant.objects.get(applicant_id=applicant_id)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'error', 'message': '考生不存在'}, status=404)

        #检查是否已经提交过志愿
        existing_preferences = MentorApplicantPreference.objects.filter(applicant=applicant).exists()
        if existing_preferences:
            return JsonResponse({'status': 'error', 'message': '已提交过志愿，不可修改'}, status=400)

        #验证并创建志愿选择
        for volunteer in volunteers:
            mentor_id = volunteer.get('mentor_id')
            rank = volunteer.get('rank')

            try:
                mentor = Mentor.objects.get(mentor_id=mentor_id)
            except ObjectDoesNotExist:
                return JsonResponse({'status': 'error', 'message': f'导师 {mentor_id} 不存在'}, status=404)

            #创建志愿记录
            MentorApplicantPreference.objects.create(
                applicant=applicant,
                mentor=mentor,
                preference_rank=rank,
                status='Pending'
            )

        return JsonResponse({
            'status': 'success',
            'message': '志愿提交成功',
            'data': {
                'applicant_id': applicant_id,
                'volunteers': volunteers
            }
        })

    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': '无效的请求数据'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def get_volunteer_status(request, applicant_id):
    """
    获取考生的志愿选择状态
    URL: /api/volunteer/status/<applicant_id>
    Method: GET
    """
    try:
        #验证考生是否存在
        try:
            applicant = Applicant.objects.get(applicant_id=applicant_id)
        except Applicant.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': f'考生ID {applicant_id} 不存在'
            }, status=404)

        #获取该考生的所有志愿选择
        preferences = MentorApplicantPreference.objects.filter(
            applicant=applicant
        ).select_related('mentor').order_by('preference_rank')

        #构建返回数据
        choices = []
        for pref in preferences:
            choices.append({
                'mentor_id': pref.mentor.mentor_id,
                'mentor_name': pref.mentor.name,
                'rank': pref.preference_rank,
                'status': pref.status
            })

        return JsonResponse({
            'status': 'success',
            'data': {
                'applicant_id': applicant_id,
                'applicant_name': applicant.name,
                'choices': choices
            }
        })

    except Exception as e:
        print(f"获取志愿状态错误: {str(e)}")  #添加服务器端日志
        return JsonResponse({
            'status': 'error',
            'message': f'获取志愿状态失败: {str(e)}'
        }, status=500)
    


import logging
from datetime import datetime

logger = logging.getLogger(__name__)
@csrf_exempt
@require_http_methods(["GET"])
def get_subject_mentors(request, applicant_id):
    try:
        logger.info(f"开始获取考生 {applicant_id} 的导师信息")
        
        #获取考生报考的学科信息
        try:
            applicant = Applicant.objects.get(applicant_id=applicant_id)
            logger.info(f"找到考生: {applicant.name}")
            
            applicant_score = ApplicantScore.objects.select_related('subject').get(
                applicant=applicant
            )
            
            if not applicant_score.subject:
                raise ValueError("考生没有关联的学科信息")

            main_subject = applicant_score.subject
            logger.info(f"考生报考学科: {main_subject.name} (ID: {main_subject.subject_id})")

            #获取学科信息
            subject_data = {
                'id': main_subject.subject_id,
                'name': main_subject.name,
                'level': main_subject.level,
                'type': main_subject.type
            }

            response_data = {
                'main_subject': subject_data,
                'has_sub_subjects': False,
                'sub_subjects': [],
                'mentors': []
            }

            current_year = datetime.now().year

            #获取所有导师方向数据
            mentor_directions = MentorSubjectDirection.objects.filter(
                subject_id=main_subject.subject_id,  # 使用一级学科ID
                is_active=True,
                year=current_year
            ).select_related('mentor')

            #按研究方向分组
            direction_groups = {}
            for md in mentor_directions:
                if md.research_direction not in direction_groups:
                    direction_groups[md.research_direction] = {
                        'id': len(direction_groups) + 1,  #生成唯一ID
                        'name': md.research_direction,
                        'mentors': []
                    }
                
                direction_groups[md.research_direction]['mentors'].append({
                    'mentor_id': md.mentor.mentor_id,
                    'name': md.mentor.name,
                    'title': md.mentor.title,
                    'research_direction': md.research_direction
                })

            #如果有研究方向，将其视为二级学科
            if direction_groups:
                response_data['has_sub_subjects'] = True
                response_data['sub_subjects'] = list(direction_groups.values())
                logger.info(f"找到 {len(direction_groups)} 个研究方向")
            else:
                logger.warning("未找到任何研究方向")

            return JsonResponse({
                'status': 'success',
                'data': response_data
            })

        except Applicant.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': '考生不存在'}, status=404)
        except ApplicantScore.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': '未找到考生成绩信息'}, status=404)
        except Exception as e:
            logger.error(f"处理过程中出错: {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    except Exception as e:
        logger.error(f"获取导师信息时发生错误: {str(e)}", exc_info=True)
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

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
    """
    获取考生成绩信息
    """
    try:
        #验证考生是否存在
        applicant = Applicant.objects.get(applicant_id=applicant_id)
        
        #获取该考生的成绩
        try:
            # 使用 select_related 优化查询
            score = ApplicantScore.objects.select_related('applicant', 'subject').get(applicant=applicant)
            
            #构建成绩数据，包含学科信息
            score_data = {
                'applicant_id': applicant_id,
                'applicant_name': applicant.name,
                'preliminary_score': float(score.preliminary_score),
                'final_score': float(score.final_score),
                'total_score': float(score.preliminary_score + score.final_score),
                'undergraduate_info': {
                    'major': applicant.undergraduate_major,
                    'school': applicant.undergraduate_school,
                    'school_type': applicant.school_type
                },
                'subject_info': {
                    'name': score.subject.name,
                    'subject_id': score.subject.subject_id,
                    'type': score.subject.type,
                    'description': score.subject.description,
                    'level': score.subject.level
                } if score.subject else None
            }
            
            return JsonResponse({
                'status': 'success',
                'data': score_data
            })
            
        except ApplicantScore.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': '暂无成绩信息'
            }, status=404)
            
    except Applicant.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': '考生不存在'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)



@api_view(['GET'])
def get_admission_status(request, applicant_id):
    try:
        #获取考生的所有志愿信息
        preferences = MentorApplicantPreference.objects.filter(
            applicant_id=applicant_id
        ).select_related('mentor', 'applicant')
        
        #获取考生成绩
        try:
            scores = ApplicantScore.objects.get(applicant_id=applicant_id)
            score_info = {
                'preliminary_score': scores.preliminary_score,
                'final_score': scores.final_score,
                'total_score': scores.preliminary_score + scores.final_score
            }
        except ApplicantScore.DoesNotExist:
            score_info = None

        #整理志愿状态信息
        preference_status = []
        for pref in preferences:
            preference_status.append({
                'rank': pref.preference_rank,
                'mentor_name': pref.mentor.name,
                'mentor_title': pref.mentor.title,
                'status': pref.status,
                'remarks': pref.remarks
            })

        #按志愿优先级排序
        preference_status.sort(key=lambda x: x['rank'])

        response_data = {
            'preferences': preference_status,
            'scores': score_info,
            'overall_status': '待定'  #默认状态
        }

        #确定整体录取状态
        if preferences.filter(status='Accepted').exists():
            response_data['overall_status'] = '已录取'
        elif preferences.filter(status='Pending').exists():
            response_data['overall_status'] = '待定'
        elif preferences.filter(status='Rejected').count() == preferences.count():
            response_data['overall_status'] = '未录取'

        return Response(response_data)

    except Exception as e:
        return Response({
            'error': str(e),
            'message': '获取录取状态失败'
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
        """获取所有一级学科及其二级学科"""
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

            logger.info(f"查询到的二级学科数量: {sub_subjects.count()}")
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
                        #如果是一级学科，查找所有相关的二级学科
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
        applicant = Applicant.objects.get(applicant_id=applicant_id)

        #构建基本信息响应
        basic_info = {
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

        return JsonResponse({
            'status': 'success',
            'data': basic_info
        })

    except Applicant.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': '考生不存在'
        }, status=404)

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)