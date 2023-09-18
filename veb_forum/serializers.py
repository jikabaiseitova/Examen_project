from rest_framework import serializers

from .models import User


class AuthorSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'password2', 'telegram_chat_id']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError('не правильный пороль')
        if len(attrs['password']) < 10:
            raise serializers.ValidationError('длина пароля должна быть не менее 10 символов')
        if not any(c.isdigit()
                for c in attrs['password']):
            raise serializers.ValidationError('пароль должен содержать минимум 1 цифру')
        if not any(c.isalpha()
                for c in attrs['password']):
            raise serializers.ValidationError('пароль должен содержать минимум 1 букву')
        return attrs

    def create(self, validated_data):
        author = User(
            username=validated_data['username'],
            telegram_chat_id=validated_data['telegram_chat_id']
        )
        author.set_password(validated_data['password'])
        author.save()
        return author
