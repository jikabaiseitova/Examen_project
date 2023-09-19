from django.urls import path
from . import views

urlpatterns = [
    path('forum/', views.ForumListCreateApiView.as_view()),
    path('news/<int:pk>/', views.ForumRetrieveUpdateDestroyApiView.as_view()),
    path('forum/<int:pk>/comments/', views.post_retrieve_update_destroy_api_view),
    path('forum/<int:pk>/comments/<int:id>/', views.CommentRetrieveUpdateDestroyAPIView.as_view()),

]
