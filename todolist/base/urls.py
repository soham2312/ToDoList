from django.urls import path
from .views import TaskList,TaskDetail,TaskCreate,TaskUpdate,TaskDelete,CustomLoginView,CustomLogoutView,RegisterPage,OTPView,task_changes
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.base import RedirectView

urlpatterns = [
    path("otp/<uuid:pk>/",OTPView.as_view(),name="otp"),
    path("login/",CustomLoginView.as_view(),name="login"),
    path("logout/",CustomLogoutView.as_view(),name="logout"),
    path("register/",RegisterPage.as_view(),name="register"),
    path("",TaskList.as_view(),name="tasks"),
    path("task/<int:pk>/",TaskDetail.as_view(),name="task"),
    path("task-create/",TaskCreate.as_view(),name="task-create"),
    path("task-update/<int:pk>/",TaskUpdate.as_view(),name="task-update"),
    path("task-delete/<int:pk>/",TaskDelete.as_view(),name="task-delete"),
    path('task-changes/', task_changes, name='task-changes')
]