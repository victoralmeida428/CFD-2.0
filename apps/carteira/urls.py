from django.urls import path
from apps.carteira.views import FormCarteira, dash

urlpatterns=[
    path('despesa', FormCarteira.as_view(), name='despesa'),
    path('dash', dash, name='dash'),
]