from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

#创建路由器
router = DefaultRouter()
router.register(r'applicants', views.ApplicantViewSet)
router.register(r'admission-catalogs', views.AdmissionCatalogViewSet, basename='admission-catalogs')
 

# API URL 配置
urlpatterns = [
    # 包含 router 生成的 URL
    path('', include(router.urls)),
    
    # 添加导师查询路由
    path('subject/mentors/<str:applicant_id>/', views.get_subject_mentors, name='get_subject_mentors'),
]
