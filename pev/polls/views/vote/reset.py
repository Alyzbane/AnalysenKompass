from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect

from polls.models import Vote
from common.utils.decorators import require_owner

@login_required
@require_owner(Vote, 'vote_id')
def vote_reset(request, vote_id):
    vote = get_object_or_404(Vote, pk=vote_id)
    poll_id = vote.poll.id

    if request.method == "POST":
        return HttpResponseRedirect(reverse("polls:add_vote", args={poll_id}))

    vote.delete()
    return redirect("polls:add_vote", poll_id)