from rest_framework import serializers

from .models import Forum, Comment


class ForumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forum
        read_only_fields = ['author',]
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['author', 'forum', 'created', ]
