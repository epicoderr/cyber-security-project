from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.http import HttpResponse
from django.db import connection
from django.conf import settings

from .models import Choice, Question

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except:
        return render(request, "polls/detail.html", {
            "question": question,
            "error_message": "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

def delete_question(request, question_id):
    # FLAW: no authentication/authorization
    Question.objects.get(id=question_id).delete()
    return HttpResponse("Deleted")

def search(request):
    query = request.GET.get("q", "")

    # FLAW: raw SQL with user input
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM polls_question WHERE question_text LIKE '%{query}%'")
        results = cursor.fetchall()

    return HttpResponse(str(results))

def leak_secret(request):
    # FLAW: exposes secret key
    return HttpResponse(settings.SECRET_KEY)