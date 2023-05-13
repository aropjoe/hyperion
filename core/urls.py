from django.urls import path
from .views import dataset_list, data_view

urlpatterns = [
    path('datasets/', dataset_list, name='dataset_list'),
    path('data/', data_view, name='data_view'),
]
