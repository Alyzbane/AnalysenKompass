from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse

from polls.models import Poll, Choice, Vote

@login_required
def poll_vote(request, poll_id):

    poll = get_object_or_404(Poll, pk=poll_id)
    polls = Poll.objects.filter(survey=poll.survey)

    # get the data for dropdown navigation
    current_poll_number = list(polls).index(poll) + 1
    user_voted = Vote.objects.filter(user=request.user, poll=poll).first()
    selected_choice_id = user_voted.choice.id if user_voted else None
    next_poll_id = Poll.get_next_poll(poll.survey.id, poll.id)
    previous_poll_id = Poll.get_previous_poll(poll.survey.id, poll.id)

    is_active = poll.survey.active 

    context =  {
        "survey": poll.survey,
        "poll": poll,
        "polls": polls,
        "current_poll_number": current_poll_number,
        "selected_choice_id": selected_choice_id,
        "vote": user_voted,
        "is_active": is_active,
        "previous_poll_id": previous_poll_id,
        "next_poll_id": next_poll_id,
    }

    if not poll.user_can_vote(request.user):
        return render(request, "polls/vote/view_page.html", context)

    if is_active and request.method == "POST":
        try:
            choice = poll.choice_set.get(pk=request.POST.get('choice'))
        except (KeyError, Choice.DoesNotExist):
            context = {
                "poll": poll,
            }
            return redirect("polls:add_vote", poll.id)
        else: 
            vote = Vote(user=request.user, survey=poll.survey, poll=poll, choice=choice)
            vote.save()
            return HttpResponseRedirect(reverse("polls:add_vote", args={poll.id}))
    else: 
        return render(request, "polls/vote/view_page.html", context)



@login_required
@require_POST
def submit_choices(request):
    poll_ids = request.POST.getlist('poll_ids[]')

    selected_choices = {}
    for poll_id in poll_ids:
        selected_choices[poll_id] = request.POST.get(f'poll_{poll_id}')

    # Process and save the selected choices as needed

    # Fetch choice data based on selected choice IDs
    selected_choices_data = []
    for poll_id, choice_id in selected_choices.items():
        choice = Choice.objects.get(pk=choice_id)
        selected_choices_data.append({
            'poll_id': poll_id,
            'choice_id': choice_id,
            'choice_text': choice.text,
        })

    # Return the data in JsonResponse
    return JsonResponse({'message': 'Choices submitted successfully', 'selected_choices': selected_choices_data})