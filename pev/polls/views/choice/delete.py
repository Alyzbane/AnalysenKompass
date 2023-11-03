from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse

from polls.forms import PollAddForm, ChoiceAddForm
from polls.models import Poll, Choice
from surveys.models import Survey
from common.utils.decorators import require_owner
   

@login_required
@require_owner(Choice, 'choice_id')
def choice_delete(request, choice_id):
    pass