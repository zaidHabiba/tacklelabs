import functools

from app.models.model_user import User
from .customized_response import Response
from .values import USER_ID_SESSIONS_KEY, USER_ID_REQUEST_URL_NAME


def authentication():
    def authentication_inner_function_one(func):
        @functools.wraps(func)
        def authentication_inner_function_two(*args, **kwargs):
            print("@authentications")
            request = args[1]
            user_id = kwargs[USER_ID_REQUEST_URL_NAME]
            session_user_id = request.session.get(USER_ID_SESSIONS_KEY, None)
            session_user_id = user_id
            if session_user_id is None:
                return Response(error_code=Response.ERROR_600_AUTHENTICATION)
            elif session_user_id != user_id:
                return Response(error_code=Response.ERROR_600_AUTHENTICATION)
            else:
                return func(*args, **kwargs)

        return authentication_inner_function_two

    return authentication_inner_function_one


def permissions(permissions_list):
    def permissions_inner_function_one(func):
        @functools.wraps(func)
        def permissions_inner_function_two(*args, **kwargs):
            print("@permission")
            user_id = kwargs[USER_ID_REQUEST_URL_NAME]
            user_type = User.users.get_user_type(user_id).type
            if user_type in permissions_list:
                return func(*args, **kwargs)
            else:
                return Response(error_code=Response.ERROR_601_NO_PERMISSIONS)

        return permissions_inner_function_two

    return permissions_inner_function_one


def validation_parameters(parameters_list):
    def validation_parameters_inner_function_one(func):
        @functools.wraps(func)
        def validation_parameters_inner_function_two(*args, **kwargs):
            print("@validation_parameters")
            request = args[1]
            request_data = request.data
            keys_values = [key for key, value in request_data.items()]
            all_in_request = True
            for item in parameters_list:
                if item not in keys_values:
                    all_in_request = False
                    break
            if all_in_request:
                return func(*args, **kwargs)
            else:
                return Response(error_code=Response.ERROR_602_PARAMETERS_NOT_FOUND)

        return validation_parameters_inner_function_two

    return validation_parameters_inner_function_one


def validation_data(validators):
    def validation_data_inner_function_one(func):
        @functools.wraps(func)
        def validation_data_inner_function_two(*args, **kwargs):
            print("@validation_data")
            request = args[1]
            response = Response(error_code=Response.ERROR_603_DATA_NOT_VALID)
            data_valid = True
            for parameter_name, validator in validators.items():
                if not validator(request.data[parameter_name]):
                    data_valid = False
                    response.add_validation_errors(parameter_name, parameter_name + " not valid")
            if not data_valid:
                return response
            else:
                return func(*args, **kwargs)

        return validation_data_inner_function_two

    return validation_data_inner_function_one
