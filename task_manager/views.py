from django.shortcuts import render


# def index(request):
#     return render(request, 'index.html')

from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    a = None
    a.hello() # Creating an error with an invalid line of code
    return HttpResponse("Hello, world. You're at the pollapp index.")