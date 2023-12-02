from django.shortcuts import render

# Create your views here.
def showmap(request):
    return render(request, 'shop.html')
