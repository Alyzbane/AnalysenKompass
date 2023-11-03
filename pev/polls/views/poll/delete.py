from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse

from polls.forms import PollAddForm, ChoiceAddForm
from polls.models import Poll, Choice
from surveys.models import Survey
from common.utils.decorators import require_owner


@login_required
@require_owner(Poll, 'poll_id')
def poll_delete(request, poll_id):
   poll = get_object_or_404(Poll, pk=poll_id) 

   if request.method == "POST":
       survey_id = poll.survey.id
       poll.delete()
       return redirect("surveys:survey_detail", survey_id)
   
   return render(request, "polls/delete_poll.html", {"poll": poll})