from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework import status

from django.http import HttpResponse
from django.http import JsonResponse

from .models import User
from .serializers import UserSerializer

from .mail_module import verification
# Create your views here.

def dashboard(request):
    return render(request, "testing/dashboard.html")

def testing(request):
    return render(request, "testing/testing.html")

@api_view(['GET'])
def routes(request):
    routes = [
        {
            'Endpoint' : '/users/', 
            'method' : 'GET', 
            'body' : 'none', 
            'description' : 'Returns all users in the database including all information'
        }
    ]
    return Response(routes)

@api_view(['GET'])
def getUsers(request):
    Users = User.objects.all()
    serializer = UserSerializer(Users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getUser(request, pk):
    Users = User.objects.get(id=pk)
    serializer = UserSerializer(Users, many=False)
    return Response(serializer.data)

'''
Format of POST-request to register a new user:
{
    email: str,
    pass_hash: str,
    name: str,
    surname: str
}
'''

@api_view(['POST'])
def register_user(request):
    user_data = JSONParser().parse(request)
    user_data['verified'] = False
    user_serializer = UserSerializer(data=user_data)
    if user_serializer.is_valid():
        user_serializer.save()
        verification.send_verification_mail(user_serializer.initial_data['email'])
        return JsonResponse(user_serializer.data, status=status.HTTP_201_CREATED) 
    return JsonResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

