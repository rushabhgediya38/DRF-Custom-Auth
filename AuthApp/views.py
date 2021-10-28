from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer
from rest_framework import viewsets
from .models import advisor, advisor_booking
from .serializers import AdvisorSerializer, AdvisorBookSerializers
from django.contrib.auth.models import User
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render


class UserAPIView(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class RegisterAPIView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class AdminAdvisorViewSet(viewsets.ModelViewSet):
    queryset = advisor.objects.all()
    serializer_class = AdvisorSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)

        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class MultipleFieldLookupMixin:
    def get_object(self):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        multi_filter = {field: self.kwargs[field] for field in self.lookup_fields}
        obj = get_object_or_404(queryset, **multi_filter)
        self.check_object_permissions(self.request, obj)
        return obj


class AdvisorSerializerGeneric(MultipleFieldLookupMixin, generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = LoginSerializer
    lookup_fields = ['user_id']


def advisor_list(request, user_id):
    try:
        user_data = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        advisor_data = advisor.objects.all()
        serializer = AdvisorSerializer(advisor_data, many=True)
        return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def advisor_book(request, user_id, advisor_id):
    try:
        user_data = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    try:
        advisor_data = advisor.objects.get(id=advisor_id)
    except advisor.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        advisor_books = JSONParser().parse(request)
        advisor_books['user'] = user_id
        advisor_books['advisors'] = advisor_id
        serializer = AdvisorBookSerializers(data=advisor_books)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return HttpResponse(status=status.HTTP_200_OK)


def advisor_book_list(request, user_id):
    try:
        user_data = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        advisor_bookings = advisor_booking.objects.filter(user=user_id)
        serializer = AdvisorBookSerializers(advisor_bookings, many=True)

        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)


def index(request):
    return render(request, 'index.html')
