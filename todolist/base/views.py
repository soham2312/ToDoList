from django.shortcuts import render
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView,FormView
from .models import *
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from django.urls import reverse
from django.contrib.auth import login
from django.shortcuts import redirect
from .mixins import *
import random
from urllib.parse import quote_from_bytes

# Create your views here.
     
class RegisterPage(FormView):
    template_name='base/register.html'
    form_class=CreateUserForm
    redirect_authenticated_user=True
    success_url=reverse_lazy('tasks')

    def form_valid(self,form):
        # user=form.save()
        username=form.cleaned_data.get('username')
        phone_number=form.cleaned_data.get('phone')
        password=form.cleaned_data.get('password1')
        user=form.save();
        profile=Profile.objects.create(user=user,phone_number=phone_number)
        if user is None:
            return redirect('register')
        return super(RegisterPage,self).form_valid(form)

    def get(self,*args,**kwargs):
        if self.request.user.is_authenticated:
            return redirect('login')
        return super(RegisterPage,self).get(*args,**kwargs)

class CustomLogoutView(LogoutView):
    next_page='login'

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        profile=Profile.objects.filter(user=self.request.user)
        if not profile.exists():
            return redirect('register')
        profile[0].otp = int(random.randint(1000,9999))
        profile[0].save()
         # MessageHandler(profile[0].phone_number,profile[0].otp).send_otp()
        return reverse_lazy('otp',kwargs={'pk':profile[0].uid})
    

class OTPView(OTPForm):
    template_name='base/otp.html'
    # form_class=OTPForm
    fields=['otp']
    success_url=reverse_lazy('login')

    def form_valid(self,form,*args,**kwargs):
        otp=form.cleaned_data.get('otp')
        uid=self.kwargs['pk']
        profile=Profile.objects.filter(uid=uid)
        if profile[0].otp == otp:
            login(profile.user,self.request)
            # profile[0].otp = None
            profile[0].save()
        return super(OTPView,self).form_valid(form)
        
    def get(self,*args,**kwargs):
        uid=self.kwargs['pk']
        profile=Profile.objects.filter(uid=uid)
        if profile[0].otp is None:
            return redirect('login')
        profile[0].otp=None
        return redirect('tasks')
    

class TaskList(LoginRequiredMixin,ListView):
    model=task  
    template_name='base/task_list.html'
    context_object_name='tasks'

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['color']='red'
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