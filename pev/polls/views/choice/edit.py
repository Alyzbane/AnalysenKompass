from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from polls.forms.choice_edit import ChoiceEditForm
from polls.models import Choice
from common.utils.decorators import require_owner


@login_required
@require_owner(Choice, 'choice_id')
def choice_edit(request, choice_id):
    choice = get_object_or_404(Choice, pk=choice_id)
     
    if request.method == 'POST':
        form = ChoiceEditForm(request.POST, instance=choice)
        if form.is_valid():
            form.save()
            return redirect("polls:edit_poll", poll_id=choice.poll.pk)
    else:
        form = ChoiceEditForm(instance=choice)
        context = {
            'form': form,
            'choice': choice
        }
        return render(request, "polls/edit_choice.html", context)
