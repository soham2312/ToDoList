from django.shortcuts import render
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from .models import task
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView

# Create your views here.

class CustomLoginView(LoginView):
    template_name='base/login.html'
    fields=['username','password']
    redirect_authenticated_user=True
    
    def get_success_url(self):
        return reverse_lazy('tasks')

class TaskList(ListView):
    model=task  
    template_name='base/task_list.html'
    context_object_name='tasks'

class TaskDetail(DetailView):
    model=task
    template_name='base/task_detail.html'
    context_object_name='task'

class TaskCreate(CreateView):
    model=task
    template_name='base/task_create.html'
    fields=['user','title','description','complete']
    success_url=reverse_lazy('tasks')

class TaskUpdate(UpdateView):
    model=task
    template_name='base/task_create.html'
    fields=['user','title','description','complete']
    success_url=reverse_lazy('tasks')

class TaskDelete(DeleteView):
    model=task
    template_name='base/task_delete.html'
    context_object_name='task'
    success_url=reverse_lazy('tasks')