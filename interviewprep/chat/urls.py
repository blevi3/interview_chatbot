from django.urls import path
from . import views

urlpatterns = [
    path('accounts/register/', views.register_request, name='register'),

    path('', views.chat_api, name='index'),
    path('api/chat/', views.chat_api, name='chat_api'),
]
