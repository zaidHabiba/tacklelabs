from rest_framework import serializers

from app.models.model_model import Model, API, IOAPI, ModelImage, ModelSubscription
from app.serializers.serializer_institutions import InstitutionFetchSerializer, InstitutionSimpleFetchSerializer
from app.serializers.serializer_user import UserFetchSearchSerializer


class ModelFetchSerializer(serializers.ModelSerializer):
    company = InstitutionFetchSerializer()

    class Meta:
        model = Model
        fields = "__all__"


class ModelSimpleFetchSerializer(serializers.ModelSerializer):
    company = InstitutionSimpleFetchSerializer()

    class Meta:
        model = Model
        fields = "__all__"


class ModelSubscriptionFetchSerializer(serializers.ModelSerializer):
    model = ModelSimpleFetchSerializer()

    class Meta:
        model = ModelSubscription
        fields = "__all__"


class ModelSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelSubscription
        fields = "__all__"


class ModelImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelImage
        fields = "__all__"


class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = "__all__"


class APISerializer(serializers.ModelSerializer):
    class Meta:
        model = API
        fields = "__all__"


class IOAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = IOAPI
        fields = "__all__"
