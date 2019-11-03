import requests
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action

from app.models.model_institutions import Institution, HospitalJoinRequest
from app.models.model_model import API, IOAPI, Model, ModelSubscription, ModelImage
from app.models.model_report import ReportImage
from app.models.model_user import User
from app.resources import values
from app.resources.customized_response import Response
from app.resources.decorators import authentication
from app.serializers.serializer_model import APISerializer, ModelSerializer, ModelImageSerializer, IOAPISerializer, \
    ModelFetchSerializer, ModelSubscriptionSerializer, ModelSubscriptionFetchSerializer, ModelRequestSerializer, \
    IORequestSerializer


class ModelCore(viewsets.ViewSet):

    @action(methods="post", url_path="user/<int:user_id>/create_api", detail=False)
    @authentication()
    def create_api(self, request, *args, **kwargs):
        request_data = request.data.copy()
        api_serializer = APISerializer(data=request_data)
        if api_serializer.is_valid():
            api_instance = api_serializer.save()
            response = Response(error_code=status.HTTP_200_OK)
            response.add_data("api", APISerializer(api_instance).data)
            return response
        else:
            response = Response(error_code=Response.ERROR_603_DATA_NOT_VALID)
            return response

    @action(methods="post", url_path="user/<int:user_id>/create_model", detail=False)
    @authentication()
    def create_model(self, request, *args, **kwargs):
        request_data = request.data.copy()
        model_serializer = ModelSerializer(data=request_data)
        if model_serializer.is_valid():
            model_instance = model_serializer.save()
            response = Response(error_code=status.HTTP_200_OK)
            response.add_data("model", ModelSerializer(model_instance).data)
            return response
        else:
            response = Response(error_code=Response.ERROR_603_DATA_NOT_VALID)
            return response

    @action(methods="post", url_path="user/<int:user_id>/create_image_model", detail=False)
    @authentication()
    def create_image_model(self, request, *args, **kwargs):
        request_data = request.data.copy()
        image_model_serializer = ModelImageSerializer(data=request_data)
        if image_model_serializer.is_valid():
            image_model_instance = image_model_serializer.save()
            response = Response(error_code=status.HTTP_200_OK)
            response.add_data("image", ModelImageSerializer(image_model_instance).data)
            return response
        else:
            response = Response(error_code=Response.ERROR_603_DATA_NOT_VALID)
            return response

    @action(methods="post", url_path="user/<int:user_id>/create_io_api", detail=False)
    @authentication()
    def create_io_api(self, request, *args, **kwargs):
        request_data = request.data.copy()
        io_api_serializer = IOAPISerializer(data=request_data)
        if io_api_serializer.is_valid():
            io_api_model_instance = io_api_serializer.save()
            response = Response(error_code=status.HTTP_200_OK)
            response.add_data("io_api", IOAPISerializer(io_api_model_instance).data)
            return response
        else:
            response = Response(error_code=Response.ERROR_603_DATA_NOT_VALID)
            return response

    @action(methods="post", url_path="user/<int:user_id>/send_request/<int:api>/<int:subscription_id>/", detail=False)
    @authentication()
    def send_request(self, request, *args, **kwargs):
        request_data = request.data.copy()
        api_id = kwargs["api"]
        user_id = kwargs["user_id"]
        subscription_id = kwargs["subscription_id"]
        api = API.objects.get(pk=api_id)
        model = Model.objects.get(api=api_id)

        subscription = ModelSubscription.objects.get(pk=subscription_id)
        if subscription.number_of_request - subscription.request_used > 0:
            subscription.request_used = subscription.request_used + 1
            subscription.save()
        else:
            response = Response(error_code=status.HTTP_400_BAD_REQUEST)
            return response

        input_api = IOAPI.objects.filter(api=api.id, is_input=True)
        output_api = IOAPI.objects.filter(api=api.id, is_input=False)
        data = {}
        files = {}
        response_from_request = ""
        model_request = ModelRequestSerializer(data={"model": model.pk, "user": user_id})

        if model_request.is_valid():
            model_request = model_request.save()
        else:
            response = Response(error_code=status.HTTP_400_BAD_REQUEST)
            return response
        for field in input_api:
            if field.is_file:
                try:
                    image_id = int(request_data[field.json_name])
                    report_image = ReportImage.objects.get(id=image_id)
                    files[field.json_name] = report_image.image
                    io_request = IORequestSerializer(
                        data={"io": field.pk, "request": model_request.pk, "file_value": report_image.image})
                    if io_request.is_valid():
                        io_request.save()
                except Exception:
                    files[field.json_name] = request_data[field.json_name]
                    io_request = IORequestSerializer(
                        data={"io": field.pk, "request": model_request.pk, "file_value": request_data[field.json_name]})
                    if io_request.is_valid():
                        io_request.save()
            else:
                data[field.json_name] = request_data[field.json_name]
                io_request = IORequestSerializer(
                    data={"io": field.pk, "request": model_request.pk, "text_value": request_data[field.json_name]})
                if io_request.is_valid():
                    io_request.save()

        if api.method == "POST":
            response_from_request = requests.post(api.url, files=files, data=data)
        elif api.method == "GET":
            response_from_request = requests.get(api.url, files=files, data=data)
        print(response_from_request.json())
        if response_from_request.status_code != 200:
            response = Response(error_code=status.HTTP_400_BAD_REQUEST)
            return response

        response_back = {}
        for field in output_api:
            if field.is_file:
                if "http" in response_from_request.json()[field.json_name]:
                    io_request = IORequestSerializer(
                        data={"io": field.pk, "request": model_request.pk,
                              "text_value": response_from_request.json()[field.json_name]})
                    if io_request.is_valid():
                        io_request = io_request.save()
                        response_back[field.json_name] = io_request.text_value

                io_request = IORequestSerializer(
                    data={"io": field.pk, "request": model_request.pk,
                          "file_value": response_from_request.json()[field.json_name]})
                if io_request.is_valid():
                    io_request = io_request.save()
                    response_back[field.json_name] = io_request.file_value.url
            else:
                response_back[field.json_name] = response_from_request.json()[field.json_name]
                io_request = IORequestSerializer(
                    data={"io": field.pk, "request": model_request.pk,
                          "text_value": response_from_request.json()[field.json_name]})
                if io_request.is_valid():
                    io_request.save()

        response = Response(error_code=status.HTTP_200_OK)
        response.add_data("response_back", response_back)
        return response

    @action(methods="post", url_path="user/<int:user_id>/fetch_models/", detail=False)
    @authentication()
    def fetch_models(self, request, *args, **kwargs):
        user_id = kwargs["user_id"]
        search = request.GET.get("search", "")
        user = User.users.get(id=user_id)
        models = Model.objects.filter(name__contains=search)
        if user.type.type == values.PERMISSION_TYPE_DOCTOR:
            models = Model.objects.filter(name__contains=search, doctor_model=True)
        elif user.type.type == values.PERMISSION_TYPE_PATIENT:
            models = Model.objects.filter(name__contains=search, patient_model=True)
        else:
            institution = Institution.objects.get(manager=user.id)
            if len(institution) != 0:
                if institution.type.type == values.INSTITUTION_HOSPITAL_NAME:
                    models = Model.objects.filter(name__contains=search, doctor_model=True)
                else:
                    models = Model.objects.filter(name__contains=search, lab_model=True)

        response = Response(error_code=status.HTTP_200_OK)
        response.add_data("models", ModelFetchSerializer(models, many=True).data)
        return response

    @action(methods="post", url_path="user/<int:user_id>/create_subscription/", detail=False)
    @authentication()
    def create_subscription(self, request, *args, **kwargs):
        request_data = request.data.copy()
        model_serializer = ModelSubscriptionSerializer(data=request_data)
        if model_serializer.is_valid():
            model_instance = model_serializer.save()
            response = Response(error_code=status.HTTP_200_OK)
            response.add_data("model", ModelSubscriptionSerializer(model_instance).data)
            return response
        else:
            response = Response(error_code=Response.ERROR_603_DATA_NOT_VALID)
            return response

    @action(methods="get", url_path="user/<int:user_id>/fetch_model_images/<model_id>", detail=False)
    @authentication()
    def fetch_model_images(self, request, *args, **kwargs):
        model_id = kwargs["model_id"]
        models = ModelImage.objects.filter(model=model_id)
        image_model_serializer = ModelImageSerializer(models, many=True)
        response = Response(error_code=status.HTTP_200_OK)
        response.add_data("images", image_model_serializer.data)
        return response

    @action(methods="get", url_path="user/<int:user_id>/fetch_subscription/", detail=False)
    @authentication()
    def fetch_subscription(self, request, *args, **kwargs):
        user_id = kwargs["user_id"]
        type = User.users.get_user_type(user_id)
        model_subscriptions = ModelSubscription.objects.filter(user=user_id)
        response = Response(error_code=status.HTTP_200_OK)
        response.add_data("model_subscriptions", ModelSubscriptionFetchSerializer(model_subscriptions, many=True).data)
        if type.type == values.PERMISSION_TYPE_DOCTOR:
            try:
                join_request = HospitalJoinRequest.objects.get(doctor=user_id, is_accepted=True)
                hospital_model_subscriptions = ModelSubscription.objects.filter(
                    user=join_request.hospital.manager.id)
                response.add_data("hospital_model_subscriptions",
                                  ModelSubscriptionFetchSerializer(hospital_model_subscriptions, many=True).data)
            except ObjectDoesNotExist:
                pass
        return response

    @action(methods="get", url_path="user/<int:user_id>/fetch_io_api/<int:api_id>", detail=False)
    @authentication()
    def fetch_io_api(self, request, *args, **kwargs):
        user_id = kwargs["user_id"]
        api_id = kwargs["api_id"]
        ios = IOAPI.objects.filter(api=api_id)
        response = Response(error_code=status.HTTP_200_OK)
        response.add_data("ios", IOAPISerializer(ios, many=True).data)
        return response


create_api = ModelCore.as_view(actions={'post': 'create_api'})
create_model = ModelCore.as_view(actions={'post': 'create_model'})
create_image_model = ModelCore.as_view(actions={'post': 'create_image_model'})
create_io_api = ModelCore.as_view(actions={'post': 'create_io_api'})
send_request = ModelCore.as_view(actions={'post': 'send_request'})
fetch_io_api = ModelCore.as_view(actions={'get': 'fetch_io_api'})
fetch_models = ModelCore.as_view(actions={'get': 'fetch_models'})
create_subscription = ModelCore.as_view(actions={'post': 'create_subscription'})
fetch_model_images = ModelCore.as_view(actions={'get': 'fetch_model_images'})
fetch_subscription = ModelCore.as_view(actions={'get': 'fetch_subscription'})
