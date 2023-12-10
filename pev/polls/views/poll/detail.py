from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from django.http import HttpResponse

from plotly.offline import plot
import plotly.graph_objs as go
import pandas as pd
from polls.models import Poll, Vote

def poll_detail(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)

    loop_count = poll.choice_set.count()
    context = {
        'poll': poll,
        'loop_time': range(0, loop_count),
    }
    return render(request, 'polls/poll/detail.html', context)

    
### Chart Functions Displays
@login_required
@require_GET
def poll_result(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
   
    # Define the raw datas for display
    # todo: add a filtering or additional template for charts
    votes_data = Vote.get_plot_dict(poll_id)
    labels, data = zip(*votes_data)

    # Define the data in othe chart
    fig = go.Figure(
        data=[go.Bar(x=labels, y=data)],
        layout_title_text="Whole Data Graph",
    )

    fig.update_yaxes(tickformat=",d", dtick=1)
    fig.update_layout(
        autosize=False,
        yaxis_title="Choice",
        xaxis_title="Frequency",
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
@require_GET
def poll_sex(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
   
    # Define the raw datas for display
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
        title_text = "Sex Data Graph",
        xaxis_title="Choice",
        yaxis_title="Frequency",
        autosize=False,
    )

    chart = plot(
        fig,
        output_type='div',
        include_plotlyjs=False,
        show_link=False,
        link_text="",
     )

    return HttpResponse(chart)



### Table Functions Displays
@login_required
@require_GET
def sex_table(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
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
    table = table.update_layout(
        title_text=f"Sex Data Summary",
        autosize=False,)
    # Convert the figure to a div string and return it
    table_div = plot(table,
                      output_type='div',
                      link_text="")

    return HttpResponse(table_div)

@login_required
@require_GET
def result_table(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
   
    # Define the raw datas for display
    votes_data = Vote.get_plot_dict(poll_id)
    labels, data = zip(*votes_data)

    vote_df = pd.DataFrame({'Choice': labels, 'Frequency': data})

    vote_stats = vote_df.describe()

    # Create Plotly Table for male and female statistics
    table = go.Figure(data=[go.Table(
        header=dict(
            values=['Statistic', 'Data'],
            font=dict(size=16),
            align="left",
            height=32
        ),
        cells=dict(
            values=[
                vote_stats.index,  # statistics names
                vote_stats['Frequency']  # female statistics
            ],
            font=dict(size=12),
            align=["left", "right"],
            height=24
        )
    )])
    table = table.update_layout(
        autosize=False,
        title_text=f"Whole Data Summary",)
    # Convert the figure to a div string and return it
    table_div = plot(table,
                      output_type='div',
                      link_text="")

    return HttpResponse(table_div)


@login_required
def age_group_boxplot(request, poll_id):
    # Define age groups
    age_groups = {
        'Young Adult': range(18, 25),
        'Adult': range(25, 50),
        'Senior': range(50, 120)
    }

    # Create a DataFrame to store the data
    df = pd.DataFrame(columns=['group', 'votes'])

    for group, ages in age_groups.items():
        # Get vote counts for each choice
        votes = Vote.get_plot_dict(poll_id, min_age=min(ages), max_age=max(ages))
        for label, freq in votes:
            temp_df = pd.DataFrame({'group': [group]*freq, 'votes': range(freq)})
            df = pd.concat([df, temp_df], ignore_index=True)

    # Create a box plot of the vote counts for each age group
    data = [go.Box(y=df[df['group'] == group]['votes'], name=group) for group in age_groups.keys()]
    layout = go.Layout(title='Vote Counts by Age Group', xaxis=dict(title='Age Group'), yaxis=dict(title='Votes'))
    fig = go.Figure(data=data, layout=layout)

    # Convert the figure to a div string and return it
    div_string = plot(fig, output_type='div')
    return HttpResponse(div_string)


## Valid Percent
@login_required
@require_GET
def poll_total_percent(request, poll_id):
    votes_data = Vote.get_plot_dict(poll_id)
    labels, data = zip(*votes_data)

    vote_df = pd.DataFrame({'choice': labels, 'frequency': data})

    total_responses = vote_df['frequency'].sum()
    vote_df['valid_percent'] = (vote_df['frequency'] / total_responses) * 100

    # Create Plotly Table for male and female statistics
    table = go.Figure(data=[go.Table(
        header=dict(
            values=['', 'N', 'Valid Percent'],
            font=dict(size=16),
            align="left",
            height=32
        ),
        cells=dict(
            values=[
                vote_df['choice'],
                vote_df['frequency'],
                vote_df['valid_percent'],
            ],
            font=dict(size=12),
            align=["left", "right"],
            height=24
        )
    )])
    table = table.update_layout(
        autosize=False,
        title_text="Whole Data Summary",)
    # Convert the figure to a div string and return it
    table_div = plot(table,
                      output_type='div',
                      link_text="")

    return HttpResponse(table_div)

