from django.core.exceptions import ValidationError
from rest_framework import serializers

from app.models.model_institutions import Institution, InstitutionType
from app.resources.exceptions import ValidationDataException
from app.resources.validator import is_name_valid


class InstitutionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstitutionType
        fields = ('id', 'type', 'logo')


class InstitutionFetchSerializer(serializers.ModelSerializer):
    type = InstitutionTypeSerializer()

    class Meta:
        model = Institution
        fields = "__all__"


class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = "__all__"

    def update(self, instance, data):
        exception = ValidationDataException()

        instance.name = data.get('name', instance.name)
        instance.logo = data.get('logo', instance.logo)
        instance.photo = data.get('photo', instance.photo)
        instance.website = data.get('website', instance.website)
        instance.description = data.get('description', instance.description)

        new_phone_number = data.get('phone_number')
        if new_phone_number is not None:
            try:
                instance.phone_number = new_phone_number
            except ValidationError:
                exception.add_error_field("phone_number", "phone_number not valid")

        new_country = data.get('country')
        if new_country is not None:
            if is_name_valid(new_country):
                instance.country = new_country
            else:
                exception.add_error_field("country", "country not valid")

        new_city = data.get('city')
        if new_city is not None:
            if is_name_valid(new_city):
                instance.type = new_city
            else:
                exception.add_error_field("city", "city not valid")

        new_street = data.get('street')
        if new_street is not None:
            if is_name_valid(new_street):
                instance.street = new_street
            else:
                exception.add_error_field("street", "street not valid")

        new_email = data.get('email')
        if new_email is not None:
            try:
                instance.email = new_email
            except ValidationError:
                exception.add_error_field("new_email", "new_email not valid")

        if exception.is_exception():
            raise exception
        else:
            return instance
