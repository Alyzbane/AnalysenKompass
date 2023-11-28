from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.html import format_html

from plotly.offline import plot
import plotly.graph_objs as go

from polls.models import Poll, Vote

def poll_detail(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)

    loop_count = poll.choice_set.count()
    context = {
        'poll': poll,
        'loop_time': range(0, loop_count),
    }
    return render(request, 'polls/poll/detail.html', context)

    
@login_required
def poll_result(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
   
    # Define the raw datas for display
    votes_data = Vote.get_plot_dic(poll_id)
    labels, data = zip(*votes_data)

    # Define the data in othe chart
    fig = go.Figure(
        data=[go.Bar(x=labels, y=data)],
        layout_title_text=poll.text,
    )

    fig.update_yaxes(tickformat=",d", dtick=1)


    chart = plot(
        fig,
        output_type='div',
        include_plotlyjs=False,
        show_link=False,
        link_text="",
     ) 

    return HttpResponse(chart)