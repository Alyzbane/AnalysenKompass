from django.urls import path

from . import views

app_name = "polls"

urlpatterns = [
    path("", views.test, name="test"),
    path('<int:poll_id>/', views.poll_detail, name='detail'),
    path('list/', views.polls_list, name='list'), 
    path("add-poll/<int:survey_id>/", views.polls_add, name="add_poll"),
    path('add-choice/<int:poll_id>/', views.create_choice, name='add_choice'),
    path("edit-poll/<int:poll_id>/", views.polls_edit, name="edit_poll"),

]
