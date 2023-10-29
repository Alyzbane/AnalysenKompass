from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse

from polls.forms import PollAddForm, ChoiceAddFormSet

@login_required()
def polls_add(request):
    if request.user.has_perm('polls.add_poll'):
        if request.method == 'POST':
            form = PollAddForm(request.POST)
            formset = ChoiceAddFormSet(request.POST, prefix="choice")
            if form.is_valid() and formset.is_valid():
                poll = form.save(commit=False)
                poll.owner = request.user
                poll.save()

                # Handler for formset choice save in the databbase
                for choice_form in formset:
                    choice = choice_form.save(commit=False)
                    choice.poll = poll
                    choice.save()
                    
                messages.success(
                    request, "Poll added successfully.", extra_tags='alert alert-success alert-dismissible fade show')

                return redirect('polls:list')
        else:
            form = PollAddForm()
            formset = ChoiceAddFormSet(prefix="choice")
        context = {
            'form': form,
            'formset': formset
        }
        return render(request, 'polls/add_poll.html', context)
    else:
        return HttpResponse("Sorry but you don't have permission to do that!")

def add_choice_form(request):
    formset = ChoiceAddFormSet(prefix="choice")
    return render(request, 'polls/partials/choice_form.html', {'choice_form': formset.empty_form})