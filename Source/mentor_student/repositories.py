from .models import Applicant
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

#获取考生信息
def get_applicant_by_id(applicant_id):
    try:
        return Applicant.objects.get(applicant_id=applicant_id)
    except ObjectDoesNotExist:
        return None

#创建考生信息
def create_applicant(data):
    try:
        applicant = Applicant(**data)
        applicant.save()
        return applicant
    except IntegrityError as e:
        print(f"Error creating applicant: {e}")
        return None  # 或者返回错误信息

#更新考生信息
def update_applicant(applicant_id, data):
    try:
        updated_count = Applicant.objects.filter(applicant_id=applicant_id).update(**data)
        return updated_count > 0  #返回 True 表示更新成功，False 表示没有更新
    except Exception as e:
        print(f"Error updating applicant: {e}")
        return False

#删除考生信息
def delete_applicant(applicant_id):
    deleted_count, _ = Applicant.objects.filter(applicant_id=applicant_id).delete()
    return deleted_count > 0

