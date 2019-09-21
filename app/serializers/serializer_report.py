from rest_framework import serializers

from app.models.model_report import Report, ReportImage
from app.serializers.serializer_institutions import InstitutionFetchSerializer
from app.serializers.serializer_user import DoctorFetchSerializer, PatientFetchSerializer


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = "__all__"


class ReportFetchSerializer(serializers.ModelSerializer):
    lab = InstitutionFetchSerializer()
    doctor = DoctorFetchSerializer()
    patient = PatientFetchSerializer()

    class Meta:
        model = Report
        fields = "__all__"


class ReportImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportImage
        fields = "__all__"


class ReportImageFetchSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportImage
        fields = ('id', 'image')


class ReportHubSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportImage
        fields = "__all__"


class ReportHubFetchSerializer(serializers.ModelSerializer):
    report = ReportFetchSerializer()

    class Meta:
        model = ReportImage
        fields = ('id', 'report', 'sender', 'title', 'msg')
