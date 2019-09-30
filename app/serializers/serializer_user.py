from rest_framework import serializers

from app.models.model_user import User, UserType
from app.resources.encryptor import encrypt_password
from app.resources.exceptions import ValidationDataException
from app.resources.validator import is_password_valid, is_name_valid, is_gender_valid, ValidationError


class UserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserType
        fields = ('id', 'type', 'logo')


class DoctorFetchSerializer(serializers.ModelSerializer):
    type = UserTypeSerializer()

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'phone_number', 'email', 'photo')


class PatientFetchSerializer(serializers.ModelSerializer):
    type = UserTypeSerializer()

    class Meta:
        model = User
        fields = (
        'id', 'first_name', 'second_name', 'middle_name', 'gender', 'last_name', 'phone_number', 'birth_date', 'email',
        'photo')


class UserFetchSerializer(serializers.ModelSerializer):
    type = UserTypeSerializer()

    class Meta:
        model = User
        fields = ('id', 'first_name', 'second_name', 'middle_name', 'country', 'city', 'street'
                  , 'last_name', 'type', 'phone_number', 'gender', 'email', 'photo', 'birth_date', 'is_login')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def update_password(self, instance, data):
        exception = ValidationDataException()
        new_password = data.get('new_password')
        old_password = data.get('old_password')
        if new_password is not None and old_password is not None:
            if is_password_valid(password=new_password) and is_password_valid(password=old_password):
                if instance.password == encrypt_password(password=old_password):
                    instance.password = encrypt_password(password=new_password)
                else:
                    exception.add_error_field("password", "password not match")
            else:
                exception.add_error_field("password", "password not valid")
        else:
            exception.add_error_field("password", "password not found")

        if exception.is_exception():
            raise exception
        else:
            return instance

    def update(self, instance, data):
        exception = ValidationDataException()

        instance.photo = data.get('photo', instance.photo)

        new_first_name = data.get('first_name')
        if new_first_name is not None:
            if is_name_valid(new_first_name):
                instance.first_name = new_first_name
            else:
                exception.add_error_field("first_name", "first_name not valid")

        new_second_name = data.get('second_name')
        if new_second_name is not None:
            if is_name_valid(new_second_name):
                instance.second_name = new_second_name
            else:
                exception.add_error_field("second_name", "second_name not valid")

        new_middle_name = data.get('middle_name')
        if new_middle_name is not None:
            if is_name_valid(new_middle_name):
                instance.middle_name = new_middle_name
            else:
                exception.add_error_field("middle_name", "middle_name not valid")

        new_last_name = data.get('last_name')
        if new_last_name is not None:
            if is_name_valid(new_last_name):
                instance.last_name = new_last_name
            else:
                exception.add_error_field("last_name", "last_name not valid")

        new_country = data.get('country')
        if new_country is not None:
            if is_name_valid(new_country):
                instance.country = new_country
            else:
                exception.add_error_field("country", "country not valid")

        new_city = data.get('city')
        if new_city is not None:
            if is_name_valid(new_city):
                instance.city = new_city
            else:
                exception.add_error_field("city", "city not valid")

        new_street = data.get('street')
        if new_street is not None:
            if is_name_valid(new_street):
                instance.street = new_street
            else:
                exception.add_error_field("street", "street not valid")

        new_birth_date = data.get('birth_date')
        if new_birth_date is not None:
            try:
                instance.birth_date = new_birth_date
            except ValidationError:
                exception.add_error_field("birth_date", "birth_date not valid")

        new_phone_number = data.get('phone_number')
        if new_phone_number is not None:
            try:
                instance.phone_number = new_phone_number
            except ValidationError:
                exception.add_error_field("phone_number", "phone_number not valid")

        new_gender = data.get('gender')
        if new_gender is not None:
            if is_gender_valid(new_gender):
                instance.gender = new_gender
            else:
                exception.add_error_field("gender", "gender not valid")

        if exception.is_exception():
            raise exception
        else:
            return instance

    @staticmethod
    def validate_password(password):
        if not is_password_valid(password=password):
            raise serializers.ValidationError("The password is not valid")
        else:
            return encrypt_password(password)

    @staticmethod
    def validate_first_name(first_name):
        if not is_name_valid(name=first_name):
            raise serializers.ValidationError("The name contains not allowed characters")
        else:
            return first_name

    @staticmethod
    def validate_middle_name(middle_name):
        if not is_name_valid(name=middle_name):
            raise serializers.ValidationError("The name contains not allowed characters")
        else:
            return middle_name

    @staticmethod
    def validate_last_name(last_name):
        if not is_name_valid(name=last_name):
            raise serializers.ValidationError("The name contains not allowed characters")
        else:
            return last_name

    @staticmethod
    def validate_gender(gender):
        if not is_gender_valid(gender):
            raise serializers.ValidationError("The gender is not valid")
        else:
            return gender
