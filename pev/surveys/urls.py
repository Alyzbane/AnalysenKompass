from django.urls import path

from . import views

app_name = "surveys"


urlpatterns = [
    path('', views.SurveyListView.as_view(), name='survey_index'),
    path('detail/<int:survey_id>/', views.survey_detail, name='survey_detail'),
    path('create/', views.create_survey, name='survey_create'),
    path('end/<int:survey_id>/', views.survey_end, name='survey_end'), 
    path('delete/<int:survey_id>/', views.survey_delete, name='survey_delete'),
    path('edit/<int:survey_id>/', views.survey_edit, name='survey_edit'),

]