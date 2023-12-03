from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.html import format_html

from plotly.offline import plot
from plotly.subplots import make_subplots
import pandas as pd
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
    # todo: add a filtering or additional template for charts
    votes_data = Vote.get_plot_dict(poll_id)
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


@login_required
def poll_sex(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
   
    # Define the raw datas for display
    # todo: add a filtering or additional template for charts
    male_votes = Vote.get_plot_dict(poll_id, sex='M')
    female_votes = Vote.get_plot_dict(poll_id, sex='F')

    male_labels, male_data = zip(*male_votes)
    female_labels, female_data = zip(*female_votes) 

     # Define the data in othe chart
    fig = go.Figure(data=[
        go.Bar(name="Male", x=male_labels, y=male_data),
        go.Bar(name="Female", x=female_labels, y=female_data),
    ],)
    fig.update_yaxes(tickformat=",d", dtick=1)

    fig.update_layout(
        title_text = poll.text,
        xaxis_title="Choice",
        yaxis_title="Frequency",
    )

    chart = plot(
        fig,
        output_type='div',
        include_plotlyjs=False,
        show_link=False,
        link_text="",
     )

    return HttpResponse(chart)

@login_required
def sex_table(request, poll_id):
    # Define the raw datas for display
    male_votes = Vote.get_plot_dict(poll_id, sex='M')
    female_votes = Vote.get_plot_dict(poll_id, sex='F')

    male_labels, male_data = zip(*male_votes)
    female_labels, female_data = zip(*female_votes) 

    # Create pandas DataFrames for male and female data
    male_df = pd.DataFrame({'Choice': male_labels, 'Frequency': male_data})
    female_df = pd.DataFrame({'Choice': female_labels, 'Frequency': female_data})

    # Calculate statistics for male and female data
    male_stats = male_df.describe()
    female_stats = female_df.describe()

    # Create Plotly Table for male and female statistics
    table = go.Figure(data=[go.Table(
        header=dict(
            values=['Statistic', 'Male', 'Female'],
            font=dict(size=16),
            align="left",
            height=32
        ),
        cells=dict(
            values=[
                male_stats.index,  # statistics names
                male_stats['Frequency'],  # male statistics
                female_stats['Frequency']  # female statistics
            ],
            font=dict(size=12),
            align=["left", "right", "right"],
            height=24
        )
    )])

    # Convert the figure to a div string and return it
    table_div = plot(table,
                      output_type='div',
                      link_text="")

    return HttpResponse(table_div)



@login_required
def poll_age(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)

    # Define the raw datas for display
    # todo: add a filtering or additional template for charts
    votes_data = Vote.get_plot_dict(poll_id)
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