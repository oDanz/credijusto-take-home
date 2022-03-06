from django.urls import path
from rest_framework.authtoken import views as auth_views
from . import views

app_name = 'rates'

urlpatterns = [
    path('', views.RatesListView.as_view(), name='rates_list'),
    path('account/register/', views.UserCreateView.as_view(), name='user_create'),
    path('token/', auth_views.obtain_auth_token),
]
