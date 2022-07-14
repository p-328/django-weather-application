from django.urls import path
from .views import *
urlpatterns = [
    path('', index, name='login-screen'),
    path('create/', create_user, name='creation'),
    path('logout/', logout_controller, name='logout-action')
]
