
from django.contrib import admin
from django.urls import path
from codes import views

urlpatterns = [
    path("",views.veri, name="veri"),
]
