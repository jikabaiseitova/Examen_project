from django.contrib.sites import requests
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import User
from .serializers import AuthorSerializer


@api_view(http_method_names=['GET', 'POST'])
@authentication_classes(authentication_classes=[TokenAuthentication])
@permission_classes([AllowAny])
def author_list_api_view(request):
    if request.method == 'GET' and request.user.is_staff:
        authors = User.objects.all()
        serializer = AuthorSerializer(data=authors, many=True)
        serializer.is_valid()
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

