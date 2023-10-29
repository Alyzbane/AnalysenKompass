from django.urls import path

from . import views

app_name = "polls"

urlpatterns = [
    path('<int:poll_id>/', views.poll_detail, name='detail'),
    path('list/', views.polls_list, name='list'), 
    path("add/", views.polls_add, name="add"),
    path('add-choice-form/', views.add_choice_form, name='add_choice_form'),
]
