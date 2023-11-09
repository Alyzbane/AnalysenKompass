from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from polls.forms import ChoiceAddForm
from polls.models import Poll
from common.utils.decorators import require_owner


@login_required
@require_owner(Poll, 'poll_id')
def create_choice(request, poll_id):
    choice_form = ChoiceAddForm(prefix="choice")
    poll = get_object_or_404(Poll, pk=poll_id)
    context = {
        'choice_form': choice_form,
        'poll': poll,
        'choices': poll.choice_set.all(),
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

    context = {
        'choice_form': choice_form,
        'poll': poll,
    }

    return render(request, 'polls/partials/choice_form.html', context)