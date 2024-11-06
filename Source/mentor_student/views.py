from django.http import HttpResponse
from captcha.image import ImageCaptcha
from django.views.decorators.csrf import csrf_exempt
from mentor_student.models import Applicant, Mentor, MentorApplicantPreference, ApplicantScore
import random
import string
from rest_framework import viewsets
from .models import Applicant
from .serializers import ApplicantSerializer
from rest_framework.decorators import action
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import MentorApplicantPreference, ApplicantScore

@csrf_exempt
def login(request):
    if request.method == "POST":
        try:
            #获取请求体中的数据
            data = json.loads(request.body)
            user_id = data.get("userId")
            password = data.get("password")
            captcha_input = data.get("captcha")
            #验证验证码
            if captcha_input != request.session.get('captcha', ''):
                return JsonResponse({"success": False, "error": "验证码错误"})

            #查找用户
            applicant = Applicant.objects.get(applicant_id=user_id)

            #验证密码是否为身份证号后 8 位
            if applicant.id_card_number[-8:] == password:
                return JsonResponse({
                    "success": True,
                    "applicant_id": user_id  # 返回 applicant_id
                })
            else:
                return JsonResponse({"success": False, "error": "密码错误"})  # 密码不匹配

        except Applicant.DoesNotExist:
            return JsonResponse({"success": False, "error": "用户不存在"})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    #如果请求方法不是 POST，则返回错误响应
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
        "mentor_choices": [
            {"mentor_id": 1, "rank": 1},
            {"mentor_id": 2, "rank": 2},
            {"mentor_id": 3, "rank": 3}
        ]
    }
    """
    try:
        data = json.loads(request.body)
        applicant_id = data.get('applicant_id')
        mentor_choices = data.get('mentor_choices', [])

        #验证考生是否存在
        try:
            applicant = Applicant.objects.get(applicant_id=applicant_id)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'error', 'message': '考生不存在'}, status=404)

        #验证并创建志愿选择
        for choice in mentor_choices:
            mentor_id = choice.get('mentor_id')
            rank = choice.get('rank')

            try:
                mentor = Mentor.objects.get(mentor_id=mentor_id)
            except ObjectDoesNotExist:
                return JsonResponse({'status': 'error', 'message': f'导师 {mentor_id} 不存在'}, status=404)

            #检查是否已存在该志愿
            preference, created = MentorApplicantPreference.objects.get_or_create(
                applicant=applicant,
                mentor=mentor,
                defaults={'preference_rank': rank, 'status': 'Pending'}
            )

            if not created:
                #更新已存在的志愿顺序
                preference.preference_rank = rank
                preference.save()

        return JsonResponse({
            'status': 'success',
            'message': '志愿提交成功',
            'data': {
                'applicant_id': applicant_id,
                'choices': mentor_choices
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
    """
    获取考生已提交的志愿信息
    """
    try:
        #验证考生是否存在
        applicant = Applicant.objects.get(applicant_id=applicant_id)
        
        #获取该考生的所有志愿选择，按志愿顺序排序
        preferences = MentorApplicantPreference.objects.filter(
            applicant=applicant
        ).select_related('mentor').order_by('preference_rank')
        
        #构建返回数据
        volunteer_data = []
        for pref in preferences:
            volunteer_data.append({
                'mentor_id': pref.mentor.mentor_id,
                'name': pref.mentor.name,
                'title': pref.mentor.title,
                'bio': pref.mentor.bio,
                'rank': pref.preference_rank,
                'status': pref.status
            })
        
        return JsonResponse({
            'status': 'success',
            'data': volunteer_data
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
            score = ApplicantScore.objects.get(applicant=applicant)
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
                }
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