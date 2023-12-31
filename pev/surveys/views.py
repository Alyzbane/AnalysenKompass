from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic

from polls.models import Poll, Vote
from common.utils.decorators import require_owner
from .forms import SurveyAddForm
from .models import Survey

class SurveyListView(LoginRequiredMixin, generic.ListView):
    """
    Define the index view of managing the created survey
    Args:
        LoginRequiredMixin (_type_): _description_
        generic (_type_): _description_

    Returns:
        surveys: user created survey only
    """
    model = Survey
    context_object_name = "surveys"
    template_name = "surveys/index.html"
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Survey.objects.filter(owner=self.request.user).order_by('-created_at')
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
@require_owner(Survey, 'survey_id')
def survey_detail(request, survey_id):
    survey = get_object_or_404(Survey, pk=survey_id)
    polls = Poll.objects.filter(survey=survey)
    survey_has_votes = survey.has_votes()
    shared_url = request.build_absolute_uri(reverse('polls:start_vote', args={survey_id}))

    context = {
        'survey': survey,
        'polls': polls,
        'survey_has_votes': survey_has_votes,
        'shared_url': shared_url,
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

        context = {
            'form': form,
            'survey': survey,
        }

        return render(request, 'surveys/edit.html', context)

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


@login_required
def survey_complete(request):
    if request.method == "POST":
        return HttpResponseRedirect(reverse("surveys:survey_index"))
    
    return render(request, "surveys/complete.html")