from django.contrib.sites import requests
from requests import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly

from .models import Forum, Comment
from .permissions import Permission
from .serializers import ForumSerializer, CommentSerializer


BOT_TOKEN = '6290334035:AAFWAdAhZG3RGAz9ZlJomSaY7nrSal9JFdo'


def telegram_bot_sendtext(bot_token, bot_chatID, bot_message):
    send_text = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={bot_chatID}&parse_mode=Markdown&text={bot_message}'
    response = requests.get(send_text)
    return response.json()


class ForumListCreateApiView(ListCreateAPIView):
    queryset = Forum.objects.all()
    serializer_class = ForumSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ForumRetrieveUpdateDestroyApiView(RetrieveUpdateDestroyAPIView):
    queryset = Forum.objects.all()
    serializer_class = ForumSerializer
    permission_classes = [Permission]
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view(http_method_names=['GET', 'POST'])
@authentication_classes(authentication_classes=[TokenAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def forum_list_create_api_view(request):
    if request.method == 'POST' and request.user.is_authenticated:
        serializer = ForumSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        tweets = Forum.objects.all()
        serializer = ForumSerializer(data=tweets, many=True)
        print(serializer.data)
        return Response(serializer.data)


class CommentRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [Permission]
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)