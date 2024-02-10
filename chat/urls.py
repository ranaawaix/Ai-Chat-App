from django.urls import path
from . import views

urlpatterns = [
    path('', views.CreateChatView.as_view(), name='index'),
]