# serializers.py
from rest_framework import serializers
from .models import Applicant

class ApplicantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields = ['name', 'birth_date', 'id_card_number', 'origin', 'undergraduate_major', 'email', 'phone', 'undergraduate_school', 'school_type', 'resume']

