from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.exceptions import APIException
from django.utils.encoding import force_text
from rest_framework import viewsets, status
from rest_framework import serializers
from .models import advisor, advisor_booking

User._meta.get_field('email')._unique = True


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id',)


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password']
        )
        return user


class CustomValidation(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'email/password combination was wrong.'

    def __init__(self, detail, status_code):
        if status_code is not None: self.status_code = status_code
        if detail is not None:
            self.detail = {'detail': force_text(self.default_detail)}


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise CustomValidation("email/password combination was wrong", status_code=status.HTTP_401_UNAUTHORIZED)


class RelatedFieldAlternative(serializers.PrimaryKeyRelatedField):
    def __init__(self, **kwargs):
        self.serializer = kwargs.pop('serializer', None)
        if self.serializer is not None and not issubclass(self.serializer, serializers.Serializer):
            raise TypeError('"serializer" is not a valid serializer class')

        super().__init__(**kwargs)

    def use_pk_only_optimization(self):
        return False if self.serializer else True

    def to_representation(self, instance):
        if self.serializer:
            return self.serializer(instance, context=self.context).data
        return super().to_representation(instance)


class AdvisorSerializer(serializers.ModelSerializer):
    class Meta:
        model = advisor
        fields = '__all__'


class AdvisorBookSerializers(serializers.ModelSerializer):
    advisors = RelatedFieldAlternative(queryset=advisor.objects.all(), serializer=AdvisorSerializer)

    class Meta:
        model = advisor_booking
        fields = '__all__'
