from django.urls import path
from .views import *
urlpatterns = [
    path('', index, name='cities-page'),
    path('<int:id>/', get_city_by_id, name='city-detail'),
    path('/delete/<int:id>', delete, name='city-delete')
]
