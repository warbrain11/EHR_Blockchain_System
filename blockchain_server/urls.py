from django.contrib import admin
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from blockchain.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', Register_User_API),
    path('login/', obtain_auth_token),
]
