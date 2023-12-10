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
    path('detail/choices/<int:poll_id>/', views.choices_list, name="list_choice"),
    path('edit/choice/<int:choice_id>/', views.choice_edit, name="edit_choice"),
    path('delete/choice/<int:choice_id>/', views.choice_delete, name="delete_choice"),
    path('vote/start/<int:survey_id>/', views.vote_start, name="start_vote"),
    path('vote/view/scroll/<int:survey_id>/', views.vote_scroll, name="scroll_view"),
    path('vote/submit_choices/', views.submit_choices, name="submit_choices"),
    path('vote/view/page/<int:poll_id>/', views.vote_page,  name="page_view"),
    path('vote/submit_choice/<int:poll_id>/', views.submit_choice, name="submit_choice"),
    path('vote-edit/page/<int:vote_id>', views.vote_reset, name="reset_vote"),
    path('vote-edit/scroll/<int:survey_id>', views.scroll_reset, name="scroll_reset"),

    # Charts URLS
    path('result/<int:poll_id>/', views.poll_result, name='result_poll'),
    path('result-sex/<int:poll_id>/', views.poll_sex, name='result_sex'),

    # Table URLS
    path('results-sex-table/<int:poll_id>', views.sex_table, name='table_sex'),
    path('results-table/<int:poll_id>', views.result_table, name='table_result'),

    # Percent URLS
    path('result-percent/<int:poll_id>', views.poll_total_percent, name='percent_poll'),
    
]
