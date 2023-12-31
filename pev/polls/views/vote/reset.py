from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden

from polls.models import Vote
from common.utils.decorators import require_owner

@login_required
@require_owner(Vote, 'vote_id')
def vote_reset(request, vote_id):
    vote = get_object_or_404(Vote, pk=vote_id)
    poll_id = vote.poll.id

    if request.method == "POST":
        return HttpResponseRedirect(reverse("polls:page_view", args={poll_id}))

    vote.delete()
    return redirect("polls:page_view", poll_id)


@login_required
def scroll_reset(request, survey_id):
    vote = Vote.objects.filter(user=request.user, survey_id=survey_id)
    if vote is None:
        return HttpResponseForbidden("Error: You cannot do that")

    if request.user != vote.first().user:
        return HttpResponseForbidden("You don't have permission to do this!")     

    if request.method == "POST":
        return HttpResponseRedirect(reverse('polls:scroll_view', args={survey_id}))

    vote.delete()
    return redirect("polls:scroll_view", survey_id)