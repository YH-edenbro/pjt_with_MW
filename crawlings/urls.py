from django.urls import path
from . import views


app_name = 'crawlings'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:comment_pk>/delete_comment/', views.delete_comment, name='delete_comment'),
    path('search/', views.search, name='search'),
]