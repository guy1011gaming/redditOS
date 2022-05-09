from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import User
from .serializers import UserSerializer
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
    data = request.data
    mail = data['email']
    pass_has = data['pass_hash']
    name = data['name']
    surname = data['name']

