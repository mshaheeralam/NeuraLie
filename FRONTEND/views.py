from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user
from .forms import CreateUserForm
from .models import Info, Questions
from datetime import datetime
from django.contrib.auth.decorators import login_required
from BACKEND.Modality2_FacialExpressions.script import FE
from BACKEND.Modality1_EyeBlink.script import BP
import multiprocessing
import os
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

# Create your views here.
c = Info()
q = Questions()

@login_required(login_url="login")
def home(request):
    global c
    user = get_user(request)
    if request.method == "POST":
        c.name = request.POST.get('name', '')
        c.age = request.POST.get('age', '')
        c.gender = request.POST.get('gender', '')
        now = datetime.now()
        c.time = now.strftime("%Y-%m-%d %H:%M")
        c.interviewer = user.username

        with open("logs.txt", "a") as file: 
            file.write(f"{c.name}/{c.age}/{c.gender}/{c.time}/{c.interviewer}\n")

        return render(request, 'FRONTEND/interview.html')
    else:
        return render(request, 'FRONTEND/home.html')

def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    context = {'form': form}
    return render(request, 'FRONTEND/register.html', context)

def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return render(request, 'FRONTEND/home.html')
        else:
            messages.error(request, 'Wrong Credentials!')
            return redirect('login')
    else:
        user = get_user(request)
        print(user.username)
        if user.username:
            return render(request, 'FRONTEND/home.html')
    return render(request, 'FRONTEND/login.html')

@login_required(login_url="login")
def signout(request):
    logout(request)
    return redirect('login')

@login_required(login_url="login")
def logs(request):
    data = Info.objects.all()
    context = {'data': data}
    return render(request, "FRONTEND/logs.html", context)

@login_required(login_url="login")
def demo(request):
    video = request.GET.get('video-input')
    if video:
        video = 'Data/'+video
        fe_result, bp_result = run_parallel(video)
        context = {}
        if video[11] == 'l':
            context['Groundtruth'] = 'Lie'
        elif video[11] == 't':
            context['Groundtruth'] = 'True'
        context['Facial Expressions'] =  fe_result[0]
        context['Blink Pattern'] =  bp_result[0]

        if bp_result[1][0] > 0.6:
            context['Combined'] = 'Lie'
        else:
            if fe_result[1] < 0.4:
                context['Combined'] = 'Lie'
            else:
                context['Combined'] = 'True'
        print(context)
        return render(request, 'FRONTEND/demo.html', {'context': context})
    else:
        return render(request, 'FRONTEND/demo.html')

@login_required(login_url="login")
def record(request):
    global q 
    question = request.GET.get('question')
    if question:
        q.question = question
        return render(request, 'FRONTEND/record.html')
    return render(request, 'FRONTEND/interview.html')

@login_required(login_url="login")
def interview(request):
    global q, c
    if c.name:
        if os.path.exists('temp.webm'):

            fe_result, bp_result = run_parallel('temp.webm')
            context = {}

            context['Facial Expressions'] =  fe_result[0]
            context['Blink Pattern'] =  bp_result[0]

            
            if bp_result[1][0] > 0.6:
                context['Combined'] = 'Lie'
                q.is_truthful = 0
            else:
                if fe_result[1] < 0.4:
                    context['Combined'] = 'Lie'
                    q.is_truthful = 0
                else:
                    context['Combined'] = 'True'
                    q.is_truthful = 1
            print(context)
            
            # create Info instance if it doesn't exist yet
            try:
                info = Info.objects.get(name=c.name)
            except:
                c.save()
            info = Info.objects.get(name=c.name)    
            q.name = info
            q.save()
            os.remove('temp.webm')
            return render(request, 'FRONTEND/interview.html', {'context': context})
        return render(request, 'FRONTEND/interview.html')
    return render(request, 'FRONTEND/home.html')

@login_required(login_url="login")
@csrf_exempt
def upload(request):
    if request.method == 'POST':
        video_data = request.FILES.get('video_data')
        print(video_data)
        # print(video_data.read())

        if video_data:
            with open('temp.webm', 'wb+') as destination:
                for chunk in video_data.chunks():
                    destination.write(chunk)
            return HttpResponse('WebM file saved successfully')
    #         return render(request, 'FRONTEND/interview.html', {'context': context})
    #     return render(request, 'FRONTEND/record.html')
    # return render(request, 'FRONTEND/interview.html')

@login_required(login_url="login")
def log(request):
    name = request.GET.get('name')
    if name:
        try:
            info = Info.objects.get(name=name)
        except:
            return render(request, 'FRONTEND/log.html')
        questions = Questions.objects.filter(name=info)
        context = {
            'name': name,
            'questions': questions,
        }
        return render(request, 'FRONTEND/log.html', context)
    return render(request, 'FRONTEND/log.html')

def run_parallel(video):
    '''
    Run functions in parallel
    '''

    # create a pipe for communication
    FE_conn, FE_child_conn = multiprocessing.Pipe()
    BP_conn, BP_child_conn = multiprocessing.Pipe()

    # create a process for FE and BP
    FE_process = multiprocessing.Process(target=FE, args=(video, FE_child_conn))
    BP_process = multiprocessing.Process(target=BP, args=(video, BP_child_conn))

    # start the processes
    FE_process.start()
    BP_process.start()

    # receive the results
    print("Sent video to FE")
    print("Sent video to BP")
    FE_result = FE_conn.recv()
    BP_result = BP_conn.recv()
    print("Received FE result")
    print("Received BP result")

    # wait for the processes to finish
    FE_process.join()
    BP_process.join()

    return FE_result, BP_result
