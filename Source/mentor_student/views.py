from django.http import HttpResponse
from captcha.image import ImageCaptcha
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from rest_framework.permissions import IsAuthenticated

from mentor_student.models import Applicant
import random
import string
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Applicant
from .serializers import ApplicantSerializer
from rest_framework.decorators import action
from rest_framework import status

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

    # 如果请求方法不是 POST，则返回错误响应
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

    # 自定义操作：获取考生基本信息
    @action(detail=True, methods=['get'], url_path='basic-info')
    def get_basic_info(self, request, pk=None):
        try:
            applicant = self.get_object()
            serializer = ApplicantSerializer(applicant)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Applicant.DoesNotExist:
            return Response({'error': 'Applicant not found'}, status=status.HTTP_404_NOT_FOUND)

