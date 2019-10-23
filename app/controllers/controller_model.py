import requests
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action

from app.models.model_institutions import Institution
from app.models.model_model import API, IOAPI, Model, ModelSubscription
from app.models.model_user import User
from app.resources import values
from app.resources.customized_response import Response
from app.resources.decorators import authentication
from app.serializers.serializer_model import APISerializer, ModelSerializer, ModelImageSerializer, IOAPISerializer


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

    @action(methods="post", url_path="user/<int:user_id>/send_request/<int:api>", detail=False)
    @authentication()
    def send_request(self, request, *args, **kwargs):
        request_data = request.data.copy()
        api_id = kwargs["api"]
        api = API.objects.get(pk=api_id)
        model = Model.objects.get(api=api_id)
        subscriptions = ModelSubscription.objects.filter(model=model.id)
        input_api = IOAPI.objects.filter(api=api.id, is_input=True)
        output_api = IOAPI.objects.filter(api=api.id, is_input=False)
        data = {}
        response_from_request = ""
        for field in input_api:
            data[field.json_name] = request_data[field.json_name]
        if api.method == "POST":
            response_from_request = requests.post(api.url, data)
        elif api.method == "GET":
            response_from_request = requests.get(api.url, data)
        print(response_from_request.json())
        if response_from_request.status_code != 200:
            response = Response(error_code=status.HTTP_400_BAD_REQUEST)
            return response
        response_back = {}
        for field in output_api:
            response_back[field.json_name] = response_from_request.json()[field.json_name]
        response = Response(error_code=status.HTTP_200_OK)
        response.add_data("response_back", response_back)
        for subscription in subscriptions:
            if subscription.request_numbers > 0:
                subscription.request_numbers = subscription.request_numbers - 1
                subscription.save()
                break
        return response

    @action(methods="post", url_path="user/<int:user_id>/fetch_models/", detail=False)
    @authentication()
    def fetch_models(self, request, *args, **kwargs):
        user_id = kwargs["user_id"]
        search = request.GET["search"]
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
        response.add_data("models", ModelSerializer(models, many=True).data)
        return response


create_api = ModelCore.as_view(actions={'post': 'create_api'})
create_model = ModelCore.as_view(actions={'post': 'create_model'})
create_image_model = ModelCore.as_view(actions={'post': 'create_image_model'})
create_io_api = ModelCore.as_view(actions={'post': 'create_io_api'})
send_request = ModelCore.as_view(actions={'post': 'send_request'})
fetch_models = ModelCore.as_view(actions={'get': 'fetch_models'})
