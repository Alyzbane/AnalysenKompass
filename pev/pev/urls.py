
from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("admin/", admin.site.urls),
    path("accounts/", include('accounts.urls', namespace="accounts")),   
    path("surveys/", include('surveys.urls', namespace="surveys")),   
    path("polls/", include('polls.urls', namespace="polls")),
]
