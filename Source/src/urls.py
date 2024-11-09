from django.contrib import admin
from django.urls import path, include
from mentor_student import views

# 主 URL 配置
urlpatterns = [
    path('admin/', admin.site.urls),
    
    # REST framework API 路由
    path('api/', include('mentor_student.urls')),  # 包含所有 API 路由
    
    # 独立的 API 端点
    path('api/login/', views.login, name='login'),
    path('api/generate_captcha/', views.generate_captcha, name='generate_captcha'),
    path('api/volunteer/submit/', views.submit_volunteer, name='submit_volunteer'),
    path('api/volunteer/status/<str:student_id>/', views.get_volunteer_status, name='get_volunteer_status'),
    path('api/applicant/volunteers/<str:applicant_id>/', views.get_applicant_volunteers, name='get_applicant_volunteers'),
    path('api/mentors/', views.get_mentors, name='get_mentors'),
    path('api/applicant/scores/<str:applicant_id>/', views.get_applicant_scores, name='get_applicant_scores'),
]





