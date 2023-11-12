from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.views import generic
from polls.models import Poll, Vote

from .forms import SurveyAddForm
from .models import Survey
from common.utils.decorators import require_owner

class SurveyListView(generic.ListView):
    model = Survey
    context_object_name = "surveys"
    template_name = "surveys/index.html"
    paginate_by = 10
    queryset = Survey.objects.all().order_by('-created_at')

    def get_queryset(self):
        queryset = super().get_queryset()
        title_sort = self.request.GET.get('title')
        created_at_sort = self.request.GET.get('created_at')
        search_term = self.request.GET.get('search_term')

        if title_sort:
            queryset = queryset.order_by('title')
        elif created_at_sort:
            queryset = queryset.order_by('created_at')

        if search_term:
            queryset = queryset.filter(title__icontains=search_term)  # filter by 'title' field

        return queryset

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
@require_owner(Survey, 'survey_id')
def survey_end(request, survey_id):
    survey = get_object_or_404(Survey, pk=survey_id)
    survey.active = not survey.active
    survey.save()
    return redirect("surveys:survey_index")

@login_required
@require_owner(Survey, 'survey_id')
def survey_report(request, survey_id):
    survey = get_object_or_404(Survey, pk=survey_id)

    context = {
        'survey': survey,
        'polls': survey.poll_set.all(),
    }
 
    return render(request, 'surveys/results.html', context)