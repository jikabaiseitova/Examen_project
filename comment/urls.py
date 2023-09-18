from django.urls import path
from . import views

urlpatterns = [
    path('forum/', views.ForumListCreateApiView),
    path('news/<int:pk>/', views.ForumRetrieveUpdateDestroyApiView.as_view()),
    path('forum/<int:pk>/comments/', views.forum_list_create_api_view),
    path('forum/<int:pk>/comments/<int:pk>', views.CommentRetrieveUpdateDestroyAPIView.as_view()),

]
