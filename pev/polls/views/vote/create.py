from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden

from polls.models import Poll, Choice, Vote

@login_required
@require_POST
def submit_choice(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)

    if not poll.user_can_vote(request.user):
        return HttpResponseForbidden("You cannot vote again")

    if poll.survey.active:
        try:
            choice = poll.choice_set.get(pk=request.POST.get('choice'))
        except (KeyError, Choice.DoesNotExist):
            context = {
                "poll": poll,
            }
            return redirect("polls:page_view", poll.id)
        else:
            vote = Vote(user=request.user, survey=poll.survey, poll=poll, choice=choice)
            vote.save()
            return HttpResponseRedirect(reverse("polls:page_view", args={poll.id}))


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
        poll = Poll.objects.get(pk=poll_id)
        vote = Vote(user=request.user, survey=poll.survey, poll_id=poll_id, choice_id=choice_id)
        vote.save()

        selected_choices_data.append({
            'poll_id': poll_id,
            'choice_id': choice_id,
        })

    # return HttpResponseRediret(reverse('survey:end_thanks'))
    # Return the data in JsonResponse
    #return JsonResponse({'message': 'Choices submitted successfully', 'selected_choices': selected_choices_data})
    return redirect("surveys:complete_survey")
