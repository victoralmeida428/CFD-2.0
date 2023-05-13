from django.shortcuts import render

def index(request):
    return render(request, 'generico/index.html')

def about(request):
    return render(request, 'generico/about.html')