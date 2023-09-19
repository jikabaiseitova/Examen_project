from django.contrib.sites import requests
from django.dispatch import receiver
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from comment.models import bot
from django.db.models.signals import post_save
from .models import User
from .serializers import AuthorSerializer


BOT_TOKEN = '6290334035:AAFWAdAhZG3RGAz9ZlJomSaY7nrSal9JFdo'


def telegram_bot_sendtext(bot_token, bot_chatID, bot_message):
    send_text = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={bot_chatID}&parse_mode=Markdown&text={bot_message}'
    response = requests.get(send_text)
    return response.json()


# @receiver(post_save, sender=User)
# def send_notification(sender, instance, **kwargs):
#     if kwargs.get('created'):
#         message = f"Добро пожаловать в наш форум, {instance.user.username}!"
#         bot.send_message(chat_id=instance.user.telegram_chat_id, text=message, parse_mode='html')
#
#     if __name__ == '__main__':
#         bot.infinity_polling()


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

