from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# 创建路由器
router = DefaultRouter()
router.register(r'applicants', views.ApplicantViewSet)
router.register(r'admission-catalogs', views.AdmissionCatalogViewSet, basename='admission-catalogs')

# API URL 配置
urlpatterns = [
    # 包含 router 生成的 URL
    path('', include(router.urls)),

    # 添加获取导师学生申请列表的路由
    path('mentor/<int:mentor_id>/students/', views.get_mentor_students, name='get_mentor_students'),
    
    # 添加处理学生申请的路由
    path('mentor/<int:mentor_id>/process-application/', views.process_student_application, name='process_student_application'),
    # 添加导师查询路由
    path('subject/mentors/<str:applicant_id>/', views.get_subject_mentors, name='get_subject_mentors'),
    
    # 添加获取考生基本信息的路由
    path('applicant/basic-info/<str:applicant_id>/', views.get_applicant_basic_info, name='get_applicant_basic_info'),
    
    # 添加录取状态路由
    path('admission/status/<str:applicant_id>/', views.get_admission_status, name='admission_status'),
    

   
]
