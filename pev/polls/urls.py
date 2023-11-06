from django.urls import path

from . import views

app_name = "polls"

urlpatterns = [
    path('<int:poll_id>/', views.poll_detail, name='detail'),
    path('list/', views.polls_list, name='list'), 
    path("add-poll/<int:survey_id>/", views.polls_add, name="add_poll"),
    path('delete/<int:poll_id>', views.poll_delete, name="delete_poll"),
    path("edit/<int:poll_id>/", views.polls_edit, name="edit_poll"),
    path('add-choice/<int:poll_id>/', views.create_choice, name='add_choice'),
    path('add-choice-clone/<int:poll_id>/', views.choice_protocol,  name="protocol_choice"),
    path('edit/choice/<int:choice_id>/', views.choice_edit, name="edit_choice"),
    path('<int:poll_id>/delete/choice/<int:choice_id>/', views.choice_delete, name="delete_choice"),
    path('vote/<int:poll_id>/', views.poll_vote,  name="add_vote"),
    path('vote-edit/<int:vote_id>', views.vote_edit, name="edit_vote"),
]
