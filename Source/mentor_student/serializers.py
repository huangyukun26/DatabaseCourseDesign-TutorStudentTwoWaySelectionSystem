# serializers.py
from .models import Applicant, Mentor
from rest_framework import serializers
from .models import AdmissionCatalog, Subject

class ApplicantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields = '__all__'

class MentorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mentor
        fields = '__all__'





class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['subject_id', 'name']

class AdmissionCatalogSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    
    class Meta:
        model = AdmissionCatalog
        fields = ['catalog_id', 'subject', 'subject_name', 'direction_id', 
                 'total_quota', 'additional_quota', 'year']