from django.shortcuts import render, redirect
from django.http import HttpResponse
from todolist_app.models import Tasklist
from todolist_app.forms import Taskform
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

def index(request):
    context = {
       'index_text': 'Welcome to Home Page!!',
    }
    return render(request, 'index.html', context)
 
@login_required
def todolist(request):
   if request.method == 'POST':
      form = Taskform(request.POST or None)
      if form.is_valid():
         form.save(commit=False).manager = request.user
         form.save()
      messages.success(request, ('New Task Added!'))
      return redirect('todolist')
   else:
      all_tasks = Tasklist.objects.filter(manager=request.user)
      paginator = Paginator(all_tasks, 5)
      page = request.GET.get('pg')
      all_tasks = paginator.get_page(page)
      return render(request, 'todolist.html', {'all_tasks': all_tasks})

def contact(request):
    context = {
       'contact_text': 'Contact Us',
    }
    return render(request, 'contact.html', context)

def about(request):
    context = {
       'about_text': 'About Taskmate',
    }
    return render(request, 'about.html', context)

@login_required
def delete_task(request, task_id):
   task = Tasklist.objects.get(pk=task_id)
   if task.manager == request.user:
      task.delete()
   else:
      messages.error(request, ('You are not authenticated for this operation'))
   return redirect('todolist')

@login_required
def edit_task(request, task_id):
   if request.method == 'POST':
      task = Tasklist.objects.get(pk=task_id)
      form = Taskform(request.POST or None, instance=task)
      if form.is_valid:
         form.save()
      messages.success(request, ('Task Edited!'))
      return redirect('todolist')
   else:
      task = Tasklist.objects.get(pk=task_id)
      return render(request, 'edit.html', {'task_obj': task})

@login_required
def complete_task(request, task_id):
   task = Tasklist.objects.get(pk=task_id)
   if task.manager == request.user:
      task.done = True
      task.save()
   else:
      messages.error(request, ('You are not authenticated for this operation'))
   return redirect('todolist')

@login_required
def pending_task(request, task_id):
   task = Tasklist.objects.get(pk=task_id)
   if task.manager == request.user:
      task.done = False
      task.save()
   else:
      messages.error(request, ('You are not authenticated for this operation'))
   return redirect('todolist')

