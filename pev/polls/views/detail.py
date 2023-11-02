from django.shortcuts import render, get_object_or_404

from polls.models import Poll

def poll_detail(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)

    loop_count = poll.choice_set.count()
    context = {
        'poll': poll,
        'loop_time': range(0, loop_count),
    }
    return render(request, 'polls/poll_detail.html', context)

def test(request):
    return render(request, 'polls/test.html')