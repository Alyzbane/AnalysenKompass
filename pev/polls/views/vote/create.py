from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse

from polls.models import Poll, Choice, Vote
from surveys.models import Survey

@login_required
def poll_vote(request, poll_id):

    poll = get_object_or_404(Poll, pk=poll_id)
    polls = Poll.objects.filter(survey=poll.survey)
    current_poll_number = list(polls).index(poll) + 1

    user_voted = Vote.objects.filter(user=request.user, poll=poll).first()
    selected_choice_id = user_voted.choice.id if user_voted else None
    is_active = poll.survey.active

    context =  {
        "poll": poll,
        "polls": polls,
        "current_poll_number": current_poll_number,
        "selected_choice_id": selected_choice_id,
        "vote": user_voted,
        "is_active": is_active,
    }

    if not poll.user_can_vote(request.user):
        return render(request, "polls/poll_vote.html", context)

    if is_active and request.method == "POST":
        try:
            choice = poll.choice_set.get(pk=request.POST.get('choice'))
        except (KeyError, Choice.DoesNotExist):
            messages.error(request, "You already voted this poll!", extra_tags='alert alert-warning alert-dismissible fade show')
            context = {
                "poll": poll,
                "messages": messages,
            }
            return redirect("polls:add_vote", poll.id)
        else: 
            vote = Vote(user=request.user, survey=poll.survey, poll=poll, choice=choice)
            vote.save()
            return redirect("polls:add_vote", poll.id)
    else: 
        return render(request, "polls/poll_vote.html", context)
