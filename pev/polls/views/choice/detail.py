from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from polls.models import Poll
from common.utils.decorators import require_owner


@login_required
@require_owner(Poll, 'poll_id')
def choices_list(request, poll_id):
    if request.method == "GET":
        choices = Poll.get(pk=poll_id).choice_set.all()

        context = {
           'choices': choices,
        }

        return render(request, "polls/partials/list_choice.html", context)
