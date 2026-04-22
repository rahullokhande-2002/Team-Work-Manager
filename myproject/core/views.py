from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Task_model

def signup(request):
    error = None
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            error = "Passwords do not match"
        elif User.objects.filter(username=username).exists():
            error = "Username already exists"
        else:
            User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            return redirect('login')

    return render(request, 'core/signup.html', {'error': error})



def user_login(request):
    error = None
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            error = "Invalid username or password"

    return render(request, 'core/login.html', {'error': error})


def user_logout(request):
    logout(request)
    return redirect('login')



@login_required
def dashboard(request):
    total = Task_model.objects.count()
    completed = Task_model.objects.filter(status="Completed").count()
    pending = Task_model.objects.filter(status="Pending").count()
    inprogress = Task_model.objects.filter(status="In Progress").count()
    recent = Task_model.objects.all().order_by('-id')[:5]

    context = {
        "total": total,
        "completed": completed,
        "pending": pending,
        "inprogress": inprogress,
        "recent": recent
    }
    return render(request, "core/dashboard.html", context)


@login_required
def addtask(request):
    if request.method == "POST":
        assigned_to = request.POST.get('assigned_to')
        title = request.POST.get('title')
        description = request.POST.get('description')
        priority = request.POST.get('priority')
        status = request.POST.get('status')
        due_date = request.POST.get('due_date') or None

        Task_model.objects.create(
            assigned_to=assigned_to,
            title=title,
            description=description,
            priority=priority,
            status=status,
            due_date=due_date
        )

        return redirect('allTask')

    return render(request, "core/addtask.html")


@login_required
def allTask(request):
    result = Task_model.objects.all()
    return render(request, "core/allTask.html", {'data': result})


@login_required
def delete(request, id):
    result = get_object_or_404(Task_model, id=id)
    result.delete()
    return redirect('allTask')


@login_required
def editTask(request, id):
    task_data = get_object_or_404(Task_model, id=id)

    if request.method == 'POST':
        task_data.assigned_to = request.POST.get('assigned_to')
        task_data.title = request.POST.get('title')
        task_data.description = request.POST.get('description')
        task_data.priority = request.POST.get('priority')
        task_data.status = request.POST.get('status')
        task_data.due_date = request.POST.get('due_date') or None

        task_data.save()
        return redirect('allTask')

    return render(request, 'core/editTask.html', {'data': task_data})