from django.shortcuts import render
from rest_framework.response import responses
from rest_framework import viewsets 
from rest_framework.request import Request
# Create your views here.
from .serializers import UpdateSerilizer 
from .models import Update







# def getUpdate(request:Request) :
#     vertion = request.data.get("version")  

#     updatefile = Update.objects.all().filter(is_active=True,version=vertion).order_by("id")   




class UpdatesViewset (viewsets.ModelViewSet):


    queryset = Update.objects.all().filter(is_active=True).order_by("id")
    serializer_class = UpdateSerilizer
    # permission_classes = [permissions.IsAuthenticated]

