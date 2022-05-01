from django.shortcuts import render

def layout_test(request):
    return render(request, "login/index.html")

# Create your views here.
