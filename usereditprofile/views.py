from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.db import connection  # Імпортуйте об'єкт підключення

from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.shortcuts import redirect

# Create your views here.
def main(request):
    return render(request, 'usereditprofile.html')
@login_required(login_url='/login/')
def data(request):
    dataparse=[]
    user = request.user.id
    with connection.cursor() as cursor:
        cursor.execute(
            '''
           SELECT username,email FROM edovidnyk.auth_user
            where id=%s; 
            ''',[user] ,  # Повторити idpage 7 разів для всіх запитів
            )
        dataparse = cursor.fetchall()
        print(dataparse)
        print(user)
    return render(request, 'usereditprofile.html', {'dataparse': dataparse[0]})

@csrf_exempt
def change_username(request):
    if request.method == 'POST':
        new_username = request.POST['new_username']
        if User.objects.filter(username=new_username).exists():
            return HttpResponse('Username already exists')
        else:
            user = request.user
            user.username = new_username
            user.save()
            return redirect('/usereditprofile')
    else:
        return render(request, 'change_username.html')
    
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password

@login_required
def change_passwd(request):
    if request.method == 'POST':
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        user = request.user
        if check_password(old_password, user.password):
            user.set_password(new_password)
            user.save()
            return redirect('/main')
        else:
            return HttpResponse('Invalid old password')
    else:
        return render(request, 'change_password.html')

