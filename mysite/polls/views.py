from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .models import Choice, Question, Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import sqlite3

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    latest_comment_list = Comment.objects.order_by('pub_date')[:20]
    context = {
        'latest_question_list': latest_question_list,
        'latest_comment_list': latest_comment_list,
    }
    return render(request, 'polls/index.html', context)

@login_required
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

@login_required
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
   
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
       
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('polls:index')
    else:
        form = UserCreationForm

    return render(request, 'register/register.html', {'form': form})      


def logout(request):
    logout(request)
    return redirect('/accounts/login')

@login_required
@csrf_exempt
def comment(request):
    if request.method == 'POST':
        c = request.POST.get("Comment", "")
        conn = sqlite3.connect('db.sqlite3')
        cur = conn.cursor()
        sql = ("INSERT INTO polls_comment(comment) VALUES ('"+str(c)+"')")
        cur.execute(sql)
        conn.commit()
        messages.success(request, "your message has been saved")
    return redirect('polls:index') 