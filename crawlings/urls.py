from django.urls import path, include
from . import views


app_name = 'crawlings'

urlpatterns = [
    path('', views.index, name='index'),
]