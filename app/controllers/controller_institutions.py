from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action

from app.models.model_institutions import Institution, HospitalJoinRequest
from app.resources import values
from app.resources.customized_response import Response
from app.resources.decorators import validation_parameters, authentication, permissions
from app.serializers.serializer_institutions import InstitutionSerializer, HJIRSerializer, InstitutionFetchSerializer, \
    HJIRFetchSerializer, InstitutionFetchHansSerializer


class InstitutionCore(viewsets.ViewSet):

    @action(methods="post", url_path="user/<int:user_id>/create_hospital/", detail=False)
    @authentication()
    @permissions([values.PERMISSION_TYPE_SUPERVISOR])
    @validation_parameters(["name", "logo"])
    def create_hospital(self, request, *args, **kwargs):
        user_id = kwargs[values.USER_ID_REQUEST_URL_NAME]
        request_data = request.data.copy()
        request_data['manager'] = user_id
        request_data['type'] = values.INSTITUTION_HOSPITAL_ID
        institution_serializer = InstitutionSerializer(data=request_data)
        if institution_serializer.is_valid():
            hospital = institution_serializer.save()
            response = Response(error_code=status.HTTP_200_OK)
            response.add_data("institution", InstitutionFetchSerializer(hospital).data)
            return response
        else:
            response = Response(error_code=Response.ERROR_602_PARAMETERS_NOT_FOUND)
            for i in institution_serializer.errors:
                response.add_validation_errors(i, str(institution_serializer.errors.get(i)[0]))
            return response

    @action(methods="post", url_path="user/<int:user_id>/create_lab/", detail=False)
    @authentication()
    @permissions([values.PERMISSION_TYPE_SUPERVISOR])
    @validation_parameters(["name", "logo"])
    def create_lab(self, request, *args, **kwargs):
        user_id = kwargs[values.USER_ID_REQUEST_URL_NAME]
        request_data = request.data.copy()
        request_data['manager'] = user_id
        request_data['type'] = values.INSTITUTION_LAB_ID
        institution_serializer = InstitutionSerializer(data=request_data)
        if institution_serializer.is_valid():
            hospital = institution_serializer.save()
            response = Response(error_code=status.HTTP_200_OK)
            response.add_data("institution", InstitutionFetchSerializer(hospital).data)
            return response
        else:
            response = Response(error_code=Response.ERROR_602_PARAMETERS_NOT_FOUND)
            for i in institution_serializer.errors:
                response.add_validation_errors(i, str(institution_serializer.errors.get(i)[0]))
            return response

    @action(methods="post", url_path="user/<int:user_id>/create_software_company/", detail=False)
    @authentication()
    @permissions([values.PERMISSION_TYPE_DEVELOPER])
    @validation_parameters(["name", "logo"])
    def create_software_company(self, request, *args, **kwargs):
        user_id = kwargs[values.USER_ID_REQUEST_URL_NAME]

        request_data = request.data.copy()
        request_data['manager'] = user_id
        request_data['type'] = values.INSTITUTION_SOFTWARE_ID
        institution_serializer = InstitutionSerializer(data=request_data)
        if institution_serializer.is_valid():
            hospital = institution_serializer.save()
            response = Response(error_code=status.HTTP_200_OK)
            response.add_data("institution", InstitutionFetchSerializer(hospital).data)
            return response
        else:
            response = Response(error_code=Response.ERROR_602_PARAMETERS_NOT_FOUND)
            for i in institution_serializer.errors:
                response.add_validation_errors(i, str(institution_serializer.errors.get(i)[0]))
            return response

    @action(methods="put", url_path="user/<int:user_id>/update_institution/<int:institution_id>", detail=False)
    @authentication()
    @permissions([values.PERMISSION_TYPE_DEVELOPER, values.PERMISSION_TYPE_DOCTOR])
    def update_institution(self, request, *args, **kwargs):
        try:
            user_id = kwargs[values.USER_ID_REQUEST_URL_NAME]
            institution_id = kwargs[values.INSTITUTION_ID_REQUEST_URL_NAME]
            institution = Institution.institutions.get(id=institution_id)
            request_data = request.data.copy()
            if institution.manager.id != user_id:
                response = Response(error_code=Response.ERROR_601_NO_PERMISSIONS)
                return response

            institution_serializer = InstitutionSerializer(instance=institution)
            new_institution = institution_serializer.update(institution, request_data)
            new_institution.save()
            response = Response(error_code=status.HTTP_200_OK)
            response.add_data("institution", InstitutionFetchSerializer(new_institution).data)
            return response
        except ObjectDoesNotExist:
            response = Response(error_code=status.HTTP_400_BAD_REQUEST)
            response.set_msg("error institution")
            return response

    @action(methods="get", url_path="user/<int:user_id>/fetch_institution/<int:institution_id>", detail=False)
    @authentication()
    def fetch_institution(self, request, *args, **kwargs):
        try:
            institution_id = kwargs[values.INSTITUTION_ID_REQUEST_URL_NAME]
            institution = Institution.institutions.get(id=institution_id)
            response = Response(error_code=status.HTTP_200_OK)
            response.add_data("institution", InstitutionFetchSerializer(institution).data)
            return response
        except ObjectDoesNotExist:
            response = Response(error_code=status.HTTP_400_BAD_REQUEST)
            response.set_msg("error institution")
            return response

    @action(methods="post", url_path="user/<int:user_id>/hospital_join_request/", detail=False)
    @authentication()
    @permissions([values.PERMISSION_TYPE_DOCTOR])
    @validation_parameters(["hospital"])
    def hospital_join_request(self, request, *args, **kwargs):
        doctor_id = kwargs[values.USER_ID_REQUEST_URL_NAME]
        data = request.data.copy()
        data["doctor"] = doctor_id
        HJIR_institution_serializer = HJIRSerializer(data=data)
        if HJIR_institution_serializer.is_valid():
            HJIR_institution_instance = HJIR_institution_serializer.save()
            response = Response(error_code=status.HTTP_200_OK)
            response.add_data("join_institution", HJIRFetchSerializer(HJIR_institution_instance).data)
            return response
        else:
            response = Response(error_code=Response.ERROR_602_PARAMETERS_NOT_FOUND)
            for i in HJIR_institution_serializer.errors:
                response.add_validation_errors(i, str(HJIR_institution_serializer.errors.get(i)[0]))
            return response

    @action(methods="post", url_path="user/<int:user_id>/cancel_join_request/<int:join_request_id>", detail=False)
    @authentication()
    def cancel_join_request(self, request, *args, **kwargs):
        join_request_id = kwargs["join_request_id"]
        try:
            join_request = HospitalJoinRequest.objects.get(id=join_request_id)
            join_request.delete()
            response = Response(error_code=status.HTTP_200_OK)
            return response
        except ObjectDoesNotExist:
            response = Response(error_code=Response.ERROR_600_AUTHENTICATION)
            return response

    @action(methods="post", url_path="fetch_hospitals/", detail=False)
    def fetch_hospitals(self, request, *args, **kwargs):
        hospitals = Institution.hospitals.all()
        hospitals_serializer = InstitutionFetchHansSerializer(hospitals, many=True)
        response = Response(error_code=status.HTTP_200_OK)
        response.add_data("hospitals", hospitals_serializer.data)
        return response

    @action(methods="post", url_path="user/<int:user_id>/search_hospitals/", detail=False)
    @authentication()
    def search_hospitals(self, request, *args, **kwargs):
        search = request.GET["search"]
        hospitals = Institution.hospitals.filter(name__contains=search)
        print(hospitals)
        hospitals_serializer = InstitutionFetchHansSerializer(hospitals, many=True)
        response = Response(error_code=status.HTTP_200_OK)
        response.add_data("hospitals", hospitals_serializer.data)
        return response


create_hospital = InstitutionCore.as_view(actions={'post': 'create_hospital'})
create_lab = InstitutionCore.as_view(actions={'post': 'create_lab'})
create_software_company = InstitutionCore.as_view(actions={'post': 'create_software_company'})
update_institution = InstitutionCore.as_view(actions={'put': 'update_institution'})
fetch_institution = InstitutionCore.as_view(actions={'get': 'fetch_institution'})
hospital_join_request = InstitutionCore.as_view(actions={'post': "hospital_join_request"})
fetch_hospitals = InstitutionCore.as_view(actions={'get': "fetch_hospitals"})
search_hospitals = InstitutionCore.as_view(actions={'get': "search_hospitals"})
cancel_join_request = InstitutionCore.as_view(actions={'delete': "cancel_join_request"})
