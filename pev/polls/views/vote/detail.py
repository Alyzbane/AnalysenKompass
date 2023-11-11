from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import plotly.express as px
from polls.models import Poll, Vote
from surveys.models import Survey


@login_required
def vote_start(request, survey_id):
    survey = get_object_or_404(Survey, pk=survey_id)
    first_poll = Poll.objects.filter(survey=survey).first()

    context = {
       'survey': survey,
       'first_poll':  first_poll, 
    }

    return render(request, 'polls/start_vote.html', context)

@login_required
def vote_bar_chart(request, poll_id):
   poll = get_object_or_404(Poll, pk=poll_id)
   
   # Define the raw datas for display
   votes_data = Vote.get_plot_dic(poll_id)
   labels, counts = zip(*votes_data)

   # Define the data in othe chart
   fig = px.bar(x=labels, y=counts)
   fig.update_layout(title_text=f"{poll.text}")

   bar_chart = fig.to_html()

   context = {
      'bar_chart': bar_chart,
   }

   return render(request, 'polls/partials/vote_result.html', context)

