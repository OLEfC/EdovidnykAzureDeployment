from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.shortcuts import redirect


@csrf_exempt
def register(request):
    if request.method == 'POST':
        username = request.POST['login']
        password = request.POST['password']
        email = request.POST['email']
        # Створення користувача за допомогою create_user
        user = User.objects.create_user(username, email, password)
        user.save()
        return redirect("/main/")
    else:
        return render(request, 'register.html')

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST['login']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/main')
        else:
            error_message = "Неправильний логін або пароль."
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')
