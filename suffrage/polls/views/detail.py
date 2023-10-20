from django.shortcuts import render, get_object_or_404
from polls.models import Question

def detail(request, question_id):
    question = get_object_or_404(Question, pk = question_id)
    return render(request, "polls/detail.html", {"question": question})

