from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from polls.models import Poll, Vote
from surveys.models import Survey


@login_required
def vote_start(request, survey_id):
    survey = get_object_or_404(Survey, pk=survey_id)
    if not survey.active:
        return render(request, 'polls/vote/end.html')

    first_poll = Poll.objects.filter(survey=survey).first()

    context = {
       'survey': survey,
       'first_poll':  first_poll,
    }

    return render(request, 'polls/vote/welcome.html', context)


@login_required
def vote_page(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    polls = Poll.objects.filter(survey=poll.survey)
    # get the data for dropdown navigation
    current_poll_number = list(polls).index(poll) + 1
    user_voted = Vote.objects.filter(user=request.user, poll=poll).first()
    selected_choice_id = user_voted.choice.id if user_voted else None
    next_poll_id = Poll.get_next_poll(poll.survey.id, poll.id)
    previous_poll_id = Poll.get_previous_poll(poll.survey.id, poll.id)
    
    is_active = poll.survey.active
    is_survey_completed= Vote.survey_complete(request.user, poll.survey.pk)

    context =  {
        "survey": poll.survey,
        "poll": poll,
        "polls": polls,
        "current_poll_number": current_poll_number,
        "selected_choice_id": selected_choice_id,
        "vote": user_voted,
        "is_active": is_active,
        "previous_poll_id": previous_poll_id,
        "next_poll_id": next_poll_id,
        "is_survey_completed": is_survey_completed,
    }

    return render(request, "polls/vote/view_page.html", context)

@login_required
def vote_scroll(request, survey_id):
    survey = Survey.objects.get(pk=survey_id)
    polls = survey.poll_set.all()
    choices = {poll.id: poll.choice_set.all() for poll in polls}

    # Identifiyng the existing choice_id in Vote table
    selected_choices = Vote.objects.filter(user=request.user, survey_id=survey_id).values('choice_id')
    selected_choices = selected_choices.values_list('choice_id', flat=True)

    is_active = survey.active
    is_survey_completed= Vote.survey_complete(request.user, survey_id)

    context = {
      'survey': survey,
      'polls': polls,
      'choices': choices,
      'is_valid': True if selected_choices.count() > 0 else False,
      'selected_choices': selected_choices,
      'is_active': is_active,
      'is_survey_completed': is_survey_completed,
    }

    return render(request, 'polls/vote/view_scroll.html', context)

