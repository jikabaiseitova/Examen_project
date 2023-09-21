from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from .models import Forum, Comment
from .permissions import Permission
from .serializers import ForumSerializer, CommentSerializer


class ForumListCreateApiView(ListCreateAPIView):
    queryset = Forum.objects.all()
    serializer_class = ForumSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ForumUpdateDestroyApiView(RetrieveUpdateDestroyAPIView):
    queryset = Forum.objects.all()
    serializer_class = ForumSerializer
    permission_classes = [Permission]
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view(http_method_names=['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def comment_list_create_api_view(request, forum_id):
    comments = Comment.objects.filter(forum=forum_id)

    if request.method == 'GET':
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        author = request.user
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=author, forum_id=forum_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([Permission])
def comment_retrieve_update_destroy_api_view(request, forum_id, comment_id):
    comment = get_object_or_404(Comment, forum=forum_id, id=comment_id)

    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    if request.method == 'PUT':
        if comment.author == request.user:
            serializer = CommentSerializer(comment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        if comment.author == request.user:
            comment.delete()
            return Response({'detail': 'Комментарий успешно удален.'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'detail': 'Вы не являетесь автором этого комментария.'}, status=status.HTTP_403_FORBIDDEN)
