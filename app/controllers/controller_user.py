from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action

from app.models.model_user import User
from app.resources import values
from app.resources.customized_response import Response
from app.resources.decorators import validation_parameters, authentication, validation_data
from app.resources.exceptions import ValidationDataException
from app.resources.validator import is_email_valid, is_password_valid, is_date_valid, is_name_valid, is_gender_valid, \
    is_int_valid
from app.serializers.serializer_user import UserFetchSerializer, UserSerializer
from django.core.exceptions import ObjectDoesNotExist
from app.resources.values import USER_ID_SESSIONS_KEY
class UserRegisterCore(viewsets.ViewSet):

    @action(methods="post", url_path="user/login/", detail=False)
    @validation_parameters(["email", "password"])
    def user_login(self, request, *args, **kwargs):
        request_data = request.data
        session_user_id = request.session.get(USER_ID_SESSIONS_KEY, None)
        if session_user_id is not None:
            user = User.users.get(id=session_user_id)
            response = Response(error_code=status.HTTP_200_OK)
            response.add_data("user", UserFetchSerializer(user).data)
            request.session[values.USER_ID_SESSIONS_KEY] = user.id
            return response
        else:
            user = User.users.login_user(email=request_data["email"], password=request_data["password"])
            if user is None:
                response = Response(error_code=Response.ERROR_605_AUTHENTICATION_FAILED)
                response.set_msg("Email or Password not correct")
                return response
            else:
                response = Response(error_code=status.HTTP_200_OK)
                response.add_data("user", UserFetchSerializer(user).data)
                request.session[values.USER_ID_SESSIONS_KEY] = user.id
                return response

    @action(methods="post", url_path="user/<int:user_id>/logout/", detail=False)
    @authentication()
    def user_logout(self, request, *args, **kwargs):
        user_id = kwargs[values.USER_ID_REQUEST_URL_NAME]
        operation_state = User.users.logout_user(user_id=user_id)
        if operation_state:
            del request.session[values.USER_ID_SESSIONS_KEY]
            response = Response(error_code=Response.ERROR_605_AUTHENTICATION_FAILED)
            response.set_msg("Logout successful")
            return response
        else:
            response = Response(error_code=Response.ERROR_605_AUTHENTICATION_FAILED)
            response.set_msg("Logout not successful")
            return response

    @action(methods="post", url_path="user/signup/", detail=False)
    @validation_parameters(['first_name', 'second_name', 'middle_name', 'last_name', 'country', 'city'
                               , 'type', 'gender', 'email', 'birth_date', 'password'])
    @validation_data({
        'first_name': is_name_valid, 'second_name': is_name_valid
        , 'middle_name': is_name_valid, 'last_name': is_name_valid
        , 'country': is_name_valid, 'city': is_name_valid
        , 'type': is_int_valid, 'gender': is_gender_valid, 'email': is_email_valid
        , 'birth_date': is_date_valid, 'password': is_password_valid})
    def user_signup(self, request, *args, **kwargs):
        request_data = request.data.copy()
        user_serializer = UserSerializer(data=request_data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            response = Response(error_code=Response.ERROR_605_AUTHENTICATION_FAILED)
            response.add_data("user", UserFetchSerializer(user).data)
            request.session[values.USER_ID_SESSIONS_KEY] = user.id
            return response
        else:
            response = Response(error_code=Response.ERROR_602_PARAMETERS_NOT_FOUND)
            for i in user_serializer.errors:
                response.add_validation_errors(i, str(user_serializer.errors.get(i)[0]))
            return response

    @action(methods="put", url_path="user/<int:user_id>/update/", detail=False)
    @authentication()
    def user_update(self, request, *args, **kwargs):
        try:
            user_id = kwargs[values.USER_ID_REQUEST_URL_NAME]
            user = User.users.get(id=user_id)
            request_data = request.data.copy()
            user_serializer = UserSerializer(instance=user)
            new_user = user_serializer.update(user, request_data)
            new_user.save()
            response = Response(error_code=status.HTTP_200_OK)
            response.set_msg("User updated")
            return response
        except ValidationDataException as e:
            if e.is_message_exception():
                response = Response(error_code=Response.ERROR_603_DATA_NOT_VALID)
                response.set_msg(e.get_message())
                return response
            else:
                response = Response(error_code=Response.ERROR_603_DATA_NOT_VALID)
                response.add_data("validation_errors", e.get_errors_list())
                return response
        except ObjectDoesNotExist:
            response = Response(error_code=status.HTTP_400_BAD_REQUEST)
            response.set_msg("user not found")
            return response

    @action(methods="put", url_path="user/<int:user_id>/change_password/", detail=False)
    @authentication()
    @validation_parameters(['old_password', 'new_password'])
    @validation_data({'old_password': is_password_valid, 'new_password': is_password_valid})
    def user_update_password(self, request, *args, **kwargs):
        try:
            user_id = kwargs[values.USER_ID_REQUEST_URL_NAME]
            user = User.users.get(id=user_id)
            request_data = request.data.copy()
            user_serializer = UserSerializer(instance=user)
            new_user = user_serializer.update_password(user, request_data)
            new_user.save()
            response = Response(error_code=status.HTTP_200_OK)
            response.set_msg("Password updated")
            return response
        except ValidationDataException as e:
            if e.is_message_exception():
                response = Response(error_code=Response.ERROR_603_DATA_NOT_VALID)
                response.set_msg(e.get_message())
                return response
            else:
                response = Response(error_code=Response.ERROR_603_DATA_NOT_VALID)
                response.add_data("validation_errors", e.get_errors_list())
                return response


user_login = UserRegisterCore.as_view(actions={'post': 'user_login'})
user_logout = UserRegisterCore.as_view(actions={'post': 'user_logout'})
user_signup = UserRegisterCore.as_view(actions={'post': 'user_signup'})
user_update = UserRegisterCore.as_view(actions={'put': 'user_update'})
user_update_password = UserRegisterCore.as_view(actions={'put': 'user_update_password'})
