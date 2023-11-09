from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect

from common.utils.decorators import require_owner
from polls.forms import PollEditForm
from polls.models import Poll


@login_required
@require_owner(Poll, 'poll_id')
def polls_edit(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
     
    if request.method == 'POST':
        form = PollEditForm(request.POST, instance=poll)
        if form.is_valid():
            form.save()
            messages.success(request, "Poll Updated successfully.",
                             extra_tags='alert alert-success alert-dismissible fade show')
            return HttpResponseRedirect(reverse("polls:detail", args={poll.pk}))

    else:
        form = PollEditForm(instance=poll)

    return render(request, "polls/poll_edit.html", {'form': form, 'poll': poll})

