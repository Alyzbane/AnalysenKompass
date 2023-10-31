from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from polls.forms import PollAddForm, ChoiceAddForm
from polls.models import Poll, Choice, Vote
from surveys.models import Survey
from common.utils.decorators import require_owner


@login_required()
@require_owner(Survey, 'survey_id')
def polls_add(request, survey_id):
    survey = get_object_or_404(Survey, pk=survey_id)
    if request.method == 'POST':
        form = PollAddForm(request.POST)

        if form.is_valid():
            poll = form.save(commit=False)
            poll.survey = survey
            poll.save()

            messages.success(
                request, "Poll added successfully.",
                extra_tags='alert alert-success alert-dismissible fade show')
            return redirect('polls:add_choice', poll.id)
    else:
        form = PollAddForm()

    context = {
        'form': form,
        'survey': survey,
    }

    return render(request, 'polls/add_poll.html', context)

@login_required
@require_owner(Poll, 'poll_id')
def create_choice(request, poll_id):
    choice_form = ChoiceAddForm(prefix="choice")
    poll = get_object_or_404(Poll, pk=poll_id)
    context = {
        'choice_form': choice_form,
             'poll': poll,
    }

    return render(request, 'polls/add_choice.html', context)


@login_required
@require_owner(Poll, 'poll_id')
def choice_protocol(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    choice_form = ChoiceAddForm(prefix="choice")

    if request.method == "POST":
        choice_form = ChoiceAddForm(request.POST, prefix="choice")

        if choice_form.is_valid():
            choice = choice_form.save(commit=False)
            choice.poll = poll
            choice.save()

            messages.success(
                request, "Choice added successfully.",
                extra_tags='alert alert-success alert-dismissible fade show')
            return redirect('polls:detail', poll_id=poll.id)

    context = {
        'choice_form': choice_form,
            'poll': poll,
    }

    return render(request, 'polls/partials/choice_form.html', context)