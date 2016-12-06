from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import generics
from app.singleton import SystemLog
from app.models import Task, WorkPlan, WorkerType, Worker, Brigade, Record
from app.serializers import TaskSerializer, WorkPlanSerializer, WorkerTypeSerializer, WorkerSerializer, BrigadeSerializer
from django.http import HttpResponse
import logging


# Create your views here.
def index_page(request):
    return HttpResponse(render(request, 'index.html'))


def register_page(request):
    return HttpResponse(render(request, 'register.html'))


def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        usermail = request.POST['usermail']
        password = request.POST['password']
        g = Group.objects.filter(name='Client')

        user = User.objects.create_user(username=username, email=usermail, password=password)
        user.groups.add(g)
        user.save()

    return HttpResponse(render(request, 'login.html'))


def menu_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        logging.basicConfig(level=logging.DEBUG)
        log = logging.getLogger()
        if user is not None:
            if user.is_active:
                login(request, user)
                SystemLog(user)
                log.info('user '+username+' logged in')
                if len(user.groups.filter(name='Client')) > 0:
                    return HttpResponse(render(request, 'menu.html', {'login': username}))
                elif len(user.groups.filter(name='Employee')) > 0:
                    return HttpResponse(render(request, 'employee_menu.html', {'login': username}))
                else:
                    return HttpResponse(render(request, 'admin_menu.html', {'login': username}))
            else:
                log.info('inactive user ' + username + ' tried to log in')
                return HttpResponse('<h1>inactive</h1>')
        else:
            log.info('unknown user ' + username + ' tried to log in')
            return HttpResponse('<h1>fail</h1>')
    else:
        user = request.user
        if user is not None:
            username = request.user.username
            if len(user.groups.filter(name='Client')) > 0:
                return HttpResponse(render(request, 'menu.html', {'login': username}))
            elif len(user.groups.filter(name='Employee')) > 0:
                return HttpResponse(render(request,'employee_menu.html', {'login': username}))
            else:
                return HttpResponse(render(request, 'admin_menu.html', {'login': username}))
        return HttpResponse(render(request, 'login.html'))


def logout_view(request):
    logout(request)

    return HttpResponse(render(request, 'logout.html'))


def add_task_form_view(request):
    return HttpResponse(render(request, 'add_task.html'))


def add_task_view(request):
    new_task = Task(
        person_name=request.user,
        short_name=request.POST['title'],
        description=request.POST['description'],
        address=request.POST['address'],
        is_completed=False
    )
    new_task.save()

    return HttpResponse(render(request, 'menu.html'))


def list_tasks_view(request):
    tasks = Task.objects.filter(person_name=request.user)
    plans = WorkPlan.objects.filter(task__person_name=request.user)
    return HttpResponse(render(request, 'list_tasks.html', {'tasks': tasks, 'plans': plans}))


def employee_tasks(request):
    tasks1 = WorkPlan.objects.filter(brigade__member1__name=request.user)
    tasks2 = WorkPlan.objects.filter(brigade__member2__name=request.user)
    tasks3 = WorkPlan.objects.filter(brigade__member3__name=request.user)
    t1 = []
    tasks = []
    for t in tasks1:
        t1.append(t)
    for t in tasks2:
        tasks.append(t)
    for t in tasks3:
        tasks.append(t)
    return HttpResponse(render(request, 'employee_tasks.html', {'user': request.user, 't1': t1, 'tasks': tasks}))


def complete_task(request):
    id = request.GET['id']
    t = Task.objects.get(id=id)
    t.is_completed = True
    t.save()
    tasks1 = WorkPlan.objects.filter(brigade__member1__name=request.user)
    tasks2 = WorkPlan.objects.filter(brigade__member2__name=request.user)
    tasks3 = WorkPlan.objects.filter(brigade__member3__name=request.user)
    t1 = []
    tasks = []
    for t in tasks1:
        t1.append(t)
    for t in tasks2:
        tasks.append(t)
    for t in tasks3:
        tasks.append(t)
    return HttpResponse(render(request, 'employee_tasks.html', {'user': request.user, 't1': t1, 'tasks': tasks}))


def admin_user_list(request):
    u = User.objects.all()
    users = []
    for user in u:
        gr = ''
        if len(user.groups.filter(name='Client')) > 0:
            gr = 'Student'
        elif len(user.groups.filter(name='Employee')) > 0:
            gr = 'Employee'
        else:
            gr = 'Admin'
        users.append([user.id, user.username, user.email, gr])
    return HttpResponse(render(request, 'admin_user_list.html', {'users': users}))


def admin_user_detail(request):
    try:
        uid = request.GET['id']
        u = User.objects.filter(id=uid)[0]
        return HttpResponse(render(request, 'admin_user_detail.html', {'sel': u, 'act': 'edit', 'id': uid}))
    except MultiValueDictKeyError:
        u = User(username='', email='', password='')
        return HttpResponse(render(request, 'admin_user_detail.html', {'sel': u, 'act': 'new'}))


def admin_user_save(request):
    act = request.GET['action']
    if act == 'new':
        username = request.POST['username']
        usermail = request.POST['usermail']
        gr = request.POST['type']
        u = User.objects.create_user(username=username, email=usermail, password='123')
        if gr == 'Admin':
            u.is_superuser = True
        else:
            g = Group.objects.filter(name=gr)
            u.groups.add(g[0].id)
            if gr == 'Employee':
                e = Worker.objects.create(name=u)
                e.save()
        u.save()
    elif act == 'edit':
        username = request.POST['username']
        usermail = request.POST['usermail']
        gr = request.POST['type']
        u = User.objects.get(id=request.POST['uid'])
        u.username = username
        u.email = usermail
        u.groups.clear()
        if gr == 'Admin':
            u.is_superuser = True
        else:
            g = Group.objects.filter(name=gr)
            u.groups.add(g[0].id)
        u.save()
    elif act == 'delete':
        u = User.objects.get(id=request.GET['id'])
        u.delete()

    us = User.objects.all()
    users = []
    for user in us:
        gr = ''
        if len(user.groups.filter(name='Client')) > 0:
            gr = 'Client'
        elif len(user.groups.filter(name='Employee')) > 0:
            gr = 'Employee'
        else:
            gr = 'Admin'
        users.append([user.id, user.username, user.email, gr])
    return HttpResponse(render(request, 'admin_user_list.html', {'users': users}))


def admin_record_list(request):
    recs = Record.objects.all()
    r = []
    for rec in recs:
        r.append(str(rec))
    return HttpResponse(render(request, 'admin_record_list.html', {'records': r}))


def admin_wt_list(request):
    wts = WorkerType.objects.all()
    return HttpResponse(render(request, 'admin_workertype_list.html', {'wts': wts}))


def admin_wt_detail(request):
    try:
        wtid = request.GET['id']
        wt = WorkerType.objects.filter(id=wtid)[0]
        return HttpResponse(render(request, 'admin_workertype_detail.html', {'sel': wt, 'act': 'edit', 'id': wtid}))
    except MultiValueDictKeyError:
        wt = WorkerType(name='')
        return HttpResponse(render(request, 'admin_workertype_detail.html', {'sel': wt, 'act': 'new'}))


def admin_wt_save(request):
    act = request.GET['action']
    if act == 'new':
        name = request.POST['wtname']
        wt = WorkerType.objects.create(name=name)
        wt.save()
    elif act == 'edit':
        name = request.POST['wtname']
        wt = WorkerType.objects.get(id=request.POST['wtid'])
        wt.name = name
        wt.save()
    elif act == 'delete':
        wt = WorkerType.objects.get(id=request.GET['id'])
        wt.delete()

    wts = WorkerType.objects.all()
    return HttpResponse(render(request, 'admin_workertype_list.html', {'wts': wts}))


def admin_worker_list(request):
    workers = Worker.objects.all()
    return HttpResponse(render(request, 'admin_worker_list.html', {'workers': workers}))


def admin_worker_detail(request):
    wt = WorkerType.objects.all()
    try:
        wid = request.GET['id']
        w = Worker.objects.filter(id=wid)[0]
        return HttpResponse(render(request, 'admin_worker_detail.html', {'sel': w, 'act': 'edit', 'id': wid, 'wt': wt}))
    except MultiValueDictKeyError:
        w = Worker(name='')
        return HttpResponse(render(request, 'admin_worker_detail.html', {'sel': w, 'act': 'new', 'wt': wt}))


def admin_worker_save(request):
    act = request.GET['action']
    if act == 'new':
        name = request.POST['wname']
        wt = Worker.objects.create(name=name)
        wt.save()
    elif act == 'edit':
        name = request.POST['wname']
        spec = request.POST['spec']
        wt = Worker.objects.get(id=request.POST['wid'])
        wt.name = User.objects.filter(username=name)[0]
        wt.type = WorkerType.objects.filter(name=spec)[0]
        wt.save()
    elif act == 'delete':
        wt = WorkerType.objects.get(id=request.GET['id'])
        wt.delete()

    wts = Worker.objects.all()
    return HttpResponse(render(request, 'admin_worker_list.html', {'workers': wts}))


def admin_brigade_list(request):
    brigades = Brigade.objects.all()
    return HttpResponse(render(request, 'admin_brigade_list.html', {'bris': brigades}))


def admin_brigade_detail(request):
    w = Worker.objects.all()
    try:
        bid = request.GET['id']
        b = Brigade.objects.filter(id=bid)[0]
        return HttpResponse(render(request, 'admin_brigade_detail.html', {'sel': b, 'act': 'edit', 'id': bid, 'ws': w}))
    except MultiValueDictKeyError:
        b = Brigade()
        return HttpResponse(render(request, 'admin_brigade_detail.html', {'sel': b, 'act': 'new', 'ws': w}))


def admin_brigade_save(request):
    act = request.GET['action']
    if act == 'new':
        mem1 = Worker.objects.filter(id=request.POST['mem1'])[0]
        mem2 = Worker.objects.filter(id=request.POST['mem2'])[0]
        mem3 = Worker.objects.filter(id=request.POST['mem3'])[0]
        b = Brigade.objects.create(member1=mem1, member2=mem2, member3=mem3)
        b.save()
    elif act == 'edit':
        b = Brigade.objects.get(id=request.POST['bid'])
        b.member1 = Worker.objects.filter(id=request.POST['mem1'])[0]
        b.member2 = Worker.objects.filter(id=request.POST['mem2'])[0]
        b.member3 = Worker.objects.filter(id=request.POST['mem3'])[0]
        b.save()
    elif act == 'delete':
        b = Brigade.objects.get(id=request.GET['id'])
        b.delete()

    bris = Brigade.objects.all()
    return HttpResponse(render(request, 'admin_brigade_list.html', {'bris': bris}))


def admin_workplan_list(request):
    plans = WorkPlan.objects.all()
    return HttpResponse(render(request, 'admin_workplan_list.html', {'plans': plans}))


def admin_workplan_detail(request):
    b = Brigade.objects.all()
    t = Task.objects.all()
    try:
        wid = request.GET['id']
        w = WorkPlan.objects.filter(id=wid)[0]
        return HttpResponse(render(request, 'admin_workplan_detail.html', {'sel': w, 'act': 'edit', 'id': wid, 'bs': b, 'ts': t}))
    except MultiValueDictKeyError:
        w = WorkPlan()
        return HttpResponse(render(request, 'admin_workplan_detail.html', {'sel': w, 'act': 'new', 'bs': b, 'ts': t}))


def admin_workplan_save(request):
    act = request.GET['action']
    if act == 'new':
        t = Task.objects.filter(id=request.POST['task'])[0]
        b = Brigade.objects.filter(id=request.POST['brigade'])[0]
        d = request.POST['date']
        p = WorkPlan.objects.create(task=t, brigade=b, date=d)
        p.save()
    elif act == 'edit':
        p = WorkPlan.objects.get(id=request.POST['wpid'])
        p.task = Task.objects.filter(id=request.POST['task'])[0]
        p.brigade = Brigade.objects.filter(id=request.POST['brigade'])[0]
        p.date = request.POST['date']
        p.save()
    elif act == 'delete':
        p = WorkPlan.objects.get(id=request.GET['id'])
        p.delete()

    plans = WorkPlan.objects.all()
    return HttpResponse(render(request, 'admin_workplan_list.html', {'plans': plans}))


# API views

class WorkerTypeList(generics.ListCreateAPIView):
    queryset = WorkerType.objects.all()
    serializer_class = WorkerTypeSerializer


class WorkerTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = WorkerType.objects.all()
    serializer_class = WorkerTypeSerializer


class WorkerList(generics.ListCreateAPIView):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer


class WorkerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer


class BrigadeList(generics.ListCreateAPIView):
    queryset = Brigade.objects.all()
    serializer_class = BrigadeSerializer


class BrigadeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Brigade.objects.all()
    serializer_class = BrigadeSerializer


class TaskList(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class WorkPlanList(generics.ListCreateAPIView):
    queryset = WorkPlan.objects.all()
    serializer_class = WorkPlanSerializer


class WorkPlanDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = WorkPlan.objects.all()
    serializer_class = WorkPlanSerializer
