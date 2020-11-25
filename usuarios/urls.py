from django.urls import path
from django.conf.urls import url
from . import views
from rest_framework.authtoken import views as authtoken_views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('change_password/', views.change_password, name='change_password'),
    # ----------------------------------------------------------------------
    # API REST URLs --------------------------------------------------------
    # ----------------------------------------------------------------------
    url('api-token-auth/', authtoken_views.obtain_auth_token),
]
