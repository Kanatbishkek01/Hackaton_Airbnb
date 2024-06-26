from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from .views import *

urlpatterns = [
    path('register/',RegisterView.as_view()),
    path('activate/<str:email>/<str:activation_code>',ActivateView.as_view(),name='activate'),
    path('login/',TokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('refresh/',TokenRefreshView.as_view(),name='token_refresh'),
    path('change-password/', ChangePasswordView.as_view()),
    path('forgot-password/', ForgotPasswordView.as_view())

]