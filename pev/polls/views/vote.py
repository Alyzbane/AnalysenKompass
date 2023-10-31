from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from polls.models import Poll, Choice, Vote
from surveys.models import Survey

@login_required
def vote_protocol(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)

    if request.method == "GET":
        polls_per_page = 1
        paginator = Paginator(polls, polls_per_page)
        page = request.GET.get('page')

        polls =  Survey.objects.get(id=poll.survey.id).get_polls()

        print(polls)

        try:
            polls_page = paginator.page(page)
        except PageNotAnInteger:     
            polls_page = paginator.page(1)
        except EmptyPage:
            polls_page = paginator.get_page(paginator.num_pages)

        context = {
            'polls_page':  polls_page,
        }

        return render(request, "polls/poll_detail.html", context)
    else:
        choice_id = request.POST.get('choice')
        HttpResponseForbidden(choice_id) 

