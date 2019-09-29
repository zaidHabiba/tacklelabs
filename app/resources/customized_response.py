from rest_framework import status
from rest_framework.response import Response as res


class Response(res):
    ERROR_600_AUTHENTICATION = 600
    ERROR_601_NO_PERMISSIONS = 601
    ERROR_602_PARAMETERS_NOT_FOUND = 602
    ERROR_603_DATA_NOT_VALID = 603
    ERROR_604_WRONG_VERIFICATION_CODE = 604
    ERROR_605_AUTHENTICATION_FAILED = 605

    error_dict = {
        ERROR_600_AUTHENTICATION: 'Authentication failed',
        ERROR_601_NO_PERMISSIONS: 'No permissions',
        ERROR_602_PARAMETERS_NOT_FOUND: 'Parameters not founds',
        ERROR_603_DATA_NOT_VALID: 'Parameters data not valid',
        ERROR_604_WRONG_VERIFICATION_CODE: 'Wronging verification code',
        ERROR_605_AUTHENTICATION_FAILED: 'Authentication failed'
    }

    def __init__(self, error_code, status_code=status.HTTP_200_OK):
        super(Response, self).__init__(status=status_code)
        self.is_validation_errors_set = False
        self.data_to_set = {}
        if error_code >= 600:
            self.error_msg = self.error_dict.get(error_code)
            self.error_code = error_code
        else:
            if error_code is status.HTTP_200_OK:
                self.error_msg = "SUCCESS"
                self.error_code = self.status_code
                super(Response, self).__init__(status=status_code)
            else:
                if status_code is 200:
                    super(Response, self).__init__(status=error_code)
                else:
                    super(Response, self).__init__(status=status_code)
                self.error_msg = self.reason_phrase
                self.error_code = self.status_code
                # for local only
        self.to_json()
        """
        self["Access-Control-Allow-Origin"] = "http://localhost:3000"
        self["Access-Control-Allow-Credentials"] = "true"
        self["Access-Control-Allow-Methods"] = "GET,HEAD,OPTIONS,POST,PUT"
        self["Access-Control-Allow-Headers"] = "Access-Control-Allow-Headers, Origin,Accept, " \
                                               "X-Requested-With, Content-Type, " \
                                               "Access-Control-Request-Method, " \
                                               "Access-Control-Request-Headers"

        """
    def to_json(self):
        self.data = {
            "data": self.data_to_set,
            'status': self.error_msg,
            'status_code': self.error_code,
        }
        return self.data

    def set_msg(self, msg):
        self.data_to_set.__setitem__("message", msg)
        self.to_json()

    def add_validation_errors(self, field, field_error):
        if self.is_validation_errors_set:
            self.data_to_set.get("validation_errors").append({"field": field, "field_error": field_error})
        else:
            self.data_to_set.__setitem__("validation_errors", [{"field": field, "field_error": field_error}])
            self.is_validation_errors_set = True
        self.to_json()

    def add_data(self, key: object, value: object):
        self.data_to_set.__setitem__(key, value)
        self.to_json()

    def set_status_msg(self, msg):
        self.error_msg = msg
        self.to_json()

    def set_status_code(self, error_code):
        if error_code >= 600:
            self.error_msg = self.error_dict.get(error_code)
            self.error_code = error_code
        else:
            if error_code is status.HTTP_200_OK:
                self.error_msg = "success"
                self.error_code = self.status_code
            else:
                self.error_msg = self.reason_phrase
                self.error_code = self.status_code
        self.to_json()
