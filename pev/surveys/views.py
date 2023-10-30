from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpResponseForbidden
from functools import wraps

from polls.models import Poll

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
   
    if survey.active is True:
        survey.active = False
        survey.save()
    
    context = {
        'survey': survey,
        'polls': survey__poll,
    }
       
    return render(request, 'surveys/end.html', context)


@login_required
@require_owner(Survey, 'survey_id')
def survey_edit(request, survey_id):
    survey = get_object_or_404(Survey, pk=survey_id)
    if survey.active and request.method == "POST":
        form = SurveyAddForm(request.POST, instance=survey)
        if form.is_valid():
            survey.save()
            return redirect('surveys:survey_detail', survey_id=survey.pk)
    elif survey.active:
        form = SurveyAddForm(instance=survey)
        return render(request, 'surveys/edit.html', {'form': form})
    else:
        return render(request, 'surveys/end.html', {'survey': survey})






@login_required()
def polls_list(request):
    all_surveys = Survey.objects.all()
    context = {
        'surveys': all_surveys,
    }
    return render(request, 'polls/polls_list.html', context)

@login_required()
def list_by_user(request):
    all_surveys = Survey.objects.filter(owner=request.user)
    paginator = Paginator(all_surveys, 7)  # Show 7 contacts per page

    page = request.GET.get('page')
    survey = paginator.get_page(page)

    context = {
        '': surveys,
    }
    return render(request, 'polls/polls_list.html', context)