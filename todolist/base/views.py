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
from django.contrib.auth import login
from django.contrib import messages
from django.http import JsonResponse



# Create your views here.


     
class RegisterPage(FormView):
    template_name='base/register.html'
    form_class=CreateUserForm
    redirect_authenticated_user=True
    success_url=reverse_lazy('login')

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
    

    def get_success_url(self):
        profile=Profile.objects.filter(user=self.request.user)
        if not profile.exists():
            return redirect('register')
        profile[0].otp =str(random.randint(1000,9999))
        profile[0].save()
        # MessageHandler(profile[0].phone_number,profile[0].otp).send_otp()
        return reverse_lazy('otp',kwargs={'pk':profile[0].uid})
    

class OTPView(LoginRequiredMixin,CreateView):
    template_name='base/otp.html'
    form_class=OTPForm
    success_url=reverse_lazy('tasks')
    redirect_authenticated_user=True
    
    def form_valid(self,form):
        otp=form.cleaned_data.get('otp')
        uid=self.kwargs['pk']
        profile=Profile.objects.filter(uid=uid)
        if profile[0].otp == otp:
            
            return redirect('tasks')
        else:
            return redirect('login')

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
    def post(self,request,*args,**kwargs):
        if request.method=='POST':
            task_ids=request.POST.getlist('id[]')
            for id in task_ids:
                task.objects.get(id=id).delete()
            return redirect('tasks')

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
    fields=['title','description','complete']
    success_url=reverse_lazy('tasks')
    def form_valid(self,form):
        form.instance.user=self.request.user
        return super(TaskUpdate,self).form_valid(form)
    

class TaskDelete(LoginRequiredMixin,DeleteView):
    model=task
    template_name='base/task_delete.html'
    context_object_name='task'
    success_url=reverse_lazy('tasks')

class TaskMultidelete(LoginRequiredMixin,DeleteView):
    model=task
    context_object_name='task'
    success_url=reverse_lazy('tasks')
    def post(self,request,*args,**kwargs):
        task_ids=request.POST.getlist('task_ids[]')
        task.objects.filter(id__in=task_ids).delete()
        return JsonResponse({'success':True},status=200)
    
#     def Getlist(request):
#         if request.method=='POST':
#             task_ids=request.POST.getlist('task_ids[]')
#             print(task_ids)
#             return JsonResponse({'success':True},status=200)
        
# def multidelete(request):
#     if request.method=='POST':
#         task_ids=request.POST.getlist('task_ids[]')
#         task.objects.filter(id__in=task_ids).delete()
#         return JsonResponse({'success':True},status=200)

    

def check_mychecklist(request):
    if request.method == 'POST':
        task.objects.filter(id=request.user.id).delete()
