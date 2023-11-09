from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Avg, Sum
from polls.models import Poll, Vote

from .forms import SurveyAddForm
from .models import Survey
from common.utils.decorators import require_owner
@login_required
def create_survey(request):
    if request.method == 'POST':
        form = SurveyAddForm(request.POST)
        if form.is_valid():
            survey = form.save(commit=False)
            survey.owner = request.user
            survey.save()
            return redirect('surveys:survey_index')
    else:
        return render(request, 'surveys/create.html', {'form': SurveyAddForm})

@login_required()
def survey_detail(request, survey_id):
    survey = get_object_or_404(Survey, pk=survey_id)
    polls = Poll.objects.filter(survey=survey)

    context = {
        'survey': survey,
        'polls': polls,
    }
    return render(request, 'surveys/detail.html', context)

@login_required()
def survey_index(request):
    if request.method == "POST":
        pass

    surveys = Survey.objects.all()
    context = {
        'surveys': surveys,
    }
    return render(request, 'surveys/index.html', context)

@login_required
@require_owner(Survey, 'survey_id')
def survey_end(request, survey_id):
    survey = get_object_or_404(Survey, pk=survey_id)
    
    survey.active = not survey.active
    survey.save()
    
    context = {
        'survey': survey,
        'polls': survey.poll_set.all(),
    }
       
    return render(request, 'surveys/end.html', context)


@login_required
@require_owner(Survey, 'survey_id')
def survey_edit(request, survey_id):
    survey = get_object_or_404(Survey, pk=survey_id)
    if request.method == "POST":
        form = SurveyAddForm(request.POST, instance=survey)
        if form.is_valid():
            survey.save()
            return redirect('surveys:survey_detail', survey_id=survey.pk)
    else:
        form = SurveyAddForm(instance=survey)
        return render(request, 'surveys/edit.html', {'form': form})


@login_required
@require_owner(Survey, 'survey_id')
def survey_delete(request, survey_id):
    survey = get_object_or_404(Survey, pk=survey_id)
    votes = Vote.objects.filter(survey=survey)

    votes.delete()
    survey.delete()

    return redirect("surveys:survey_index")


@login_required
def survey_report(request):
    return render(request, 'chart.html')

@login_required
def survey_chart(request, survey_id):
    survey = get_object_or_404(Survey, pk=survey_id)

    labels = []
    data = []
    
    queryset = Vote.objects.filter(survey=survey)
    