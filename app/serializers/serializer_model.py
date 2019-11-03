from rest_framework import serializers

from app.models.model_model import Model, API, IOAPI, ModelImage, ModelSubscription, ModelRequest, IORequest
from app.serializers.serializer_institutions import InstitutionFetchSerializer, InstitutionSimpleFetchSerializer


class ModelFetchSerializer(serializers.ModelSerializer):
    company = InstitutionFetchSerializer()

    class Meta:
        model = Model
        fields = "__all__"


class ModelSimpleFetchSerializer(serializers.ModelSerializer):

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


class ModelRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelRequest
        fields = "__all__"


class IORequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = IORequest
        fields = "__all__"
