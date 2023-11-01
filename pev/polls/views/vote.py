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
        messages.error(
            request, "You already voted this poll!", extra_tags='alert alert-warning alert-dismissible fade show')
    #    return redirect("surveys:survey_detail", poll.survey.pk)
        return HttpResponse("You already voted in this poll!")
    
    return render(request, "polls/poll_vote.html", {"poll": poll})

   
@login_required
def vote_protocol(request, poll_id):
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
    
    if request.method == "GET":
        polls =  Survey.objects.get(id=poll.survey.id)
        polls_per_page = 1
        paginator = Paginator(polls, polls_per_page)
        page = request.GET.get('page')

        try:
            polls_page = paginator.page(page)
        except PageNotAnInteger:     
            polls_page = paginator.page(1)
        except EmptyPage:
            polls_page = paginator.get_page(paginator.num_pages)
        
        print(polls_page.previous_page_number)
        context = {
            'polls_page':  polls_page,
        }
        
        render(request, "polls/partials/vote_poll.html", context)
