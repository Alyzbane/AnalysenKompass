from django.urls import path

from . import views

app_name = "surveys"


urlpatterns = [
    path('', views.survey_index, name='survey_index'),
    path('detail/<int:survey_id>/', views.survey_detail, name='survey_detail'),
    path('create/<int:survey_id>/', views.create_survey, name='survey_create'),
]
