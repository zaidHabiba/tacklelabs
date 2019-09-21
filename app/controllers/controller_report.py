from rest_framework import viewsets
from rest_framework.decorators import action

from app.resources.decorators import validation_parameters, validation_data
from app.resources.validator import is_email_valid, is_password_valid


class UserRegisterCore(viewsets.ViewSet):

    @action(methods="post", url_path="user/login/", detail=False)
    @validation_parameters(["email", "password"])
    @validation_data({"email": is_email_valid, "password": is_password_valid})
    def create_report(self, request, *args, **kwargs):
        pass
