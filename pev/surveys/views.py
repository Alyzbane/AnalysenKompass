from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count

from polls.models import Poll

from .forms import SurveyAddForm
from .models import Survey

def survey_list(request):
    return render(request, 'surveys/list.html', {'surveys': Survey.objects.all()})

@login_required
def create_survey(request, survey_id):
    if request.method == 'POST':
        form = SurveyAddForm(request.POST)
        if form.is_valid():
            survey = form.save(commit=False)
            survey.owner = request.user
            survey.save()
            return redirect('surveys:survey_index')
    else:
        return redirect('surveys:survey_index')

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
        'form': SurveyAddForm(),  # Assuming you have a form for adding surveys
    }
    return render(request, 'surveys/index.html', context)



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