"""lab1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from rest_framework.urlpatterns import format_suffix_patterns

from app import views

urlpatterns = i18n_patterns(
    url(r'^admin/', admin.site.urls),
    url(r'^index/', views.index_page),
    url(r'^login/', views.login_page),
    url(r'^register/', views.register_page),
    url(r'^menu/', views.menu_page),
    url(r'^addTaskForm/', views.add_task_form_view),
    url(r'^addTask/', views.add_task_view),
    url(r'^listTasks/', views.list_tasks_view),
    url(r'^viewEmployeeTasks/', views.employee_tasks),
    url(r'^complete_task/', views.complete_task),
    url(r'^user_list/', views.admin_user_list),
    url(r'^user_add/', views.admin_user_detail),
    url(r'^user_edit/', views.admin_user_detail),
    url(r'^user_save/', views.admin_user_save),
    url(r'^record_list/', views.admin_record_list),
    url(r'^wt_list/', views.admin_wt_list),
    url(r'^wt_add/', views.admin_wt_detail),
    url(r'^wt_edit/', views.admin_wt_detail),
    url(r'^wt_save/', views.admin_wt_save),
    url(r'^worker_list/', views.admin_worker_list),
    url(r'^worker_add/', views.admin_worker_detail),
    url(r'^worker_edit/', views.admin_worker_detail),
    url(r'^worker_save/', views.admin_worker_save),
    url(r'^brigade_list/', views.admin_brigade_list),
    url(r'^brigade_add/', views.admin_brigade_detail),
    url(r'^brigade_edit/', views.admin_brigade_detail),
    url(r'^brigade_save/', views.admin_brigade_save),
    url(r'^workplan_list/', views.admin_workplan_list),
    url(r'^workplan_add/', views.admin_workplan_detail),
    url(r'^workplan_edit/', views.admin_workplan_detail),
    url(r'^workplan_save/', views.admin_workplan_save),
    url(r'^logout/', views.logout_view),
)

api_urls = [
    url(r'^worker_types/$', views.WorkerTypeList.as_view()),
    url(r'^worker_types/(?P<pk>[0-9]+)/$', views.WorkerTypeDetail.as_view()),
    url(r'^workers/$', views.WorkerList.as_view()),
    url(r'^workers/(?P<pk>[0-9]+)/$', views.WorkerDetail.as_view()),
    url(r'^brigades/$', views.BrigadeList.as_view()),
    url(r'^brigades/(?P<pk>[0-9]+)/$', views.BrigadeDetail.as_view()),
    url(r'^tasks/$', views.TaskList.as_view()),
    url(r'^tasks/(?P<pk>[0-9]+)/$', views.TaskDetail.as_view()),
    url(r'^work_plans/$', views.WorkPlanList.as_view()),
    url(r'^work_plans/(?P<pk>[0-9]+)/$', views.WorkPlanDetail.as_view()),
]

api_urls = format_suffix_patterns(api_urls)

urlpatterns += api_urls
