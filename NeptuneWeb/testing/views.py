from django.shortcuts import render

# Create your views here.

def dashboard(request):
    return render(request, "testing/dashboard.html")

def testing(request):
    return render(request, "testing/testing.html")