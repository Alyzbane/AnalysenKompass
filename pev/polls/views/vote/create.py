from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


from polls.models import Poll, Choice, Vote
from surveys.models import Survey

@login_required
def poll_vote(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if not poll.user_can_vote(request.user):
    #    return redirect("polls:detail_poll", )
        return HttpResponse("TANGA")

    poll = Poll.objects.get(pk=poll_id)
    if request.method == "POST":
        try:
            choice = poll.choice_set.get(pk=request.POST.get('choice'))
        except (KeyError, Choice.DoesNotExist):
            messages.error(request, "You already voted this poll!", extra_tags='alert alert-warning alert-dismissible fade show')
            context = {
                "poll": poll,
                "messages": messages,
            }
            return render(request, "polls/poll_detail", context)
        else: 
            vote = Vote(user=request.user, survey=poll.survey, poll=poll, choice=choice)
            vote.save()
            return HttpResponse(Vote.objects.get(pk=vote.id)) 

    return render(request, "polls/poll_vote.html", {"poll": poll})

   
@login_required
def vote_protocol(request, poll_id):
    if request.method == "GET":
        poll = get_object_or_404(Poll, pk=poll_id)
        related_polls = Poll.objects.filter(survey=poll.survey)
        polls_per_page = 1
        paginator = Paginator(related_polls, polls_per_page)
        page = request.GET.get('page')

        try:
            polls_page = paginator.page(page)
        except PageNotAnInteger:
            polls_page = paginator.page(1)
        except EmptyPage:
            polls_page = paginator.get_page(paginator.num_pages)

        context = {
            'poll': poll,
            'polls_page': polls_page,
        }

        return render(request, "polls/partials/vote_poll.html", context)