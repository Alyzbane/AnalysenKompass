from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from polls.models import Poll
from surveys.models import Survey


@login_required
def vote_start(request, survey_id):
    survey = get_object_or_404(Survey, pk=survey_id)
    first_poll = Poll.objects.filter(survey=survey).first()

    context = {
       'survey': survey,
       'first_poll':  first_poll, 
    }

    return render(request, 'polls/vote/welcome.html', context)

@login_required
def vote_scroll(request, survey_id):
    survey = Survey.objects.get(pk=survey_id)
    polls = survey.poll_set.all()
    choices = {poll.id: poll.choice_set.all() for poll in polls}

    context = {
      'survey': survey,
      'polls': polls,
      'choices': choices,
    }

    return render(request, 'polls/vote/view_scroll.html', context)