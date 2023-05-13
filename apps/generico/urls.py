from django.urls import path
from apps.generico.views import *

urlpatterns = [
    path('', index, name='index'),
    path('about', about, name='about')
]