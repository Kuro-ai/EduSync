from django.urls import path 
from .views import request_count_api
urlpatterns = [
    path('request_count_api/', request_count_api),
]