from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from polls.models import Poll, Choice
from common.utils.decorators import require_owner
   

decorators = [require_owner(Choice, 'choice_id'), login_required]
@login_required
@require_owner(Choice, 'choice_id')
def choice_delete(request, poll_id, choice_id):
    choice = get_object_or_404(Choice, pk=choice_id)

    if request.method == "POST":
        votes = choice.vote_set.all()
        votes.delete()
        choice.delete()
        return redirect('polls:edit_poll', poll_id)

    context = {
        'choice': choice,
        'poll_id': poll_id
    }
    return render(request, "polls/delete_choice.html", context)
