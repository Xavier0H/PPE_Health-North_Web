from rest_framework.serializers import ModelSerializer

from .models import Appointment, Document, Profile


class AppointmentSerializer(ModelSerializer):
    class Meta:
        model = Appointment
        fields = "__all__"  # ['id', 'name']


class DocumentSerializer(ModelSerializer):
    class Meta:
        model = Document
        fields = "__all__"  # ['id', 'name']


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"  # ['id', 'name']
