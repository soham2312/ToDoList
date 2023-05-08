from django.shortcuts import render
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView,FormView
from .models import task
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect

# Create your views here.
     
class RegisterPage(FormView):
    template_name='base/register.html'
    form_class=UserCreationForm
    redirect_authenticated_user=True
    success_url=reverse_lazy('tasks')

    def form_valid(self,form):
        user=form.save()
        if user is not None:
            login(self.request,user)
        return super(RegisterPage,self).form_valid(form)

    def get(self,*args,**kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage,self).get(*args,**kwargs)

class CustomLogoutView(LogoutView):
    next_page='login'


class CustomLoginView(LoginView):
    template_name='base/login.html'
    fields=['username','password']
    redirect_authenticated_user=True
    
    def get_success_url(self):
        return reverse_lazy('tasks')

class TaskList(LoginRequiredMixin,ListView):
    model=task  
    template_name='base/task_list.html'
    context_object_name='tasks'

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['tasks']=context['tasks'].filter(user=self.request.user)
        context['count']=context['tasks'].filter(complete=False).count()
        
        search_input=self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks']=context['tasks'].filter(title__startswith=search_input)
        
        context['search_input']=search_input
        return context

class TaskDetail(LoginRequiredMixin,DetailView):
    model=task
    template_name='base/task_detail.html'
    context_object_name='task'

class TaskCreate(LoginRequiredMixin,CreateView):
    model=task
    template_name='base/task_create.html'
    fields=['title','description','complete']
    success_url=reverse_lazy('tasks')

    def form_valid(self,form):
        form.instance.user=self.request.user
        return super(TaskCreate,self).form_valid(form)

class TaskUpdate(LoginRequiredMixin,UpdateView):
    model=task
    template_name='base/task_create.html'
    fields=['user','title','description','complete']
    success_url=reverse_lazy('tasks')

class TaskDelete(LoginRequiredMixin,DeleteView):
    model=task
    template_name='base/task_delete.html'
    context_object_name='task'
    success_url=reverse_lazy('tasks')