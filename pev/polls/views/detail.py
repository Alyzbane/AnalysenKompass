from django.shortcuts import render, get_object_or_404

from polls.models import Poll

def poll_detail(request, poll_id):
    """
    Displaying the polls details

    Args:
        request (get) 
        poll_id (pk) 

    Returns:
        render: Poll summary
    """

    poll = get_object_or_404(Poll, id=poll_id)

    if not poll.active:
        return render(request, 'polls/poll_result.html', {'poll': poll})
    loop_count = poll.choice_set.count()
    context = {
        'poll': poll,
        'loop_time': range(0, loop_count),
    }
    return render(request, 'polls/poll_detail.html', context)
