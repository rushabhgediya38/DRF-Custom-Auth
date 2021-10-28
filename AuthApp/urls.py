from knox import views as knox_views
from django.urls import path, include
from .views import LoginAPIView, RegisterAPIView, \
    AdminAdvisorViewSet, advisor_list, advisor_book, advisor_book_list, index
from rest_framework import routers

router = routers.DefaultRouter()

router.register('', AdminAdvisorViewSet)

urlpatterns = [
    path('user/register/', RegisterAPIView.as_view(), name='register'),
    path('user/login/', LoginAPIView.as_view(), name='login'),
    path('user/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('admin/advisor/', include(router.urls)),
    path('user/<int:user_id>/advisor', advisor_list, name='advisor_user'),
    path('user/<int:user_id>/advisor/<int:advisor_id>/', advisor_book, name='advisor_book'),
    path('user/<int:user_id>/advisor/booking/', advisor_book_list, name='advisor_booking_list'),
    path('', index, name='index')
]
