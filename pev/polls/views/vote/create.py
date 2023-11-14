from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect

from polls.models import Poll, Choice, Vote
from surveys.models import Survey

@login_required
def poll_vote(request, poll_id):

    poll = get_object_or_404(Poll, pk=poll_id)
    polls = Poll.objects.filter(survey=poll.survey)

    # get the data for dropdown navigation
    current_poll_number = list(polls).index(poll) + 1
    user_voted = Vote.objects.filter(user=request.user, poll=poll).first()
    selected_choice_id = user_voted.choice.id if user_voted else None
    next_poll_id = Poll.get_next_poll(poll.survey.id, poll.id)
    previous_poll_id = Poll.get_previous_poll(poll.survey.id, poll.id)

    is_active = poll.survey.active 

    context =  {
        "poll": poll,
        "polls": polls,
        "current_poll_number": current_poll_number,
        "selected_choice_id": selected_choice_id,
        "vote": user_voted,
        "is_active": is_active,
        "previous_poll_id": previous_poll_id,
        "next_poll_id": next_poll_id,
    }

    if not poll.user_can_vote(request.user):
        return render(request, "polls/vote/add.html", context)

    if is_active and request.method == "POST":
        try:
            choice = poll.choice_set.get(pk=request.POST.get('choice'))
        except (KeyError, Choice.DoesNotExist):
            context = {
                "poll": poll,
            }
            return redirect("polls:add_vote", poll.id)
        else: 
            vote = Vote(user=request.user, survey=poll.survey, poll=poll, choice=choice)
            vote.save()
            return HttpResponseRedirect(reverse("polls:add_vote", args={poll.id}))
    else: 
        return render(request, "polls/vote/add.html", context)
