
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('adminUser',admin.site.urls),
    path('',include('api.urls'))
]
