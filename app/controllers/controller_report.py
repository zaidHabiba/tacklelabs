from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action

from app.models.model_user import User
from app.resources.customized_response import Response
from app.resources.decorators import authentication
from app.serializers.serializer_report import Report, ReportImage
from app.serializers.serializer_report import ReportSerializer, ReportImageSerializer, ReportFetchSerializer, \
    ReportHubSerializer


class UserRegisterCore(viewsets.ViewSet):

    @action(methods="post", url_path="user/<int:user_id>/create_report/", detail=False)
    @authentication()
    def create_report(self, request, *args, **kwargs):
        print(request.data)
        request_data = request.data.copy()
        photo_size = int(request_data["photo_size"])
        photos = []
        if photo_size > 0:
            for index in range(photo_size):
                photos.append(request_data["photo" + str(index + 1)])
        if photo_size > 0:
            report_serializer = ReportSerializer(data=request_data)
            if report_serializer.is_valid():
                report_instance = report_serializer.save()
                for photo in photos:
                    report_image_serializer = ReportImageSerializer(data={"image": photo, "report": report_instance.id})
                    if report_image_serializer.is_valid():
                        report_image_serializer.save()
                response = Response(error_code=status.HTTP_200_OK)
                response.add_data("report", ReportSerializer(report_instance).data)
                return response
            else:
                response = Response(error_code=Response.ERROR_602_PARAMETERS_NOT_FOUND)
                for i in report_serializer.errors:
                    response.add_validation_errors(i, str(report_serializer.errors.get(i)[0]))
                return response

    @action(methods="post", url_path="user/<int:user_id>/fetch_reports/<int:lab>", detail=False)
    @authentication()
    def fetch_lab_saved_reports(self, request, *args, **kwargs):
        try:
            lab_id = kwargs["lab"]
            reports = Report.objects.filter(lab=lab_id)
            reports_serializer = ReportFetchSerializer(reports, many=True)
            response = Response(error_code=status.HTTP_200_OK)
            response.add_data("reports", reports_serializer.data)
            return response
        except ObjectDoesNotExist:
            response = Response(error_code=status.HTTP_200_OK)
            response.add_data("reports", [])
            return response

    @action(methods="get", url_path="user/<int:user_id>/fetch_lab_saved_reports_search/<int:lab>", detail=False)
    @authentication()
    def fetch_lab_saved_reports_search(self, request, *args, **kwargs):
        try:
            lab_id = kwargs["lab"]
            search = request.GET["search"]
            patient = User.patients.filter(first_name__contains=search) \
                      | User.patients.filter(second_name__contains=search) \
                      | User.patients.filter(middle_name__contains=search) \
                      | User.patients.filter(last_name__contains=search)
            reports = Report.objects.filter(lab=lab_id).filter(patient__in=patient)
            reports_serializer = ReportFetchSerializer(reports, many=True)
            response = Response(error_code=status.HTTP_200_OK)
            response.add_data("reports", reports_serializer.data)
            return response
        except ObjectDoesNotExist:
            response = Response(error_code=status.HTTP_200_OK)
            response.add_data("reports", [])
            return response

    @action(methods="post", url_path="user/<int:user_id>/fetch_report_images/<int:report>", detail=False)
    @authentication()
    def fetch_report_images(self, request, *args, **kwargs):
        try:
            report_id = kwargs["report"]
            report_images = ReportImage.objects.filter(report=report_id)
            report_images_serializer = ReportImageSerializer(report_images, many=True)
            response = Response(error_code=status.HTTP_200_OK)
            response.add_data("images", report_images_serializer.data)
            return response
        except ObjectDoesNotExist:
            response = Response(error_code=status.HTTP_200_OK)
            response.add_data("reports", [])
            return response

    @action(methods="post", url_path="user/<int:user_id>/send_report/", detail=False)
    @authentication()
    def send_report(self, request, *args, **kwargs):
        request_data = request.data.copy()
        receivers_list = list(request_data["receiver_list"])
        receivers_list = [item for item in receivers_list if item is not ',']
        for receiver in receivers_list:
            request_data["receiver"] = receiver
            report_hub_serializer = ReportHubSerializer(data=request_data)
            if report_hub_serializer.is_valid():
                report_hub_serializer.save()
        response = Response(error_code=status.HTTP_200_OK)
        response.set_msg("Send done")
        return response


create_report = UserRegisterCore.as_view(actions={'post': 'create_report'})
fetch_report_images = UserRegisterCore.as_view(actions={'get': 'fetch_report_images'})
fetch_lab_saved_reports = UserRegisterCore.as_view(actions={'get': 'fetch_lab_saved_reports'})
fetch_lab_saved_reports_search = UserRegisterCore.as_view(actions={'get': 'fetch_lab_saved_reports_search'})
send_report = UserRegisterCore.as_view(actions={'post': 'send_report'})
