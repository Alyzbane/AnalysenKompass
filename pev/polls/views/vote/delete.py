from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse

from polls.models import Poll, Choice, Vote
from surveys.models import Survey
from common.utils.decorators import require_owner

@login_required
@require_owner(Vote, 'vote_id')
def vote_edit(request, vote_id):
    vote = get_object_or_404(Vote, pk=vote_id)
    poll_id = vote.poll.id

    if request.method == "POST":
        return redirect("polls:add_vote", poll_id)

    vote.delete()
    return redirect("polls:add_vote", poll_id)