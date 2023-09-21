import requests
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User


class AuthorSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'password2', 'telegram_chat_id']

    def create(self, validated_data):
        author = User(
            username=validated_data['username'],
            telegram_chat_id=validated_data['telegram_chat_id']
        )
        bot_message = f"Добро пожаловать в наш форум, {author.username}"
        bot_token = '6009637428:AAFc_6QOklxowo6JymlAARKTRreFkxOZqQc'
        bot_chat_id = author.telegram_chat_id
        send_text = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={bot_chat_id}&parse_mode=Markdown&text={bot_message}'
        response = requests.get(send_text)
        response.json()
        if validated_data['password'] == validated_data['password2']:
            author.set_password(validated_data['password'])
            author.save()
            return author
        raise ValidationError("Wrong password!")

