class ValidationDataException(Exception):

    def __init__(self):
        super()
        self.errors = []
        self.exception_flag = False
        self.message = ""

    def add_error_field(self, field_name, field_error):
        self.exception_flag = True
        self.errors.append({"field": field_name, "field_error": field_error})

    def get_errors_list(self):
        return self.errors

    def is_exception(self):
        return self.exception_flag

    def set_message(self, message):
        self.message = message

    def get_message(self):
        return self.message

    def is_message_exception(self):
        if self.message == "":
            return False
        else:
            return True

    def raise_exception(self):
        if self.is_exception() or self.is_message_exception():
            raise self
