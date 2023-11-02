from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from common.utils.decorators import require_owner

from polls.forms import PollAddForm, ChoiceAddForm, PollEditForm, ChoiceEditForm
from polls.models import Poll, Choice, Vote


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
            return redirect("polls:detail", poll_id=poll.pk)

    else:
        form = PollEditForm(instance=poll)

    return render(request, "polls/poll_edit.html", {'form': form, 'poll': poll})


@login_required
@require_owner(Choice, 'choice_id')
def choice_edit(request, choice_id):
    choice = get_object_or_404(Choice, pk=choice_id)
     
    if request.method == 'POST':
        form = ChoiceEditForm(request.POST, instance=choice)
        if form.is_valid():
            form.save()
            messages.success(request, "Poll Updated successfully.",
                             extra_tags='alert alert-success alert-dismissible fade show')
            return redirect("polls:detail", choice_id=choice.pk)

    else:
        form = PollEditForm(instance=)
        return HttpResponse(form)

    return render(request, "polls/poll_edit.html", {'form': form, 'poll': poll})
