from django.shortcuts import render
from django.db import connection  # Імпортуйте об'єкт підключення
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def main(request):
    return render(request, 'search.html')

def complect(request):
    return render(request, 'complect.html')

def gpusearch(request):
    if request.method == 'GET':
        return render(request, 'gpusearch.html')
    
def ramsearch(request):
    if request.method == 'GET':
        return render(request, 'ramsearch.html')

