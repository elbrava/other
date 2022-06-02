from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path("calc",views.calc, name="calc"),
    path("operate",views.operate,name="operate"),
    path("record",views.record,name="record"),
    path("scav",views.scav,name="scav"),
    path("ii",views.ii,name="ii"),
]
