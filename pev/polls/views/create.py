from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse

from polls.forms import PollAddForm, ChoiceAddForm
from polls.models import Poll
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

