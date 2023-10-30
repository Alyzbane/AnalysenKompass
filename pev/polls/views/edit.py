from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden

from polls.forms import PollAddForm, ChoiceAddForm, PollEditForm
from polls.models import Poll, Choice, Vote

@login_required
def polls_edit(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if request.user != poll.survey.owner:
        return redirect('home')

    if request.method == 'POST':
        form = PollEditForm(request.POST, instance=poll)
        if form.is_valid:
            form.save()
            messages.success(request, "Poll Updated successfully.",
                             extra_tags='alert alert-success alert-dismissible fade show')
            return redirect("polls:detail", poll_id=poll.pk)

    else:
        form = PollEditForm(instance=poll)

    return render(request, "polls/poll_edit.html", {'form': form, 'poll': poll})
